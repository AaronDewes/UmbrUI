import pygame
import time
import os
import grpc
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import codecs

from lib import pygamefb

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

class UmbrUI(pygamefb.fbgame):
    def start(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

# Connect to bitcoin RPC and get data
try:
    btcurl = "http://%s:%s@%s:%s"%(os.getenv('BITCOIN_RPC_USER'), os.getenv('BITCOIN_RPC_PASS'), os.getenv('BITCOIN_IP'), os.getenv('BITCOIN_RPC_PORT'))
    rpc_connection = AuthServiceProxy(btcurl)
    rpc_connection.getwalletinfo()
except Exception:
    print("Please make sure BITCOIN_RPC_PORT, BITCOIN_RPC_PASS, BITCOIN_IP and BITCOIN_RPC_PORT are set and valid")
    exit(1)

print("Connection to bitcoin core established.")

print("Attemtping to connect to LND")
os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

# Lnd cert is at ~/.lnd/tls.cert on Linux and
# ~/Library/Application Support/Lnd/tls.cert on Mac
cert = open(os.path.expanduser('./lnd/tls.cert'), 'rb').read()
creds = grpc.ssl_channel_credentials(cert)
lnurl = "%s:%s"%(os.getenv('LND_IP'), os.getenv('LND_GRPC_PORT'))
channel = grpc.secure_channel(lnurl, creds)
stub = lnrpc.LightningStub(channel)

if(os.getenv("USE_REGTEST")):
    with open('./lnd/data/chain/bitcoin/regtest/admin.macaroon', 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')
elif(os.getenv("USE_TESTNET")):
    with open('./lnd/data/chain/bitcoin/testnet/admin.macaroon', 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')
else:
    with open('./lnd/data/chain/bitcoin/mainnet/admin.macaroon', 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')


metadata = [('macaroon',macaroon)]

# Example
#response = stub.WalletBalance(ln.WalletBalanceRequest(),metadata=metadata)
#print(response.total_balance)

# Create an instance of the UmbrUI class
ui = UmbrUI()
ui.start()
time.sleep(10)
