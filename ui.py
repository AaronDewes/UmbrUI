import pygame
from time import sleep
import os
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pyqrcode
import grpc


from lib.pygamefb import fbscreen
from lib.network import get_ip
from lib.qr_generator import generate_qr_code
import rpc_pb2 as ln
from warnui import WarnUI
from consts import *

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


stub = get_stub()

metadata = [('macaroon',get_macaroon())]

def check_lnd():
    try:
        warnui
    except Exception:
        warnui = WarnUI()
    try:
        response = stub.GetInfo(ln.GetInfoRequest(),metadata=metadata)
        response.num_active_channels
    except grpc._channel._InactiveRpcError:
        sleep(2)
        check_lnd()
    else:
        pygame.quit()
    
check_lnd()

print("Connected to LND")

class UmbrUI(fbscreen):
    def __init__(self):
        # Call parent constructor
        fbscreen.__init__(self)
        
        # Set background color to umbrel
        self.screen.fill(background_color)

        self.init()

        self.add_logo_and_text()
        self.add_qr_code()
        self.build_info_section("admin", get_ip(), (col1_x, row1_y))
        # Tor is always going to be really long so not sure about this one ... :/
        self.build_info_section("tor", "r7cckasdfasfdargsnf4eoxaivgiykmrcglhg4zlwueknhuw66otiid.onion", (col2_x, row1_y))

        response = stub.GetInfo(ln.GetInfoRequest(),metadata=metadata)

        self.build_info_section("Max Send", "3M Sats", (col1_x, row2_y))
        self.build_info_section("Max Recieve", "2M Sats", (col2_x, row2_y))
        self.build_info_section("Active Channels", str(response.num_active_channels), (col3_x, row2_y))
        self.build_info_section("24H Forwards", "53", (col1_x, row3_y))
            
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
 
    sleep(2)
    # Draws the surface object to the screen.
    pygame.display.update()
