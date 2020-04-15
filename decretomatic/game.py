import time
import random
import pygame
import os
import sys
sys.path.insert(1, os.path.join(os.getcwd(), 'pygame-menu'))
import pygameMenu

from pygame.locals import *
from .locals import *
from .sprites import Wheel, Mask, Bin
from .graphs import LineGraph, BarGraph
from .decrees import Decrees
from .people import People

#TODOs: 
#max number of decrees
#make decree list pretty
#create an exe
#Tell user when:
##decree has already been created
##decrees cannot be deleted anymore
##Make it more obvious when the days pass
#highlight buttons when mouse hovers 
#variable scale on the line graph
#improve menu
#Change fonts

LEFT_MOUSEBUTTON = 1
RIGHT_MOUSEBUTTON = 3


class Game():
    """
    The main class instantiating all the sprite, controlling all the events, etc.
    """
    FLAGS = 0
    FPS = 30

    game_over = False
    game_lost = False
    isday_selected = False
    w1_selected = False
    w2_selected = False
    w3_selected = False

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

        self.do_delete = False
        self.day = 1
        self.days = [self.day,]
        self.sick_ppls = [1,]
        self.new_sick_ppls = [0,]
        #print(pygame.display.Info())

        self.decrees = Decrees(self.screen)
        self.people = People(self.screen, self.decrees)

        self.make_sprites()

        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.mask, layer = 4)
        self.sprites.add(self.w1, layer = 3)
        self.sprites.add(self.w2, layer = 2)
        self.sprites.add(self.w3, layer = 1)
        self.sprites.add(self.w3, layer = 1)
        self.sprites.add(self.bin, layer = 1)
        self.sprites.add(self.line_graph_lin, layer = 4)
        self.sprites.add(self.line_graph_log, layer = 4)
        #self.sprites.add(self.graph, layer = 1)

        self.title_font = pygame.font.SysFont('Monospace', 30, True)
        textsurface = self.title_font.render('Decreti', False, (150, 150, 150))
        self.screen.blit(textsurface,(WIDTH*0.8,HEIGHT*0.1))

        self.actions = 0
        self.day_button_rect = pygame.Rect(DAY_BUTTON_POSITION, DAY_BUTTON_SIZE)

        self.make_menu()

    def make_sprites(self):
        self.bin = Bin((WIDTH*0.9, HEIGHT*0.9))
        self.mask = Mask((WIDTH*MASK_POS_X, HEIGHT*MASK_POS_Y), self.decrees.journal)
        self.line_graph_lin = LineGraph(self.sick_ppls, self.days, WIDTH*0.05,HEIGHT*0.7,0)
        self.line_graph_log = LineGraph(self.sick_ppls, self.days, WIDTH*0.3,HEIGHT*0.7,1)
        self.make_wheels()

    def make_wheels(self):
        """Create all the wheel sprites."""
        mask_topleft_x, mask_topleft_y =  self.mask.rect.topleft
        mask_width, mask_height = self.mask.size

        w1_x = mask_topleft_x + mask_width * 0.0721
        w1_y = mask_topleft_y + mask_width * 0.1528

        w2_x = mask_topleft_x + mask_width * 0.3099
        w2_y = mask_topleft_y + mask_width * 0.3073

        w3_x = mask_topleft_x + mask_width * 0.6558
        w3_y = mask_topleft_y + mask_width * 0.1556

        #Button positions are relative to the mask
        #oM: (255, 237) -> (227, 173)
        #W1: (255, 237) -> (278, 232)
        self.w1_button_pos = (mask_topleft_x + 51, mask_topleft_y + 59)
        #W2: (362, 307) -> (384, 301)
        self.w2_button_pos = (mask_topleft_x + 157, mask_topleft_y + 128)
        #W3: (518, 239) -> (540, 231)
        self.w3_button_pos = (mask_topleft_x + 313, mask_topleft_y + 60)

        self.w1 = Wheel('w1_t.png', (w1_x, w1_y), self.w1_button_pos)
        self.w2 = Wheel('w2_t.png', (w2_x, w2_y), self.w2_button_pos)
        self.w3 = Wheel('w3_t.png', (w3_x, w3_y), self.w3_button_pos)

    def make_menu(self):
        """Create the main game menu"""
        menu_config = {}
        menu_config['menu_width'] =  WIDTH
        menu_config['menu_height'] = HEIGHT
        menu_config['font'] = 'Monospace' #self.title_font
        menu_config['title'] = 'Decret-O-Matic'
        menu_config['mouse_enabled'] = True
        menu_config['onclose'] = pygameMenu.events.CLOSE
        self.menu = pygameMenu.Menu(**menu_config)
        for tutorial in TUTORIALS:
            self.menu.add_label(tutorial, max_char=100, font_size=18)
        self.menu.add_button('Gioca', pygameMenu.events.CLOSE)

    def make_end_menu(self):
        """Create the menu displayed at the end of the game"""
        end_menu_config = {}
        end_menu_config['title'] = 'Hai Perso' if self.game_lost else 'Hai Vinto!'
        end_menu_config['font'] = 'Monospace' #self.title_font
        end_menu_config['mouse_enabled'] = True
        end_menu_config['onclose'] = pygameMenu.events.CLOSE
        end_menu_config['menu_width'] = WIDTH * 0.8
        end_menu_config['menu_height'] = HEIGHT * 0.5
        self.end_menu = pygameMenu.Menu(**end_menu_config)
        for credit in CREDITS:
            self.end_menu.add_label(credit, max_char=80, font_size=18)
        self.end_menu.add_button('Gioca di Nuovo', self.__init__)

    def update_day(self):
        self.day_textsurface = self.title_font.render(f'Giorno: {self.day} Azioni: {self.actions}/{MAX_ACTIONS}', False, color['GREY'])
        
    def update_decrees(self):
        """
        Update the list of valid decrees made by the player.
        """
        updated = False
        decree_index = (
                self.w1.decree_index, 
                self.w2.decree_index, 
                self.w3.decree_index)
        #print('index')
        #print(decree_index)
        if self.decrees.get_num_valid_decrees() < MAX_NUM_DECREES:
            if self.decrees.add_valid_decree(decree_index):
                self.actions += 1
                self.decrees.update_decrees_text()
                updated = True
        if self.actions >= MAX_ACTIONS:
            self.actions = 0
            self.next_day()
        return updated

    def events(self, events):
        """
        Standard event loop.
        """

        for event in events:
            #if event.type == pygameMenu.events.EXIT:
                #self.menu.disable()
            if event.type == pygame.QUIT:
                self.running = False
            # Keyboard keys: not really used in gameplay, only for debugging
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
            # Mouse hovering stuff
            elif event.type == MOUSEMOTION:
                if self.bin.rect.collidepoint(event.pos):
                    self.bin.open_bin()
                elif self.mask.button_rect.collidepoint(event.pos):
                    #self.mask.activate()
                    pass
                elif self.day_button_rect.collidepoint(event.pos):
                    self.isday_selected = True
                elif self.w1.button_rect.collidepoint(event.pos):
                    self.w1_selected = True
                elif self.w2.button_rect.collidepoint(event.pos):
                    self.w2_selected = True
                elif self.w3.button_rect.collidepoint(event.pos):
                    self.w3_selected = True
                else:
                    self.mask.active = False
                    self.bin.close_bin()
                    self.isday_selected = False
                    self.w1_selected = False
                    self.w2_selected = False
                    self.w3_selected = False
            # Mouse clicking
            elif event.type == MOUSEBUTTONDOWN:
                print(f'Mouse at {event.pos}')
                if self.w1.button_rect.collidepoint(event.pos):
                    if event.button == LEFT_MOUSEBUTTON: 
                        self.w1.next_decree()
                    elif event.button == RIGHT_MOUSEBUTTON: 
                        self.w1.prev_decree()
                elif self.w2.button_rect.collidepoint(event.pos):
                    if event.button == LEFT_MOUSEBUTTON: 
                        self.w2.next_decree()
                    elif event.button == RIGHT_MOUSEBUTTON: 
                        self.w2.prev_decree()
                elif self.w3.button_rect.collidepoint(event.pos):
                    if event.button == LEFT_MOUSEBUTTON: 
                        self.w3.next_decree()
                    elif event.button == RIGHT_MOUSEBUTTON: 
                        self.w3.prev_decree()
                elif self.mask.button_rect.collidepoint(event.pos):
                    if self.update_decrees(): 
                        self.mask.active = True
                elif self.day_button_rect.collidepoint(event.pos):
                    self.next_day()
                elif self.bin.rect.collidepoint(event.pos):
                    if self.do_delete:
                        self.decrees.delete_valid_decree(self.decree2delete_index)
                        self.do_delete = False
                        self.actions += 2
                        self.decrees.selected_decree_index = ()
                        if self.actions >= MAX_ACTIONS:
                            self.actions = 0
                            self.next_day()
                else:
                    for decree_index, delete_button in self.decrees.delete_buttons.items():
                        if delete_button.collidepoint(event.pos) and (self.actions<=MAX_ACTIONS-2 or self.do_delete):
                            #self.decrees.delete_decree(decree_index)
                            if self.decrees.selected_decree_index==decree_index:
                                self.do_delete =  0
                                self.decree2delete_index = -1
                                self.decrees.selected_decree_index = -1
                            else:
                                self.do_delete = 1
                                self.decree2delete_index = decree_index
                                self.decrees.selected_decree_index = decree_index

    def render(self):
        """
        Do all the rendering and displaying of sprites and what not.
        """
        self.screen.blit(self.background, (0, 0))
        self.sprites.draw(self.screen)
        self.draw_buttons()
        self.screen.blit(self.day_textsurface, DAY_BUTTON_POSITION)
        self.screen.blit(self.people.ppl_textsurface,PEOPLE_TEXT_POSITION)
        self.decrees.update_decrees_text()

    def draw_buttons(self):
        """Draw all the buttons"""

        #pygame.draw.rect(self.screen, color['RED'], (DAY_BUTTON_POSITION, DAY_BUTTON_SIZE), 1) # The not is to get the desired look

        if self.isday_selected:
                self.day_textsurface = self.title_font.render(f'Giorno: {self.day} Azioni: {self.actions}/{MAX_ACTIONS}', True, color['RED'])

        if self.w1_selected:
            pygame.draw.rect(self.screen, color['RED'], (self.w1_button_pos, WHEEL_BUTTON_SIZE_1), 1)
        if self.w2_selected:
            pygame.draw.rect(self.screen, color['RED'], (self.w2_button_pos, WHEEL_BUTTON_SIZE_2), 1)
        if self.w3_selected:
            pygame.draw.rect(self.screen, color['RED'], (self.w3_button_pos, WHEEL_BUTTON_SIZE_3), 1)

    def next_day(self):
        """
        Advance the game to the next day.
        """
        self.day += 1
        self.actions=0
        self.days.append(self.day)
        #self.people.update_sick(self.decrees)
        self.people.update_sick()
        self.sick_ppls.append(self.people.get_sick_people())
        self.decree2delete_index = -1
        self.decrees.selected_decree_index = -1

        if self.day == LAST_DAY:
            if self.sick_ppls[-1] > MAX_SICK_PPL:
                self.game_over = True
                self.game_lost = True
        if self.sick_ppls[-1] > MAX_SICK_PPL:
            self.game_over = True
            self.game_lost = True
        if self.day == LAST_DAY:
            self.game_over = True
            self.game_lost = False

    def get_day(self):
        return self.day

    def mainloop(self):
        """
        Handle the game main loop until player stops playing.
        """

        while self.running:
            self.clock.tick(self.FPS)
            fs = time.time()
            events = pygame.event.get()

            if self.menu.is_enabled(): 
                #self.menu.mainloop(self.screen) #events)
                self.menu.draw(self.screen)
                self.menu.update(events)
            else:
                self.events(events)
                self.sprites.update()
                self.people.update()
                self.update_day()
                self.render()

                if self.game_over:
                    #self.end_menu_title = 'Hai Perso' if self.game_lost else 'Hai Vinto!'
                    self.make_end_menu()
                    self.menu = self.end_menu
                    self.game_over = False
                    self.game_lost = False

            pygame.display.flip()

        pygame.quit()

