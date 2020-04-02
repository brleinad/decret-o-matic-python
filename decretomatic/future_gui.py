import pygame
import numpy
import random 

WIDTH = 1200
HEIGHT = 800
BLACK = (0, 0, 0)


class Widget():

    events_table = []

    def __init__(self, screen):
        self.screen = screen
    
    def handle_event(self, event):
        if event.type in self.events_table:
            for func in self.events_table[event.type]:
                if func(event) == False:
                    break

    def draw(self, surface):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        pass
        
    def draw_border(self, surface, rect, color, border=True, corners=True, other=False):
        
        left, top,  = 0, 0
        width, height = rect.size
        right, bottom = width-1, height-1

        color2 = tuple(x*50//100 for x in color)

        # --- border ---
        
        if border:
            thickness = border
            if border is True:
                thickness = 1
                
            pygame.draw.rect(surface, color2, (left, top, right+1, bottom+1), thickness) 

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


class MovableWidget(Widget):

    redrawing = False
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                if event.button == 1:
                    if self.movable:
                        self.moving = True
                        self.redrawing = True
                        return True
                elif event.button == 3:
                    print(self.rect.topleft)
                    return True
                    
        if event.type == pygame.MOUSEBUTTONUP:
            
            if self.hover:
                if self.movable and self.moving:
                    self.moving = False
                    self.redrawing = True
                    return True

        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            
            if self.movable and self.moving:
                self.rect.move_ip(event.rel)
                self.border_rect.move_ip(event.rel)
                self.redrawing = True
                return True

    def draw(self, surface):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.border, self.border_rect)


class Rectangle(MovableWidget):
    
    def __init__(self, screen, x, y, width, height, movable=False, color=(0, 100, 255), fill=(0,0,0,128), grid=False):
        MovableWidget.__init__(self, screen)
        self.hover = False
        self.moving = False

        self.movable = movable
        self.color = color
        self.fill = fill
        
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill(fill)
        
        # --- grid ---
        
        if grid:
            for j in range(0, width, 30):
                pygame.draw.line(self.image, (255,255,255,16), (j, 0), (j, height))

            for j in range(0, height, 30):
                pygame.draw.line(self.image, (255,255,255,16), (0, j), (width, j))

            for j in range(0, height, 30):
                for i in range(0, width, 30):
                    pygame.draw.rect(self.image, (255,255,255,24), (i-1, j-1, 3, 3))
        
        # --- boder ---
        
        self.border_rect = pygame.Rect(x, y, width, height)
        self.border = pygame.Surface( self.border_rect.size ).convert_alpha()
        self.border.fill((0,0,0,0))
        self.draw_border(self.border, self.border_rect, self.color, False, 1, False)


class LineBorder(MovableWidget):
    
    def __init__(self, screen, x, y, width, height, movable=False, color=(0, 100, 255), fill=(0,0,0,128)):
        MovableWidget.__init__(self, screen)
        self.hover = False
        self.moving = False

        self.movable = movable
        self.color = color
        self.fill = fill
        
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill(fill)
        
        # --- object ---

        self.points = []
        for _ in range(15, width-15, 10):
            self.points.append(random.randint(5, height-30))
        
        self.draw_bars(self.image, self.rect)
        
        # --- boder ---
 
        self.border_rect = pygame.Rect(x, y, width, height)
        self.border = pygame.Surface( self.border_rect.size ).convert_alpha()
        self.border.fill((0,0,0,0))
        self.draw_border(self.border, self.border_rect, self.color, True, 3, False)
        
        self.anim_deltatime = 250
        self.anim_time = pygame.time.get_ticks() + self.anim_deltatime

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

    def draw_bars(self, surface, rect):
        #pygame.draw.rect(surface, 
        width, height = rect.size
        
        color1 = self.color
        color2 = (0, 80, 110, 128)
        
        for x, size in zip(range(15, width-15, 10), self.points):
            pygame.draw.rect(surface, color2, (x, 15, 5, height-30), 0) 
            pygame.draw.rect(surface, color1, (x, 15+size, 5, height-30-size), 0) 

    def update(self):
        
        time = pygame.time.get_ticks()
        
        if time >= self.anim_time:
            self.draw_bars(self.image, self.rect)
            
            self.points.pop(0)
            self.points.append(random.randint(5, self.rect.height-30))

            self.anim_time = time + self.anim_deltatime
            self.redrawing = True            

