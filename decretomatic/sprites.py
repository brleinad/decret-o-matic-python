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
    images = {}
    def __init__(self, position):
        BaseSprite.__init__(self)
        self.images['active'], self.rect = self.load_image('mask_z_click.png', TRANSPARENT)
        self.images['nonactive'], self.rect = self.load_image('mask_z.png', TRANSPARENT)
        self.image = self.images['nonactive']
        self.size = self.image.get_size()
        self.rect.center = position
        self.button_rect = pygame.Rect((229,365), (self.rect.width, 50))

        self.active = False
        self.active_counter = 0

    def update(self):
        #if self.active:
        #    if self.active_counter > 10:
        #        self.active = False
        #        self.active_counter = 0
        #        self.image = self.images['nonactive']
        #    self.active_counter += 1
        pass

    def activate(self):
        self.image = self.images['active']
        self.active = True

    def deactivate(self):
        self.image = self.images['nonactive']
        self.active = False



class Bin(BaseSprite):
    """
    A simple bin sprite. It will be used to delete decrees.
    """
    images = {}
    def __init__(self, position):
        BaseSprite.__init__(self)
        self.sprite_sheet, self.rect_sheet = self.load_image('bin.png', TRANSPARENT)
        #print(f'BOB BIN SIZE is {self.size}')

        width, height = (30, 35)
        self.images['closed'] = self.sprite_sheet.subsurface(self.rect_sheet.left, self.rect_sheet.top, width, self.rect_sheet.height)
        self.images['open'] = self.sprite_sheet.subsurface(self.rect_sheet.left + width, self.rect_sheet.top, width, self.rect_sheet.height)

        self.image = self.images['closed']
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.center = position

        self.open = False
        self.close_counter = 0

    def update(self):
        #if self.open:
        #    if self.close_counter > 10:
        #        self.open = False
        #        self.close_counter = 0
        #        self.image = self.images['closed']
        #    self.close_counter += 1
        pass

    def open_bin(self):
        self.image = self.images['open']
        self.open = True

    def close_bin(self):
        self.image = self.images['closed']
        self.open = False



