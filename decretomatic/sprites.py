import pygame
import os
from pygame.locals import RLEACCEL
from .locals import *


SCALE_FACTOR = 1 #2.5 #for imagees that are too big
TRANSPARENT = (1, 0, 0)
WHEEL_NUM_OPTIONS = 7
MASK_BUTTON_POSITION = (229, 365)
MASK_BUTTON_HEIGHT = 50
BIN_SIZE = (30, 35)
CLOCKWISE = 1
ANTICLOCKWISE = -1
SPIN_ANGLE = 4


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

        self.button_rect = pygame.Rect((button_position), WHEEL_BUTTON_SIZE)
        self.button_rect.topleft = button_position

        self.sprites_image, self.sprites_rect = self.load_image(image, TRANSPARENT)

        left = self.sprites_rect.left
        top = self.sprites_rect.top
        width = self.sprites_rect.width / WHEEL_NUM_OPTIONS
        height = self.sprites_rect.height


        self.images = [None for i in range(WHEEL_NUM_OPTIONS)]
        self.images[0] = self.sprites_image.subsurface(left, top, width, height)
        left = self.sprites_rect.width - width #UBBI ha fatto lo sprite al contrario
        for i in range(1, WHEEL_NUM_OPTIONS):
            self.images[i] = self.sprites_image.subsurface(left, top, width, height)
            left -= width

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.size = self.image.get_size()
        self.rect.center = position
        self.position = position

        self.spinning = 0
        self.spins = 0
        self.initial_image = self.image.copy()
        self.decree_index = 0

    def update(self):
        """
        Spin or stay.
        """
        self.decree_index = self.spins
        if self.spinning >= 1:
            self._spin(CLOCKWISE)
        elif self.spinning <= -1:
            self._spin(ANTICLOCKWISE)

    def _update_image(self):
        """
        Set the image from the sprite sheet.
        """
        index=self.spins
        if index<0: index+=7
        if index>6: index-=7
        self.image = self.images[index] #self.decree_index]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        print('Updated image')

    def _spin(self, direction):
        """
        Spin the wheelclockwise.
        """
        center = self.rect.center
        self.spinning += SPIN_ANGLE * direction

        #finished_spinning = True
        if direction == CLOCKWISE:
            finished_spinning = self.spinning >  360.0/WHEEL_NUM_OPTIONS
        elif direction == ANTICLOCKWISE:
            finished_spinning = self.spinning < -360.0/WHEEL_NUM_OPTIONS

        if finished_spinning:
            self.spinning = 0
            self.spins += direction
            if self.spins > WHEEL_NUM_OPTIONS - 1:
                self.spins = 0
            self._update_image()
        else:
            rotation_angle = 360.0/WHEEL_NUM_OPTIONS * self.spins + self.spinning
            self.image = pygame.transform.rotate(self.initial_image, rotation_angle)
            self.rect = self.image.get_rect(center = center)
            self.rect.center = center

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
    def __init__(self, position, valid_decrees):
        BaseSprite.__init__(self)
        self.valid_decrees = valid_decrees
        self.images['active'], self.rect = self.load_image('mask_z_click.png', TRANSPARENT)
        self.images['nonactive'], self.rect = self.load_image('mask_z.png', TRANSPARENT)
        self.images['overload'], self.rect = self.load_image('mask_ko.png', TRANSPARENT)
        self.image = self.images['nonactive']
        self.size = self.image.get_size()
        self.rect.center = position
        self.button_rect = pygame.Rect(MASK_BUTTON_POSITION, (self.rect.width, MASK_BUTTON_HEIGHT))

        self.active = False
        self.active_counter = 0

    def update(self): #, active = False, num_decrees = 0):
        if len(self.valid_decrees) <  MAX_NUM_DECREES:
            if self.active:
                self.activate()
            else:
                self.deactivate()
        else:
            self.overload()

    def activate(self):
        self.image = self.images['active']
        self.active = True

    def deactivate(self):
        self.image = self.images['nonactive']
        self.active = False

    def overload(self):
        self.image = self.images['overload']
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

        width, height = BIN_SIZE
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
