import pygame
from lib.fbscreen import fbscreen
from consts import black, background_color, bold_font, light_font, columns_x, rows_y

class WarnUI(fbscreen):
    def __init__(self):
        # Call parent constructor
        fbscreen.__init__(self)
        
        # Set background color to umbrel
        self.screen.fill(background_color)

        self.init()

        self.add_logo_and_text()
        self.add_warning("You haven't opened the Umbrel dashboard yet.", (columns_x[0], rows_y[0]))
        self.add_warning("Please do that first to access this screen.", (columns_x[0], rows_y[1] - 70))
        pygame.display.set_caption("UmbrUI")
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
        pygame.display.flip()
        self.screen.blit(umbrelImg, (16, 16))
        self.screen.blit(title, (90, 30))

    def add_warning(self, text, position):
        text = self.textFont.render(text, True, black)

        x, y = position
        self.screen.blit(text, (x, y))