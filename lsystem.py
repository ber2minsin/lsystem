from pygame.constants import SRCCOLORKEY
import math_funcs as mf

from inspect import signature
import pygame
import math
import json
import os
import numpy as np

# In pygame the y axis is flipped, meaning the y+ is down and y- is up
# by substracting y from the screen height we can translate the coords both from pygame to actual and actual to pygame
def translate_coords(coords, height):
    return (coords[0], height - coords[1])

# If you rotate point (px, py) around point (ox, oy) by angle theta you'll get:
# p'x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
# p'y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
def rotate(rotated, around, angle):
    return (np.cos(np.deg2rad(angle)) * (rotated[0] - around[0]) - np.sin(np.deg2rad(angle)) * (rotated[1] - around[1]) + around[0],
            np.sin(np.deg2rad(angle)) * (rotated[0] - around[0]) + np.cos(np.deg2rad(angle)) * (rotated[1] - around[1]) + around[1])


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Lsystem:
    def __init__(self, axiom, constants, variables, rules, screen_size, angle=0, start_angle=0, line_length=3, line_color=(255,255,255)):
        
        self.axiom = axiom
        self.constants = constants
        self.variables = variables
        self.rules = rules
        self.angle = angle
        self.system = axiom
        self.line_length = line_length
        self.screen_size = screen_size
        self.line_color = line_color
        self.saved_drawing_states = []
        self.start_position = translate_coords((250, 250), screen_size[1])
        self.start_angle = start_angle

        # this is saved in actual coordinates meaning +y is up and -y is down        
        self.current_position = self.start_position
        
        self.current_rotation = 0
        self.current_iteration = 0
        self.last_draw = 0

        # total delay for drawing (in seconds)
        self.draw_delay = 0

        # individual delay for drawing (in ms)
        self.delay = 5

    # TODO Cleanup
    @staticmethod
    def load_from_json(fname, screen_size):
        with open(os.path.dirname(__file__) + '\\saved\\' + fname + '.json', 'r') as f:
            
            returned_obj = Lsystem('', '', '', '', '')

            lsys_as_json = json.loads(f.read())
            lsys_as_json['screen_size'] = screen_size
            
            for k, v in returned_obj.__dict__.items():
                print(k, v)
                if v is None or v == '':
                    if k not in lsys_as_json:
                        print('set to empty')
                        returned_obj.__dict__[k] = ''
                    else:
                        print(k, 'is empty or None')
                        print(lsys_as_json[k])
                        returned_obj.__dict__[k] = lsys_as_json[k]
            return returned_obj
    
    def save_to_json(self, fname):
        dct = self.__dict__
        """ 
        Saves the system with json file format
        """

        dct.pop('screen_size')
        dct.pop('current_position')
        dct.pop('current_rotation')
        dct.pop('start_position')
        dct.pop('system')

        print(dct)
        lsys_as_json = json.dumps(dct, indent=4)
        
        with open(os.path.dirname(__file__) + '\\saved_systems\\' + fname + '.json', 'w') as f:
            f.write(lsys_as_json)
        
    
    def iterate(self, n):
        """
        Advances the lsystem
        """

        for i in range(n):
            self.current_iteration += 1
            temp_system = ''
            for j in range(len(self.system)):
                if self.system[j] in self.variables:
                    temp_system += self.rules[self.system[j]]
                else:
                    temp_system += self.system[j]
                    continue
            self.system = temp_system
            print('Iteration:', self.current_iteration, 'Length of system:', len(self.system))

       

    # TODO add more drawing functions
    def lowercase_f(self):
        self.current_position = rotate((self.current_position[0], self.current_position[1] + self.line_length), self.current_position, self.current_rotation)
    
    def upperrcase_f(self, surface):
        end_pos = rotate((self.current_position[0], self.current_position[1] + self.line_length), self.current_position, self.current_rotation)
        pygame.draw.line(surface, self.line_color, translate_coords(self.current_position, self.screen_size[1]), translate_coords(end_pos, self.screen_size[1]))
        self.current_position = end_pos
    
    def plus(self):
        self.current_rotation += self.angle

    def minus(self):
        self.current_rotation -= self.angle
    
    def open_bracket(self):
        self.saved_drawing_states.append((self.current_position, self.current_rotation))
    
    def close_bracket(self):
        saved = self.saved_drawing_states.pop()
        self.current_position = saved[0]
        self.current_rotation = saved[1]

    def get_function(self, strng):
        operations = {'f': self.lowercase_f, 'F': self.upperrcase_f, '+': self.plus, '-': self.minus, '[': self.open_bracket, ']': self.close_bracket}
        
        if strng in operations:
            sig = signature(operations[strng])
            return (operations[strng], len(sig.parameters))
        else:
            return (None, None)
    
    def execute(self, screen):
        """
        Draws the lsystem into given pygame surface
        """

        if self.last_draw != self.current_iteration:
            screen.fill((0,0,0))

            self.current_position = self.start_position
            self.current_rotation = self.start_angle
        
        # Iterate through l-system
        for i in range(len(self.system)):

            (function, arglength) = self.get_function(self.system[i])

            if function and arglength is not None:
                if arglength == 0:
                    function()                   
                else:
                    function(screen)
                    pygame.display.update()
                    pygame.time.delay(self.delay)
                    pygame.time.Clock().tick()
            
        self.last_draw = self.current_iteration
    
    def set_draw_time(self, total_delay):
        """
        Sets how much time it takes to draw the whole L-System in seconds
        """
        total_drawing_functions = 0

        for i in range(len(self.system)):
            (function, arglength) = self.get_function(self.system[i])
            
            
            if function and arglength is not None:
                if arglength != 0:
                    total_drawing_functions += 1
        if total_drawing_functions != 0:
            self.delay = int(math.floor((total_delay * 1000) / total_drawing_functions))
        else:
            self.delay = 0
        print(self.delay)

