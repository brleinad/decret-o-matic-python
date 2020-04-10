import os
import sys

if __name__ == '__main__':
    # To get pyinstaller working
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS) 
    from decretomatic.game import Game
    Game().mainloop()

