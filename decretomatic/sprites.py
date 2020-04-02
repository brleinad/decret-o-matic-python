import pygame
import os
from pygame.locals import RLEACCEL


SCALE_FACTOR = 1 #2.5 #for imagees that are too big
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

class Wheel(BaseSprite):
    """
    Generic class to represent the three wheels.
    """
    layer = 1
    def __init__(self, image, position = (0, 0), button_position = (0, 0)):
        self.image_name = image
        BaseSprite.__init__(self)

#W1: (255, 237) -> (278, 232)
#W1: (255, 237) -> (277, 247)
#W1: (255, 237) -> (375, 231)
#W1: (255, 237) -> (375, 247)
        button_width = 100
        button_height = 40
        self.button_rect = pygame.Rect((button_position), (button_width, button_height))
        self.button_rect.topleft = button_position

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
        if self.spinning >=1:
            self._spin()
        elif self.spinning <= -1:
            self._aspin()
        self.decree_index = self.spins

    def _spin(self):
        """
        Spin the wheelclockwise.
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

    def _aspin(self):
        """
        Spin the wheel anticlockwise.
        """
        center = self.rect.center
        self.spinning -= 4

        if self.spinning < -51.43:
            self.spinning = 0
            self.spins -= 1

        if self.spins == 0:
            #self.image, self.rect = self.load_image(self.image_name, TRANSPARENT)
            self.image = self.initial_image.copy()
            self.spins = 6
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

    def prev_decree(self):
        """
        This will spin to the prev decree.
        """
        if not self.spinning:
            self.spinning = -1


class Mask(BaseSprite):
    """
    Represents the mask that goes on top of the wheels.
    """
    layer = 2
    def __init__(self, position):
        BaseSprite.__init__(self)
        self.image, self.rect = self.load_image('mask_z.png', TRANSPARENT)
        self.size = self.image.get_size()
        self.rect.center = position
        self.button_rect = pygame.Rect((229,365), (self.rect.width, 50))


class Bin(BaseSprite):
    """
    A simple bin sprite. It will be used to delete decrees.
    """
    def __init__(self, position):
        BaseSprite.__init__(self)
        self.image, self.rect = self.load_image('bin_s.png', TRANSPARENT)
        self.size = self.image.get_size()
        self.rect.center = position



