import time
import pygame
import os
from pygame.locals import RLEACCEL

WIDTH = 1000
HEIGHT = 600
SCALE_FACTOR = 2.5 #for imagees that are too big
#sprites = pygame.sprite.LayeredUpdates()

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


class Wheel(BaseSprite):
    """
    Generic class to represent the three wheels.
    """
    layer = 1
    def __init__(self, image, position = (0, 0)):
        BaseSprite.__init__(self)
        self.image, self.rect = self.load_image(image, -1)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()

        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]//SCALE_FACTOR), int(self.size[1]//SCALE_FACTOR)))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = position
        print(self.rect.center)

    def update(self):
        """
        Spin or stay.
        """
        pass

    def spin(self):
        """
        Spin the wheel.
        """
        pass


class Mask(BaseSprite):
    """
    """
    layer = 2
    def __init__(self):
        BaseSprite.__init__(self)
        self.image, self.rect = self.load_image('mask.png', -1)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]//SCALE_FACTOR), int(self.size[1]//SCALE_FACTOR)))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH*0.5, HEIGHT*0.5)
        #sprites.add(self, layer=self.layer)


class UserInterface(BaseSprite):
    """
    The main user interface holding three wheels and the button to create a new decree.
    """
    def __init__(self):
        w1 = Wheel('w1.png')
        w2 = Wheel('w2.png')
        w3 = Wheel('w3.png')

    def update(self):
        """
        """
        pass


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
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        print(pygame.display.Info())

        mask = Mask()
        mask_width, mask_height = mask.size

        mask_topleft_x, mask_topleft_y =  mask.rect.topleft

        w1_x = mask_topleft_x + mask_width * 0.0721
        w1_y = mask_topleft_y + mask_width * 0.1528

        w2_x = mask_topleft_x + mask_width * 0.3099
        w2_y = mask_topleft_y + mask_width * 0.3073

        w3_x = mask_topleft_x + mask_width * 0.6558
        w3_y = mask_topleft_y + mask_width * 0.1556

        w1 = Wheel('w1.png', (w1_x, w1_y))
        w2 = Wheel('w2.png', (w2_x, w2_y))
        w3 = Wheel('w3.png', (w3_x, w3_y))

        
        self.allsprites = pygame.sprite.RenderPlain((mask, w1, w2, w3))
        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(mask, layer = 4)
        self.sprites.add(w1, layer = 3)
        self.sprites.add(w2, layer = 2)
        self.sprites.add(w3, layer = 1)
        
    def events(self, events):
        """
        Standard even loop.
        """

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

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
            #self.tick(dt)
            self.render()
            events = pygame.event.get()
            self.events(events)

            #self.allsprites.update()
            self.screen.blit(self.background, (0, 0))
            #self.allsprites.draw(self.screen)
            self.sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

