import random
import pprint

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

        self.factors = [[[self.get_factor() for dec3 in self.w3_decs] for dec2 in self.w2_decs] for dec1 in self.w1_decs]

        pprint.pprint(self.factors)

    def print_decs(self):
        pprint.pprint(self.decrees)
        print(self.w1_decs)

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

    def get_valid_indeces(self):
        valid_indeces = []
        for i in range(len(self.valid_decrees)):
            for j in range(len(self.valid_decrees[i])):
                for k in range(len(self.valid_decrees[j])):
                    if self.valid_decrees[i][j][k]:
                        valid_indeces.append((i,j,k))
        return valid_indeces

    def get_factor(self): 
        standard_factor = 2 + random.randint(0,10)*0.1

        max_power = 10
        fix_power = 3
        exp_power = 1.2
        max_good_bad = 10
        good_bad_thresh = 6

        rand_good_bad = random.randint(1, max_good_bad)
        rand_power = random.randint(1, max_power)
        factor_good_bad = -1 if (rand_good_bad > good_bad_thresh) else  1
        factor_power = fix_power // (rand_power**exp_power)

        factor = factor_good_bad * factor_power

        return factor
