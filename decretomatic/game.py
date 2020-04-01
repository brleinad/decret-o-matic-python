import time
import random
import pygame
from pygame.locals import *

from .constants import *
from .sprites import Wheel, Mask, Graph
from .decrees import Decrees

#TODOs: 
#deleting decrees, 
#game over screen
#new game option,
#Change fonts
#Use sprite sheet at the end of rotate
#improve gui with future gui
#highlight buttons when mouse hovers 

class People():
    """
    """
    def __init__(self, screen, decrees):
        self.screen = screen
        self.decrees = decrees
        self.sick_ppl = 1
        self.new_sick_ppl = 0
        self.title_font = pygame.font.SysFont('Monospace', 30, True)
        self.ppl_textsurface = self.title_font.render(f'Contagi: {self.sick_ppl} (+{self.new_sick_ppl})', False, color['GREY'])
        #factor = sum((self.get_factors))
    def get_sick_people(self):
        return self.sick_ppl
    def get_new_sick_people(self):
        return self.new_sick_ppl

    def update_sick(self):
        #dec_factor = self.decrees.get_factor
        #valid_dec_indeces = self.decrees.get_valid_indeces()
        valid_factors = []
        for i, j, k in self.decrees.get_valid_indeces():
            valid_factors.append(self.decrees.factors[i][j][k])

        standard_factor = 2.0 + float(random.randint(0,10))*0.1
        decrees_factor = sum(valid_factors)
        self.new_sick_ppl = int(self.sick_ppl * (max(1.0, (decrees_factor + standard_factor))-1))
        self.sick_ppl += self.new_sick_ppl
        print(f'sick people: {self.sick_ppl} with factor: {decrees_factor}')

        self.ppl_textsurface = self.title_font.render(f'Contagi: {self.sick_ppl} (+{self.new_sick_ppl})', False, color['GREY'])


class Game():
    FLAGS = 0
    FPS = 30

    def __init__(self):
        #pygame.mixer.pre_init()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Decret-O-Matic')
        self.running = True

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        #self.background.fill((250, 250, 250)) #WHITE
        self.background.fill((0, 0, 0)) #BLACK
        self.background.set_colorkey((10,10,10,0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.day = 1
        self.days = [self.day,]
        self.sick_ppls = [1,]
        self.new_sick_ppls = [0,]
        print(pygame.display.Info())

        self.mask = Mask((WIDTH*MASK_POS_X, HEIGHT*MASK_POS_Y))
        mask_width, mask_height = self.mask.size

        mask_topleft_x, mask_topleft_y =  self.mask.rect.topleft

        w1_x = mask_topleft_x + mask_width * 0.0721
        w1_y = mask_topleft_y + mask_width * 0.1528

        w2_x = mask_topleft_x + mask_width * 0.3099
        w2_y = mask_topleft_y + mask_width * 0.3073

        w3_x = mask_topleft_x + mask_width * 0.6558
        w3_y = mask_topleft_y + mask_width * 0.1556

        #Button positions are relative to the mask
        #oM: (255, 237) -> (227, 173)
        #W1: (255, 237) -> (278, 232)
        w1_button_pos = (mask_topleft_x + 51, mask_topleft_y + 59)
        #W2: (362, 307) -> (384, 301)
        w2_button_pos = (mask_topleft_x + 157, mask_topleft_y + 128)
        #W3: (518, 239) -> (540, 231)
        w3_button_pos = (mask_topleft_x + 313, mask_topleft_y + 58)

        self.w1 = Wheel('w1_z.png', (w1_x, w1_y), w1_button_pos)
        self.w2 = Wheel('w2_z.png', (w2_x, w2_y), w2_button_pos)
        self.w3 = Wheel('w3_z.png', (w3_x, w3_y), w3_button_pos)

        self.decrees = Decrees(self.screen)
        self.people = People(self.screen, self.decrees)
        self.graph = Graph(self.sick_ppls, self.days)

        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.mask, layer = 4)
        self.sprites.add(self.w1, layer = 3)
        self.sprites.add(self.w2, layer = 2)
        self.sprites.add(self.w3, layer = 1)
        self.sprites.add(self.w3, layer = 1)
        #self.sprites.add(self.graph, layer = 1)

        self.title_font = pygame.font.SysFont('Monospace', 30, True)
        textsurface = self.title_font.render('Decreti', False, (150, 150, 150))
        self.screen.blit(textsurface,(WIDTH*0.8,HEIGHT*0.1))

        self.decree_actions = 0
        self.day_textsurface = self.title_font.render(f'Giorno: {self.day}', False, color['GREY'])


    def update_decrees(self):
        """
        Update the list of valid decrees made by the player.
        """
        decree_index = (
                self.w1.decree_index, 
                self.w2.decree_index, 
                self.w3.decree_index)
        print('index')
        print(decree_index)
        if self.decrees.add_valid_decree(decree_index):
            self.decree_actions += 1
            self.decrees.update_decrees_text()

        if self.decree_actions >= 3:
            self.decree_actions = 0
            self.next_day()

        
    def events(self, events):
        """
        Standard event loop.
        """

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    self.w1.next_decree()
                elif event.key == K_2:
                    self.w2.next_decree()
                elif event.key == K_3:
                    self.w3.next_decree()
                elif event.key == K_SPACE:
                    self.update_decrees()
                elif event.key == K_p:
                    self.decrees.print_valid_decrees()
                elif event.key == K_RETURN: 
                    #TODO: remove this elif, only for debugging
                    self.next_day()
            elif event.type == MOUSEBUTTONDOWN:
                print(f'Mouse at {event.pos}')
                if self.w1.button_rect.collidepoint(event.pos):
                    self.w1.next_decree()
                    #print(f'W1: {self.w1.rect.center} -> {event.pos}')
                if self.w2.button_rect.collidepoint(event.pos):
                    self.w2.next_decree()
                    #print(f'W2: {self.w2.rect.center} -> {event.pos}')
                if self.w3.button_rect.collidepoint(event.pos):
                    self.w3.next_decree()
                    #print(f'W3: {self.w3.rect.center} -> {event.pos}')
                if self.mask.button_rect.collidepoint(event.pos):
                    self.update_decrees()


    def render(self):
        """
        Do all the rendering and displaying of sprites and what not.
        """
        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)
        self.screen.blit(self.graph.surf, (WIDTH*0.1,HEIGHT*0.7))
        self.screen.blit(self.people.ppl_textsurface,(WIDTH*0.02, HEIGHT*0.6))
        self.decrees.update_decrees_text()
        self.screen.blit(self.day_textsurface,(WIDTH*0.06, HEIGHT*0.06))

    def next_day(self):
        """
        Advance the game to the next day.
        """
        self.day += 1
        self.days.append(self.day)
        self.sick_ppls.append(self.people.get_sick_people())
        #self.people.update_sick(self.decrees)
        self.people.update_sick()
        self.graph.update()
        self.day_textsurface = self.title_font.render(f'Giorno: {self.day}', False, color['GREY'])

        if self.day == LAST_DAY:
            if self.sick_ppls[-1] > MAX_SICK_PPL:
                self.lost_game

    def get_day(self):
        return self.day

    def mainloop(self):
        """
        Handle the game main loop until player stops playing.
        """

        while self.running:
            self.clock.tick(self.FPS)
            fs = time.time()
            #self.render()
            events = pygame.event.get()
            self.events(events)
            self.sprites.update()
            self.render()
            pygame.display.flip()

        pygame.quit()

