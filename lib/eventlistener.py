import threading
import pygame
from time import sleep

class eventListener(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        self._running = True
        thread.start()

    def run(self):
        while self._running:
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

    def stop(self):
        self._running = False