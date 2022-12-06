"""
Project name : Castle Game
File name : CONFIGS.py
Author(s) : DZ
"""

# COORDINATES
LOW_LEFT_CORNER = (-240, -240)
UP_RIGHT_CORNER = (50, 200)
CORNER_NOTICE = (-240, 240)
CORNER_INVENTORY = (70, 210)

# COLORS
BOX_COLOR = 'white'
CORRIDOR_COLOR = 'white'
WALL_COLOR = 'grey'
GOAL_COLOR = 'yellow'
DOOR_COLOR = 'orange'
OBJECT_COLOR = 'green'
VIEW_COLOR = 'wheat'
COLORS = {0: CORRIDOR_COLOR,
          1: WALL_COLOR,
          2: GOAL_COLOR,
          3: DOOR_COLOR,
          4: OBJECT_COLOR,
          5: VIEW_COLOR}
OUT_COLOR = 'white'

# CHARACTER
CHARACTER_COLOR = 'red'
CHARACTER_RATIO = 0.80
START_COORD = (0, 1)

# FILES
MAP_FILE = 'files/castle_map.txt'
QUESTIONS_FILE = 'files/doors.txt'
OBJECTS_FILE = 'files/objects.txt'

# TEXTS
STYLE_FONT = ('Times New Roman', 12, 'normal')
STYLE_FONT_TITLE = ('Times New Roman', 13, 'bold')
