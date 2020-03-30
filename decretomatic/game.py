import time
import pygame
import os
import random
from pygame.locals import *

WIDTH = 1000
HEIGHT = 600
SCALE_FACTOR = 1 #2.5 #for imagees that are too big
#sprites = pygame.sprite.LayeredUpdates()
GREEN = (0, 255, 0)
TRANSPARENT = (1, 0, 0)




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

#class Decreto():
#    """
#    """
#    w1_dec = (
#            "evitate",
#            "chiuderemo",
#            "non chiuderemo",
#            "rimanete ne",
#            "non rimanete ne",
#            "recatevi ne",
#            "non recatevi ne",
#            )
#    w2_dec = (
#            "i parchi pubblici",
#            "le scuole",
#            "i cantieri",
#            "il comune di residenza",
#            "il luogo di lavoro",
#            "la propria abitazione",
#            "i supermercati",
#            )
#    w3_dec = (
#            "per esigenze lavorative",
#            "per beni di prima necessita'",
#            "per produzioni di interesse strategico",
#            "a un metro di distanza",
#            "per motivi di salute",
#            "in piu' di due persone",
#            "per comprovate necessita'",
#            )
#    decreto = [[][][]]
#
#    def __init__(self):
#
#        i, j, k = 0, 0, 0
#        for dec1 in w1_dec:
#            for dec2 in w2_dec:
#                for dec3 in w3_dec:
#                    decreti[[i][j][k]] = ' '.join(dec1, dec2, dec3)
#                    k += 1
#                j += 1
#            i += 1
#                    
#
#
#    def make_decreto(self, w_positions):
#        pass
#
#    def get_decreto(self ):
#        pass
#
#    def calc_decree_factor(self): 
#        standard_factor = 2 + random.randint(0,10)*0.1
#
#        max_power = 10
#        fix_power = 3
#        exp_power = 1.2
#        max_good_bad = 10
#        good_bad_thresh = 6
#
#        rand_good_bad = random.randint(1, max_good_bad)
#        rand_power = random.randint(1, max_power)
#        factor_good_bad = -1 if rand_good_bad > good_bad_thresh else factor_good_bad = 1
#        factor_power = fix_power // (random_power**exp_power)
#
#        factor = factor_good_bad * factor_power
#
#        return factor
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

    def update(self):
        """
        Spin or stay.
        """
        if self.spinning:
            self._spin()

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
            print('UBBI')
            self.spins = 0
        else:
            rotation_angle = 51.43 * self.spins + self.spinning
            self.image = pygame.transform.rotate(self.initial_image, rotation_angle)
            print(self.spins)

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
        self.rect.center = (WIDTH*0.5, HEIGHT*0.5)
        #sprites.add(self, layer=self.layer)


class Graph(BaseSprite):
    """
    A graph showing number of people that are infected.
    """
    pass


class Decrees(BaseSprite):
    """
    A table to show all the decrees in action.
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
        #self.background.fill((250, 250, 250))
        #self.background.fill((0, 0, 0, 250))
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
                #elif event.key == K_ENTER:
                    #pass


    def render(self):
        """
        """
        pass

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
            self.sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

