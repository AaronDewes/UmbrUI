import pygame
import time
import os
import grpc
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import codecs

from lib.pygamefb import fbscreen
from lib.network import get_ip

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


from lib.pygamefb import fbscreen
from lib.network import get_ip

import pyqrcode

black = (0, 0, 0)
background_color = (247,249,251)
bold_font = 'assets/Roboto-Bold.ttf'
light_font = 'assets/Roboto-Light.ttf'


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
#response = stub.GetInfo(ln.GetInfoRequest(),metadata=metadata)
#print(response.total_balance)

class UmbrUI(fbscreen):
    def __init__(self):
        # Call parent constructor
        fbscreen.__init__(self)
        
        # Set background color to umbrel
        self.screen.fill(background_color)

        self.init()

        self.add_logo_and_text()
        self.build_info_section("admin", get_ip(), (16, 98))
        
        # Tor is always going to be really long so not sure about this one ... :/
        self.build_info_section("tor", "r7cckf5ddovlud4uytnf4eoxaivgiykmrcglhg4zlwueknhuw66otiid.onion", (160, 98))

        response = stub.GetInfo(ln.GetInfoRequest(),metadata=metadata)

        self.build_info_section("Max Send", "3M Sats", (16, 160))
        self.build_info_section("Max Recieve", "2M Sats", (160, 160))
        self.build_info_section("Active Channels", str(response.num_active_channels), (305, 160))
        self.build_info_section("24H Forwards", "53", (16, 223))
            
        pygame.display.update() 

    def init(self):
        pygame.init()
        self.titleFont = pygame.font.Font(bold_font, 46)
        self.headingFont = pygame.font.Font(light_font, 12)
        self.textFont = pygame.font.Font(bold_font, 18)

    def add_logo_and_text(self):
        title = self.titleFont.render("umbrel", True, black)

        umbrelImg = pygame.image.load('assets/logo.png')
        # pg.transform.rotozoom(IMAGE, 0, 2)
        umbrelImg = pygame.transform.scale(umbrelImg, (64, 73))

        qr = pyqrcode.create("r7cckf5ddovlud4uytnf4eoxaivgiykmrcglhg4zlwueknhuw66otiid.onion")
        qr.png("QR.png", scale=3)
        img = pygame.image.load("QR.png")
        self.screen.blit(img,(300, 150))
        pygame.display.flip()
        
        self.screen.blit(umbrelImg, (16, 16))
        self.screen.blit(title, (90, 30))

    def build_info_section(self, heading, text, position):
        heading = self.headingFont.render(heading, True, black)
        text = self.textFont.render(text, True, black)

        x, y = position
        self.screen.blit(heading, position)
        self.screen.blit(text, (x, y + 20))

# Create an instance of the UmbrUI class
game = UmbrUI()

while True:
     for event in pygame.event.get():
     
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()
 
            # quit the program.
            quit()
 
        # Draws the surface object to the screen.
        pygame.display.update()
