# -*- coding: utf-8 -*-

"""
All the constants of the game
Fact : i use // instead of / to avoid float
"""

from assets.math import Math

# WINDOW
X_SIZE = 1080
Y_SIZE = 720
SCREEN_SIZE = (X_SIZE, Y_SIZE)
X_MID = X_SIZE//2
Y_MID = Y_SIZE//2

MIDDLE = (X_MID, Y_MID)
CENTER = (0, 0)

# FRAME RATE
FPS = 120

# BOARD
# CELLS
R = 32  # radius of the conscript circle that contain the apexes of the hexagon
U = Math.inscribed_rad(R)  # radius of the inscribed circle
MULT = 1.1  # multiply radius by this to get the space between two tiles
# BOARD SIZE
B_W = 540
B_H = 614
BOARD_SIZE = (B_W, B_H)
# BOARD FIRST TILE POS (0, 0)
B_XO = X_MID
B_YO = (Y_SIZE - B_H) // 2 + 1.2 * U
B_O = (B_XO, B_YO)
# BOARD PLACE POSITION (top left rect edge)
B_RECT_POS = (X_MID-B_W//2, Y_MID-B_H//2)

# TEXT POS
CHAT_FONT_SIZE = 18
HEIGHT = Y_MID
TBR = (6 * X_SIZE / 7, HEIGHT)
TBL = (X_SIZE / 7, HEIGHT)

TB_SIZE = (280, 500)
CHAT_POS = (10, TB_SIZE[1]-2*CHAT_FONT_SIZE-10)
INPUT_BOX_SIZE = (TB_SIZE[0], CHAT_FONT_SIZE)

TURN_P = (TB_SIZE[0]/2, TB_SIZE[1]/1.1/2)
PROCESS_P = (TB_SIZE[0]/2, TB_SIZE[1]*1.1/2)

# STOPWATCH POS
CLOCK = {0: (TB_SIZE[0]/2, TB_SIZE[1]*0.3), 1: (TB_SIZE[0]/2, TB_SIZE[1]*0.7)}

# BUTTON POS
G_BUT = {0: [], 1: (TB_SIZE[0]/2, TB_SIZE[1]*0.7)}

# GAME INFOS
GAME_NAME = "Select!"
# JUST TO KNOW WHICH ARE THE DIFFERENT STATES
GAME_STATE = {"choose insect": 0, "choose way": 1}
TURN_STATE = {"white": 0, "black": 1}

# PATHS
ICON = 'assets/other/icon.png'
FONTS = 'assets/fonts'
COLORS_DFLT = 'assets/default textures/colors.txt'
COLORS_CUST = 'assets/textures/colors.txt'
INSECTS = 'assets/default textures/insects/'
SCREENSHOTS = 'assets/screenshots/'

# TEST COLORS_DFLT
BACKGROUND_COLOR = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# TEXT PLACEMENTS
TITLE_POS = (X_MID, Y_SIZE/5)
SUB1_POS = (X_MID, Y_SIZE/3.4)

# TEXTS
SUB1 = "Game made by Valentin Cassayre"

MENU_RADIUS = 100
MENU_UNIT = Math.inscribed_rad(MENU_RADIUS)
MENU_EDGE = 1.1

# LINKS
url = {'github': 'https://github.com/V-def/select-game/', 'website': 'https://valentin.cassayre.me/'}

MENU_VARIABLES = {
    'mode': (('1 player', 'Offline', 'computer'), ('2 players', 'Offline', 'offline'), ('2 players', 'Online', 'online')),
    'clock': (('1 + 0', 'min', ((60000, 60000), 0)), ('2 + 1', 'min + sec', ((120000, 120000), 1000)),
              ('3 + 0', 'min', ((180000, 180000), 0)), ('3 + 2', 'min + sec', ((180000, 180000), 2000)),
              ('5 + 0', 'min', ((300000, 300000), 0)), ('5 + 3', 'min + sec', ((300000, 300000), 3000)),
              ('10 + 0', 'min', ((600000, 600000), 0)), ('10 + 5', 'min + sec', ((600000, 600000), 5000)),
              ('15 + 10', 'min + sec', ((900000, 900000), 10000)), ('30 + 0', 'min', ((1800000, 1800000), 0)),
              ('30 + 20', 'min + sec', ((18000000, 18000000), 20000)), ('No clock', 'infinite time', (False, 0))),
    'commands': (('Allow', 'commands', True), ('Deny', 'commands', False))
    }

TEXT_MENU = {
            'more': {(0, 0): ('state/last', 'Back', 'To the menu'),
                      (0, 1): ('browse/github', 'Git Hub', 'Webpage'),
                      (1, 0): ('browse/website', 'Website', 'In french'),
                      (1, 1): ('leave', 'Quit game', '')},
            'main': {(0, 0): ('state/menu load', 'Load game', 'Off/online'),
                     (0, 1): ('state/game tutorial', 'Tutorial', 'Soon'),
                     (1, 0): ('state/menu more', 'More', 'Links'),
                     (1, 1): ('state/menu new', 'New game', 'Off/online')},
            'new': {(0, 0): ('variable/new/0,0/mode/next', '', ''),
                     (0, 1): ('variable/new/0,1/clock/next', '', ''),
                     (1, 0): ('variable/new/1,0/commands/next', '', ''),
                     (1, 1): ('state/game', 'Start', 'game')},
            'load': {(0, 0): ('', 'Soon', ''),
                    (1, 1): ('state/menu main', 'Back', 'Main menu')},
            'pause': {(0, 0): ('state/last', 'Resume', ''),
                      (0, 1): ('save', 'Save', 'Soon'),
                      (1, 0): ('browse/github', 'Git Hub', 'Webpage'),
                      (1, 1): ('leave', 'Quit', 'Save')}
            }
