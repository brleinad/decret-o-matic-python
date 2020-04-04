import pygame
import matplotlib
import matplotlib.pyplot as pyplot
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

from .sprites import BaseSprite
from . import future_gui
from .constants import *
import pygame.gfxdraw
from math import log10

class Graph(BaseSprite):
    """
    A graph showing number of people that are infected.
    """
    sick_ppls = []
    days = []

    def __init__(self, sick_peoples, days):
        self.sick_ppls = sick_peoples
        self.days = days

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


class LineGraph(BaseSprite):#, future_gui.LineGraph):
    """
    Cool graph to show total number of sick people.
    """
    def __init__(self, sick_ppls, days, x_pos, y_pos, log):
        BaseSprite.__init__(self)
        #x_pos, y_pos = (WIDTH*0.1,HEIGHT*0.7)
        self.position = (x_pos, x_pos)
        width, height = 305, 200
        #future_gui.LineGraph.__init__(self, screen, position[0], position[1], width, height, movable=False, color=(0, 180, 220))
        #BaseSprite.__init__(self)
        self.sick_ppls = sick_ppls
        self.days = days
        self.log = log
        self.color = (0, 180, 220) #TODO: add all colors here to constants
        fill = (0,0,0,128)
        

        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill(fill)

        self.border_rect = pygame.Rect(x_pos, y_pos, width, height)
        self.border = pygame.Surface( self.border_rect.size ).convert_alpha()
        #self.draw_border(self.border, self.border_rect, self.color, True, 3, False)
        self.draw_border(self.image, self.rect, self.color, True, 3, False)

        self.update()


    def update(self):

        width, height = self.rect.size
        #height*=0.9
		
        color1 = self.color
        color2 = (0, 80, 110, 128)
        color3 = (255, 190, 50, 255)
        color4 = (255, 0, 0, 255)
        
        #for p1, p2 in zip(points, points[1:]):
            #pygame.gfxdraw.line(self.image, *p1, *p2, color2)

        origin_x, origin_y = self.rect.topleft
        
        for i in range(len(self.days)): #range(LAST_DAY):
            #x = origin_x + self.days[i]*width/14
            x_0=0
            dy=height
            if i>0:
                x_0=self.days[i-1]*width/(LAST_DAY+1.)
            if self.log:
                y = height *(1.0 - (log10(self.sick_ppls[i])/log10(MAX_SICK_PPL)))
                y_0=y
                if i>0:
                    y_0=height*(1.0 - (log10(self.sick_ppls[i-1])/log10(MAX_SICK_PPL)))
                    dy=height *(1.0 - (self.sick_ppls[i]-self.sick_ppls[i-1])/(1.6*self.sick_ppls[i-1]))
            else:
                y = height * (1.0 - ((self.sick_ppls[i])/(MAX_SICK_PPL)))
                y_0=y
                if i>0: y_0=height * (1.0 - (self.sick_ppls[i-1])/(MAX_SICK_PPL))
            #dy=height - height*(log10(self.sick_ppls[i]-self.sick_ppls[i-1])/log10(MAX_SICK_PPL*.0005))
            
            x = self.days[i]*width/(LAST_DAY+1.)
			#y = height - height*log10(self.sick_ppls[i]*10/MAX_SICK_PPL)
            #TODO: figure out a better scale
			
			
            x, y, y_0, dy = (int(x), int(0.9*y), int(0.9*y_0), int(0.9*dy))

            pygame.draw.rect(self.image, color3, (x-2, y-2, 4, 4), 0) 
            #pygame.draw.rect(self.image, color3, (self.days[i]-2, self.sick_ppls[i]-2, 4, 4), 0) 
            #pygame.gfxdraw.circle(self.image, color1, (x, y), 10, 1) 
            pygame.gfxdraw.aacircle(self.image, x, y, 10, color1) 
            #pygame.gfxdraw.aacircle(self.image, self.days[i], self.sick_ppls[i], 10, color1) 
            pygame.draw.lines(self.image, color3, False, ((x_0,y_0),(x,y)), 1)
            if self.log and i>0: pygame.draw.rect(self.image, color4, (x-width/(LAST_DAY+1.0)/2, height*0.9, width/(LAST_DAY+1.0), dy), 1) 
            

    def draw_border(self, surface, rect, color, border=True, corners=True, other=False):
        
        left, top = 0, 0
        width, height = rect.size
        right, bottom = width-1, height-1

        color2 = tuple(x*50//100 for x in color)

        # --- border ---
        
        if border:
            thickness = border
            if border is True:
                thickness = 1

            size_x = 50 
            size_y = 50
            
            points = [
                    (left, top), 
                        (left+size_x, top), (left+size_x+5, top+5),
                        (right-size_x-5, top+5), (right-size_x, top), 
                    (right, top),
                        (right, top+size_y), (right-5, top+size_y+5),
                        (right-5, bottom-size_y-5), (right, bottom-size_y), 
                    (right, bottom),
                        (right-size_x, bottom), (right-size_x-5, bottom-5), 
                        (left+size_x+5, bottom-5), (left+size_x, bottom),
                    (left, bottom), 
                         (left, bottom-size_y), (left+5, bottom-size_y-5),
                        (left+5, top+size_y+5), (left, top+size_y), 
                    (left, top), 
                    ]
                      
            pygame.draw.lines(surface, color2, False, points) 

        # --- corners ---

        if corners:
            thickness = corners
            if corners is True:
                thickness = 5
                
            # left top
            pygame.draw.line(surface, color, (left, top), (left+15, top), thickness) 
            pygame.draw.line(surface, color, (left, top), (left, top+15), thickness) 

            # right top
            pygame.draw.line(surface, color, (right, top), (right-15, top), thickness) 
            pygame.draw.line(surface, color, (right, top), (right, top+15), thickness) 

            # right bottom
            pygame.draw.line(surface, color, (right, bottom), (right-15, bottom), thickness) 
            pygame.draw.line(surface, color, (right, bottom), (right, bottom-15), thickness) 

            # left bottom
            pygame.draw.line(surface, color, (left, bottom), (left+15, bottom), thickness) 
            pygame.draw.line(surface, color, (left, bottom), (left, bottom-15), thickness) 

        # --- other ---

        if other:
            points = ( (left+5, top+5), (left+5, top+30), (left+50, top+30), (left+50+10, top+20), (right-5, top+20), (right-5, top+5) )
            
            pygame.draw.polygon(surface, (*color2, 128), points)
            #pygame.draw.polygon(surface, color, points, 1)
            pygame.draw.lines(surface, color, False, points[1:-1], 1)
            

            points = ( (left+5, bottom-5), (left+5, bottom-20), (right-50-10, bottom-20), (right-50, bottom-30), (right-5, bottom-30), (right-5, bottom-5) )
            
            pygame.draw.polygon(surface, (*color2, 128), points)
            #pygame.draw.polygon(surface, color, points, 1)
            pygame.draw.lines(surface, color, False, points[1:-1], 1)




class BarGraph(BaseSprite):
    """
    Cool graph to show number of sick people increase per day.
    """
    pass
