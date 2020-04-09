import pygame
import random
import pprint

#from .sprite import Delete
from .locals import *

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

    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont('Monospace', 30, True)
        self.delete_buttons = {}
        self.selected_decree_index = ()


        self.decrees = [[[' '.join((dec1, dec2, dec3)) for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]
        self.valid_decrees = [[['' for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]
        self.factors = [[[self.get_factor() for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]
        self.journal = []

        for j in range(7):
            for k in range(7):
                self.factors[2][j][k]=-self.factors[1][j][k]
                self.factors[4][j][k]=-self.factors[3][j][k]
                self.factors[6][j][k]=-self.factors[5][j][k]

        #pprint.pprint(self.factors)
        self.decrees_font = pygame.font.SysFont('Monospace', 12)
        self.selected_decrees_font = pygame.font.SysFont('Monospace', 12, bold=True)

    def print_decs(self):
        pprint.pprint(self.decrees)
        print(self.w1_decs)

    def add_valid_decree(self, decree_index):
        """
        Given a decree index touple it will add the corresponding decree to a list.
        """
        corrected_index = [0 for i in range(len(decree_index))]
        for i in range(len(decree_index)):
            corrected_index[i] = decree_index[i]
            if corrected_index[i] < 0: 
                corrected_index[i] += 7
            elif corrected_index[i] > 6: 
                corrected_index[i] -= 7

        if self.valid_decrees[corrected_index[0]][corrected_index[1]][corrected_index[2]]:
            return False
        #return self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]]
        self.valid_decrees[corrected_index[0]][corrected_index[1]][corrected_index[2]] = self.decrees[corrected_index[0]][corrected_index[1]][corrected_index[2]]
        self.journal.append(tuple(corrected_index))
        return True

    def delete_valid_decree(self, decree_index):
        """
        Given a decree index touple it will delete the corresponding decree to a list.
        """
        if self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]]:
            self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]] = ''
            self.journal.remove(decree_index)
            return True
        return False

    def print_valid_decrees(self):
        #pprint.pprint(self.valid_decrees)
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        print(self.valid_decrees[i][j][k])

    def get_valid_decrees(self):
        """
        Returns all the currently valid decrees in a dictionary where keys are the tuple indeces and the values are the decrees.
        """
        #pprint.pprint(self.valid_decrees)
        valid_decs = []
        valid_indeces = []
        valid_index2decs = {}
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_index2decs[(i,j,k)] = self.valid_decrees[i][j][k]
        return valid_index2decs

    def get_valid_indeces(self):
        """
        Get all inceces that correspond to valid decrees.
        """
        valid_indeces = []
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_indeces.append((i,j,k))
        return valid_indeces

    def get_factor(self): 
        """
        Calculate factors which are then used to calculate the number of sick people.
        """
        max_power = 10.0
        fix_power = 2.5
        exp_power = 1.5
        max_good_bad = 10.0
        good_bad_thresh = 4.0

        rand_good_bad = float(random.randint(1, max_good_bad))
        rand_power = float(random.randint(1, max_power))
        factor_good_bad = -1.0 if (rand_good_bad > good_bad_thresh) else  1.0
        factor_power = float(fix_power / (rand_power**exp_power))

        factor = float(factor_good_bad * factor_power)

        return factor

    def update_decrees_text(self):
        """
        Update and blit the text showing the current valid decrees.
        """
        valid_decrees = 'Decreti\n'
        #valid_decrees += self.decrees.get_valid_decrees_str()
        textsurface = self.title_font.render('Decreti', False, color['GREY'])
        text_x, text_y = DECREES_TEXT_POSITION
        #text_x, text_y = WIDTH*0.58, HEIGHT*0.1
        self.screen.blit(textsurface,(text_x, text_y))
        word_width, word_height = textsurface.get_size()

        text_y += word_height

        for dec_i in self.journal:
            dec = self.get_valid_decree(dec_i)
            
            #Do actual text
            dec_textsurface = self.decrees_font.render(dec, False, color['GREY'])
            if self.selected_decree_index == dec_i:
                dec_textsurface = self.selected_decrees_font.render(dec, False, color['RED'])

            self.screen.blit(dec_textsurface,(text_x, text_y))
            #Do delete buttons
            button_width, button_height = dec_textsurface.get_size()
            #button_height = word_height 
            self.delete_buttons[dec_i] = pygame.Rect((text_x, text_y-button_height/2.0), (button_width, button_height))
            text_y += button_height*DECREES_TEXT_SPACING

    def get_decree_index(self, decree):
        """
        Given a decree get its touple index.
        """
        pass

    def get_valid_decree(self, index):
        """
        Return a valid decree given a valid touple index
        """
        return self.valid_decrees[index[0]][index[1]][index[2]]
