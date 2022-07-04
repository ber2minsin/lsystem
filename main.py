from lsystem import Lsystem
from enum import Enum
import pygame
import sys


if __name__ == "__main__":
    size = width, height = 600, 600
    #test = Lsystem('X', ['-', '+', '[', ']'], ['F', 'X'], {'F':'FF', 'X': 'F-[[X]+X]+F[+FX]-X'}, (width, height))
    #test = Lsystem('F', ['-', '+', '[', ']'], ['F'], {'F':'FF+[+F-F-F]-[-F+F+F]'}, (width, height))
    #test = Lsystem('X+X+X+X+X+X+X+X', ['+', '-', 'F'], ['X', 'Y'], {'X': 'X+YF++YF-FX--FXFX-YF+X', 'Y': '-FX+YFYF++YF+FX--FX-YF'}, (width, height))
    test = Lsystem('FX', ['-', '+', 'F'], ['X', 'Y'], {'X': 'X+YF+', 'Y': '-FX-Y'}, (height, width), 90, 90, 10)

    pygame.init()

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    while True:
        # TODO do all of this in real time with changing variables using tkinter GUI
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    test.iterate(1)
                    test.set_draw_time(5)
                
                if event.key == pygame.K_j:
                    test.execute(screen)
                    
                    
        
