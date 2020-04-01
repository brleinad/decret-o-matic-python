import pygame
import random
import pprint

#from .sprite import Delete
from .constants import *

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

        self.decrees = [[[' '.join((dec1, dec2, dec3)) for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        self.valid_decrees = [[['' for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        self.factors = [[[self.get_factor() for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        pprint.pprint(self.factors)
        self.decrees_font = pygame.font.SysFont('Monospace', 12)

    def print_decs(self):
        pprint.pprint(self.decrees)
        print(self.w1_decs)

    def add_valid_decree(self, decree_index):
        """
        Given a decree index touple it will add the corresponding decree to a list.
        """
        if self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]]:
            return False
        #return self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]]
        self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]] = \
            self.decrees[decree_index[0]][decree_index[1]][decree_index[2]]
        return True

    def delete_valid_decree(self, decree_index):
        """
        Given a decree index touple it will delete the corresponding decree to a list.
        """
        if self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]]:
            self.valid_decrees[decree_index[0]][decree_index[1]][decree_index[2]] = ''
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
        #pprint.pprint(self.valid_decrees)
        valid_decs = []
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_decs.append(self.valid_decrees[i][j][k])
        return valid_decs

    def get_valid_indeces(self):
        valid_indeces = []
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_indeces.append((i,j,k))
        return valid_indeces

    def get_factor(self): 

        max_power = 10.0
        fix_power = 4.0
        exp_power = 1.3
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
        text_x, text_y = WIDTH*0.58, HEIGHT*0.1
        self.screen.blit(textsurface,(text_x, text_y))

        word_width, word_height = textsurface.get_size()

        for dec in self.get_valid_decrees():
            dec_textsurface = self.decrees_font.render(dec, False, color['GREY'])
            text_y += word_height
            self.screen.blit(dec_textsurface,(text_x, text_y))
            #delete_sprite()


