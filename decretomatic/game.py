import time
import pygame
import os
import random
import pprint
from pygame.locals import *

WIDTH = 1000
HEIGHT = 600
SCALE_FACTOR = 1 #2.5 #for imagees that are too big
GREEN = (0, 255, 0)
TRANSPARENT = (1, 0, 0)
MASK_POS_X = 0.35 #relative to WIDTH
MASK_POS_Y = 0.4 #relative to HEIGHT


class BaseSprite(pygame.sprite.Sprite):
    """
    Just a base sprite class to use as a parent for all the other sprites.
    It will have some useful loading methods.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('decretomatic/data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def load_sound(self, name):
        class NoneSound:
            def play(self): 
                pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error as message:
            print('Cannot load sound:', wav)
            raise SystemExit(message)
        return sound

class Decrees():
    """
    Holds all the information used for managing decrees.
    Just like a big smart dictionary.
    """
    w1_decs = (
            "evitate",
            "non recatevi ne",
            "recatevi ne",
            "non rimanete ne",
            "rimanete ne",
            "non chiuderemo",
            "chiuderemo",
            )
    w2_decs = (
            "i parchi pubblici",
            "i supermercati",
            "la propria abitazione",
            "il luogo di lavoro",
            "il comune di residenza",
            "i cantieri",
            "le scuole",
            )
    w3_decs = (
            "per esigenze lavorative",
            "per comprovate necessita'",
            "in piu' di due persone",
            "per motivi di salute",
            "a un metro di distanza",
            "per produzioni di interesse strategico",
            "per beni di prima necessita'",
            )

    def __init__(self):

        self.decrees = [[[' '.join((dec1, dec2, dec3)) for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        self.valid_decrees = [[['' for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        pprint.pprint(self.decrees)
        pprint.pprint(self.valid_decrees)

    def print_decs(self):
        print(self.w1_decs)

    def make_decreto(self, w_positions):
        pass

    def get_decreto(self):
        pass

    def add_valid_decree(self, decree_index):
        """
        Given a decree index touple it will add the corresponding decree to a list.
        """
        self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]] = \
            self.decrees[decree_index[0]][decree_index[1]][decree_index[2]]

    def print_valid_decrees(self):
        #pprint.pprint(self.valid_decrees)
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        print(self.valid_decrees[i][j][k])

    def get_valid_decrees(self):
        #pprint.pprint(self.valid_decrees)
        valid_decs = []
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_decs.append(self.valid_decrees[i][j][k])
        return valid_decs

    def calc_decree_factor(self): 
        standard_factor = 2 + random.randint(0,10)*0.1

        max_power = 10
        fix_power = 3
        exp_power = 1.2
        max_good_bad = 10
        good_bad_thresh = 6

        rand_good_bad = random.randint(1, max_good_bad)
        rand_power = random.randint(1, max_power)
        factor_good_bad = -1 if (rand_good_bad > good_bad_thresh) else  1
        factor_power = fix_power // (random_power**exp_power)

        factor = factor_good_bad * factor_power

        return factor
#
#
#class People():
#
#    def calc_sick_people(self):
#        sum_factors = sum(decree.get_factor()) for active_decrees
#        gente_giorno_dopo = gente_giorno_prima * (sum_factors + standard_factor)


class Wheel(BaseSprite):
    """
    Generic class to represent the three wheels.
    """
    layer = 1
    def __init__(self, image, position = (0, 0)):
        self.image_name = image
        BaseSprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.image, self.rect = self.load_image(image, TRANSPARENT)
        self.size = self.image.get_size()
        #self.image = pygame.transform.scale(self.image, (int(self.size[0]//SCALE_FACTOR), int(self.size[1]//SCALE_FACTOR)))
        #self.size = self.image.get_size()
        #self.rect = self.image.get_rect()
        self.rect.center = position
        print(self.rect.center)

        self.spinning = 0
        self.spins = 0
        self.initial_image = self.image.copy()
        self.decree_index = 0

    def update(self):
        """
        Spin or stay.
        """
        if self.spinning:
            self._spin()
        self.decree_index = self.spins

    def _spin(self):
        """
        Spin the wheel.
        """
        center = self.rect.center
        self.spinning += 4

        if self.spinning > 51.43:
            self.spinning = 0
            self.spins += 1

        if self.spins > 6:
            #self.image, self.rect = self.load_image(self.image_name, TRANSPARENT)
            self.image = self.initial_image.copy()
            self.spins = 0
        else:
            rotation_angle = 51.43 * self.spins + self.spinning
            self.image = pygame.transform.rotate(self.initial_image, rotation_angle)
            #print(self.spins)

        self.rect = self.image.get_rect(center = center)

    def next_decree(self):
        """
        This will spin to the next decree.
        """
        if not self.spinning:
            self.spinning = 1



class Mask(BaseSprite):
    """
    """
    layer = 2
    def __init__(self):
        BaseSprite.__init__(self)
        self.image, self.rect = self.load_image('mask_z.png', TRANSPARENT)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]//SCALE_FACTOR), int(self.size[1]//SCALE_FACTOR)))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH*MASK_POS_X, HEIGHT*MASK_POS_Y)
        #sprites.add(self, layer=self.layer)


class Graph(BaseSprite):
    """
    A graph showing number of people that are infected.
    """
    pass


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


        print(pygame.display.Info())

        self.mask = Mask()
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

        self.allsprites = pygame.sprite.RenderPlain((self.mask, self.w1, self.w2, self.w3))
        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.mask, layer = 4)
        self.sprites.add(self.w1, layer = 3)
        self.sprites.add(self.w2, layer = 2)
        self.sprites.add(self.w3, layer = 1)

        self.decrees = Decrees()
        #decrees.print_decs()

        self.title_font = pygame.font.SysFont('Comic Sans MS', 30, True)
        self.decrees_font = pygame.font.SysFont('Comic Sans MS', 20)
        textsurface = self.title_font.render('Decreti', False, (150, 150, 150))
        self.screen.blit(textsurface,(WIDTH*0.8,HEIGHT*0.1))
        
    def events(self, events):
        """
        Standard even loop.
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


    def render(self):
        """
        """
        pass

    def update_decrees_text(self):
        valid_decrees = 'Decreti\n'
        #valid_decrees += self.decrees.get_valid_decrees_str()

        textsurface = self.title_font.render('Decreti', False, (150, 150, 150))
        text_x, text_y = WIDTH*0.6, HEIGHT*0.1
        self.screen.blit(textsurface,(text_x, text_y))

        word_width, word_height = textsurface.get_size()

        for dec in self.decrees.get_valid_decrees():
            dec_textsurface = self.decrees_font.render(dec, False, (150, 150, 150))
            text_y += word_height
            self.screen.blit(dec_textsurface,(text_x, text_y))


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
            self.screen.blit(self.background, (0, 0))
            self.update_decrees_text()
            self.sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