class BarBorder(MovableWidget):
    
    def __init__(self, screen, x, y, width, height, movable=False, color=(0, 100, 255), fill=(0,0,0,128)):
        MovableWidget.__init__(self, screen)
        self.hover = False
        self.moving = False

        self.movable = movable
        self.color = color
        self.fill = fill
        
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height)).convert_alpha()
        self.image.fill(fill)
        
        # --- object ---

        self.points = []
        for _ in range(25, width-15, 50):
            self.points.append(random.randint(5, height-30))
        
        self.draw_bars(self.image, self.rect)
        
        # --- boder ---
 
        self.border_rect = pygame.Rect(x, y, width, height)
        self.border = pygame.Surface( self.border_rect.size ).convert_alpha()
        self.border.fill((0,0,0,0))
        self.draw_border(self.border, self.border_rect, self.color, True, 3, False)
        
        self.anim_deltatime = 250
        self.anim_time = pygame.time.get_ticks() + self.anim_deltatime

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
            
            print(left)
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

    def draw_bars(self, surface, rect):
        #pygame.draw.rect(surface, 
        width, height = rect.size
        
        color1 = self.color
        color2 = (0, 80, 110, 128)
        color3 = (255, 190, 50, 255)
        
        points = []
        
        for x, size in zip(range(25, width-15, 50), self.points):
            points.append( (x, size) )
            
        import pygame.gfxdraw
        
        for p1, p2 in zip(points, points[1:]):
            pygame.gfxdraw.line(surface, *p1, *p2, color2)
        
        for x, y in points:
            pygame.draw.rect(surface, color3, (x-2, y-2, 4, 4), 0) 
            #pygame.gfxdraw.circle(surface, color1, (x, y), 10, 1) 
            pygame.gfxdraw.aacircle(surface, x, y, 10, color1) 
            

    def update(self):
        
        time = pygame.time.get_ticks()
        
        if time >= self.anim_time:
            self.draw_bars(self.image, self.rect)
            
            #self.points.pop(0)
            #self.points.append(random.randint(5, self.rect.height-30))

            self.anim_time = time + self.anim_deltatime
            self.redrawing = True            

# --------------------------------------------------------------------


class FutureGUI():

    def on_quit(self, event):
        self.running = False

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False

    def on_draw(self, event=None):
        #screen.fill(BLACK)
        for w in self.widgets:
            w.draw(self.screen)
        
        #pygame.display.flip()
        pygame.display.update()

    events_table = {
        pygame.QUIT: [on_quit],
        pygame.KEYDOWN: [on_keydown],
    }

    def __init__(self):
        pygame.init()
        pygame.mixer.quit()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        font_monospace_20 = pygame.font.SysFont('Monospace', 20, True)
        self.running = True
        self.redrawing = True

# --- background ---
        self.widgets = [
            Rectangle(self.screen, 0, 0, WIDTH, HEIGHT, False, (100, 255,0), fill=(255,255,255,0), grid=True),
        ]
        self.widgets.append(LineBorder(self.screen, 20, 200, 305, 200, True, (0, 180, 220)))
        self.widgets.append(BarBorder(self.screen, 325, 200, 305, 200, True, (0, 180, 220)))
        self.widgets.append(LineBorder(self.screen, 325, 400, 305, 200, True, (0, 180, 220)))
        self.widgets.append(BarBorder(self.screen, 20, 400, 305, 200, True, (0, 180, 220)))


    def is_redrawing(self):
        for w in self.widgets:
            if w.redrawing:
                return True
        return self.redrawing

    def stop_redrawing(self):
        for w in self.widgets:
            w.redrawing = False

    def mainloop(self):

        while self.running:

            for event in pygame.event.get():
                if event.type in self.events_table:
                    for func in self.events_table[event.type]:
                        if func(event) == True:
                            break
                for w in reversed(self.widgets):
                    if w.handle_event(event) == True:
                        break
                    
            for w in self.widgets:
                w.update()
                
            if self.is_redrawing():
                self.screen.fill(BLACK)
                self.on_draw()
                self.redrawing = False
                self.stop_redrawing()
            self.clock.tick(25)
            
        pygame.quit()


if __name__ == '__main__':
    FutureGUI().mainloop()
