import grpc
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import codecs
import os

def get_stub():
    cert = open(os.path.expanduser('./lnd/tls.cert'), 'rb').read()
    creds = grpc.ssl_channel_credentials(cert)
    lnurl = "%s:%s"%(os.getenv('LND_IP'), os.getenv('LND_GRPC_PORT'))
    channel = grpc.secure_channel(lnurl, creds)
    stub = lnrpc.LightningStub(channel)
    return stub

def get_macaroon():
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
    return macaroon