import time
import pygame
from pygame.locals import *

from .sprites import Wheel, Mask, Graph
from .decrees import Decrees

WIDTH = 1280
HEIGHT = 720
GREEN = (0, 255, 0)
GREY = (150, 150, 150)
MASK_POS_X = 0.35 #relative to WIDTH
MASK_POS_Y = 0.4 #relative to HEIGHT

class People():
    """
    """
    def __init__(self, decrees):
        self.sick_ppl = 1
        self.decrees = decrees

        #factor = sum((self.get_factors))
    def get_sick_people(self):
        return self.sick_ppl

    def update_sick(self):
        #dec_factor = self.decrees.get_factor
        #valid_dec_indeces = self.decrees.get_valid_indeces()
        valid_factors = []
        for i, j, k in self.decrees.get_valid_indeces():
            valid_factors.append(self.decrees.factors[i][j][k])

        standard_factor = 1
        decrees_factor = sum(valid_factors)
        self.sick_ppl = self.sick_ppl * (decrees_factor + standard_factor)
        print(f'sick people: {self.sick_ppl} with factor: {decrees_factor}')
#
#        sum_factors = sum(decree.get_factor()) for active_decrees
#        gente_giorno_dopo = gente_giorno_prima * (sum_factors + standard_factor)


class Game:
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

        self.w1 = Wheel('w1_z.png', (w1_x, w1_y))
        self.w2 = Wheel('w2_z.png', (w2_x, w2_y))
        self.w3 = Wheel('w3_z.png', (w3_x, w3_y))

        self.decrees = Decrees()
        self.people = People(self.decrees)
        self.graph = Graph(self.sick_ppls, self.days)

        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.mask, layer = 4)
        self.sprites.add(self.w1, layer = 3)
        self.sprites.add(self.w2, layer = 2)
        self.sprites.add(self.w3, layer = 1)
        self.sprites.add(self.w3, layer = 1)
        #self.sprites.add(self.graph, layer = 1)


        self.title_font = pygame.font.SysFont('Comic Sans MS', 30, True)
        self.decrees_font = pygame.font.SysFont('Comic Sans MS', 20)
        textsurface = self.title_font.render('Decreti', False, (150, 150, 150))
        self.screen.blit(textsurface,(WIDTH*0.8,HEIGHT*0.1))

        
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
                    decree_index = (
                            self.w1.decree_index, 
                            self.w2.decree_index, 
                            self.w3.decree_index)
                    print('index')
                    print(decree_index)
                    self.decrees.add_valid_decree(decree_index)
                    self.update_decrees_text()
                elif event.key == K_p:
                    self.decrees.print_valid_decrees()
                elif event.key == K_RETURN:
                    self.next_day()


    def render(self):
        """
        Do all the rendering and displaying of sprites and what not.
        """
        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)
        self.screen.blit(self.graph.surf, (WIDTH*0.1,HEIGHT*0.7))

    def update_decrees_text(self):
        """
        Update and blit the text showing the current valid decrees.
        """
        valid_decrees = 'Decreti\n'
        #valid_decrees += self.decrees.get_valid_decrees_str()

        textsurface = self.title_font.render('Decreti', False, GREY)
        text_x, text_y = WIDTH*0.6, HEIGHT*0.1
        self.screen.blit(textsurface,(text_x, text_y))

        word_width, word_height = textsurface.get_size()

        for dec in self.decrees.get_valid_decrees():
            dec_textsurface = self.decrees_font.render(dec, False, GREY)
            text_y += word_height
            self.screen.blit(dec_textsurface,(text_x, text_y))

        sick_ppl = self.people.get_sick_people()
        ppl_textsurface = self.title_font.render(f'Malati: {sick_ppl}', False, GREY)
        self.screen.blit(ppl_textsurface,(WIDTH*0.02, HEIGHT*0.6))

        day_textsurface = self.title_font.render(f'Giorno: {self.day}', False, GREY)
        self.screen.blit(day_textsurface,(WIDTH*0.06, HEIGHT*0.06))

    def next_day(self):
        self.day += 1
        self.days.append(self.day)
        self.sick_ppls.append(self.people.get_sick_people())
        #self.people.update_sick(self.decrees)
        self.people.update_sick()
        self.graph.update()

    def get_day(self):
        return self.day

    def mainloop(self):
        """
        Handle the game main loop until player stops playing.
        """

        while self.running:
            self.clock.tick(self.FPS)
            fs = time.time()
            self.render()
            events = pygame.event.get()
            self.events(events)
            self.sprites.update()
            self.render()
            self.update_decrees_text()
            pygame.display.flip()

        pygame.quit()

