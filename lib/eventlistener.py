import asyncio
import pygame
from time import sleep

async def eventlistener():
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
