# Libraries provided by the system
import pygame
from time import sleep
import os
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pyqrcode
import grpc
import asyncio

# Local libraries & files
import rpc_pb2 as ln
from lib.fbscreen import fbscreen
from lib.network import get_ip
from lib.qr_generator import generate_qr_code
from lib.lnd import get_stub, get_macaroon, check_lnd
from lib.eventlistener import eventlistener
from consts import black, background_color, bold_font, light_font, columns_x, rows_y

# Try to connect to bitcoin RPC and get data
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

# Wait until lnd is configured & unlocked
check_lnd()
print("Connected to LND")

# Define variables outside of the check function
stub = get_stub()
metadata = [('macaroon',get_macaroon())]

class UmbrUI(fbscreen):
    def __init__(self):
        # Call parent constructor
        fbscreen.__init__(self)
        
        # Set background color to umbrel
        self.screen.fill(background_color)

        self.init()

        self.add_logo_and_text()
        self.add_qr_code()
        self.build_info_section("admin", get_ip(), (columns_x[0], rows_y[0]))
        # Tor is always going to be really long so not sure about this one ... :/
        self.build_info_section("tor", "r7cckasdfasfdargsnf4eoxaivgiykmrcglhg4zlwueknhuw66otiid.onion", (columns_x[1], rows_y[0]))

        response = stub.GetInfo(ln.GetInfoRequest(),metadata=metadata)

        self.build_info_section("Max Send", "3M Sats", (columns_x[0], rows_y[1]))
        self.build_info_section("Max Recieve", "2M Sats", (columns_x[1], rows_y[1]))
        self.build_info_section("Active Channels", str(response.num_active_channels), (columns_x[2], rows_y[1]))
        self.build_info_section("24H Forwards", "53", (columns_x[0], rows_y[2]))
            
        pygame.display.set_caption("UmbrUI")
        pygame.display.update() 

    def init(self):
        pygame.init()
        self.titleFont = pygame.font.Font(bold_font, 56)
        self.headingFont = pygame.font.Font(light_font, 18)
        self.textFont = pygame.font.Font(bold_font, 32)

    def add_logo_and_text(self):
        title = self.titleFont.render("umbrel", True, black)

        umbrelImg = pygame.image.load('assets/logo.png')
        # pg.transform.rotozoom(IMAGE, 0, 2)
        umbrelImg = pygame.transform.scale(umbrelImg, (88, 100))
        
        self.screen.blit(umbrelImg, (16, 16))
        self.screen.blit(title, (110, 30))

    def add_qr_code(self):
        qrImg = generate_qr_code(get_ip())
        
        self.screen.blit(qrImg, (544, 16))

    def build_info_section(self, heading, text, position):
        heading = self.headingFont.render(heading, True, black)
        text = self.textFont.render(text, True, black)

        x, y = position
        self.screen.blit(heading, position)
        self.screen.blit(text, (x, y + 25))

# Create an instance of the UmbrUI class
game = UmbrUI()

asyncio.run(eventlistener())
