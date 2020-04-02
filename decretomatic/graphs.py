import pygame
import matplotlib
import matplotlib.pyplot as pyplot
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

from .sprites import BaseSprite
from .future_gui import LineBorder

class Graph(BaseSprite):
    """
    A graph showing number of people that are infected.
    """
    sick_ppls = []
    days = []

    def __init__(self, sick_peoples, days):
        self.sick_ppls = sick_peoples
        self.days = days

        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.update()

    def update(self):
        #pyplot.plot(days, sick_ppl) 
        #pyplot.xlabel('Giorni') 
        #pyplot.ylabel('Malati') 
        #plt.title('') 
        #plt.show()

        #self.sick_ppls.append(self.sick_ppl)
        #self.days.append(self.day)

        fig = pylab.figure(figsize=[4, 2], # Inches
                           dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        print('Plotting')
        print(self.days)
        print(self.sick_ppls)
        ax.plot(self.days, self.sick_ppls)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        size = canvas.get_width_height()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        self.surf = pygame.image.fromstring(raw_data, size, "RGB")


class LineGraph(LineBorder):
    """
    Cool graph to show total number of sick people.
    """
    def __init__(self, screen, position, width, height):
        LineBorder.__init__(screen, position, width, height, False, (0, 180, 220))

    #def update(self):
    #    pass



class BarGraph(BaseSprite):
    """
    Cool graph to show number of sick people increase per day.
    """
    pass
