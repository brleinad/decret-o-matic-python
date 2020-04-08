import pygame
import random
from .locals import *
from .decrees import Decrees


class People():
    """
    Class for managing number of sick people.
    """
    def __init__(self, screen, decrees):
        self.screen = screen
        self.decrees = decrees
        self.sick_ppl = 1
        self.new_sick_ppl = 0
        self.t_new_sick_ppl = 0
        self.extra_factor = 0.0
        self.title_font = pygame.font.SysFont('Monospace', 30, True)
        self.ppl_textsurface = self.title_font.render(f'Contagi: {self.sick_ppl} (+{self.new_sick_ppl})', False, color['GREY'])
        #factor = sum((self.get_factors))
    def get_sick_people(self):
        return self.sick_ppl + self.t_new_sick_ppl
    def get_new_sick_people(self):
        return self.new_sick_ppl

    def update_sick(self):
        """
        Update the number of sick people.
        """
        #dec_factor = self.decrees.get_factor
        #valid_dec_indeces = self.decrees.get_valid_indeces()
        valid_factors = []
        for i, j, k in self.decrees.get_valid_indeces():
            valid_factors.append(self.decrees.factors[i][j][k])
        standard_factor = float(3.8 + self.extra_factor + float(random.randint(0,10))*0.02)
        decrees_factor = sum(valid_factors)
        self.new_sick_ppl=0
        self.t_new_sick_ppl += int(0.5+(self.sick_ppl+self.t_new_sick_ppl) * (max(0.0, (decrees_factor + standard_factor)-1.0)))
        if self.t_new_sick_ppl==0: self.extra_factor+=max(-(0.5*(decrees_factor-1.0),0.1))
        #print(f'sick people: {self.sick_ppl + self.t_new_sick_ppl} with factor: {decrees_factor} and std: {standard_factor}')
		
    def update(self):
        if self.t_new_sick_ppl > 0:
    	    self.sick_ppl += max(self.t_new_sick_ppl//10,1)
    	    self.new_sick_ppl += max(self.t_new_sick_ppl//10,1)
    	    self.t_new_sick_ppl -= max(self.t_new_sick_ppl//10,1)
        self.ppl_textsurface = self.title_font.render(f'Contagi: {self.sick_ppl} (+{self.new_sick_ppl})', False, color['GREY'])

