"""
Project name : Castle Game
File name : main.py
Author(s) : DZ
"""

# -----------------------------------------------------------------------------
import CONFIGS
import turtle

# -----------------------------------------------------------------------------
INVENTORY_FRAME = turtle.Turtle()
NOTICE_FRAME = turtle.Turtle()

PLAYER_position = CONFIGS.START_COORD
# -----------------------------------------------------------------------------
# LEVEL 1
# -----------------------------------------------------------------------------


def read_matrix(filename: str) -> list:
    """Return a list of rows containing values of plan boxes."""
    with open(filename, 'r', encoding='utf-8') as file:
        matrix = [list(map(int, line.split())) for line in file.readlines()]
    return matrix


def get_step(matrix: list) -> int:
    """Return dimension to be given to the boxes."""
    rows, columns = len(matrix), len(matrix[0])
    width = abs(CONFIGS.LOW_LEFT_CORNER[0]) + abs(CONFIGS.UP_RIGHT_CORNER[0])
    height = abs(CONFIGS.LOW_LEFT_CORNER[1]) + abs(CONFIGS.UP_RIGHT_CORNER[1])
    return min(width//columns, height//rows)


def get_pxl_coords(indexes_box: tuple, step: int) -> tuple:
    """Return turtle pixel coordinates LOWER LEFT corner of a box defined
    by its indexed coordinates: row and column number."""
    row, column = indexes_box
    x0, y0 = CONFIGS.LOW_LEFT_CORNER[0], CONFIGS.UP_RIGHT_CORNER[1]
    return x0 + column * step, y0 - step - row * step


def draw_box(indexes_box: tuple, color: str, pxl_length: int):
    x, y = get_pxl_coords(indexes_box, pxl_length)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.color("white")
    turtle.fillcolor(color)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(pxl_length)
        turtle.left(90)
    turtle.end_fill()


def display_map(matrix: list):
    for index_row, line in enumerate(matrix):
        for index_col, num in enumerate(line):
            color_box = CONFIGS.COLORS[num]
            draw_box((index_row, index_col), color_box, get_step(matrix))

# -----------------------------------------------------------------------------
# LEVEL 2
# -----------------------------------------------------------------------------


def get_pxl_position(indexes_box: tuple, step: int) -> tuple:
    """Return turtle pixel coordinates CENTER of a box defined
    by its indexed coordinates: row and column number."""
    row, column = indexes_box
    x0, y0 = CONFIGS.LOW_LEFT_CORNER[0] + step//2, CONFIGS.UP_RIGHT_CORNER[1] - step//2
    return x0 + column * step, y0 - row * step


def draw_player(position: tuple, step: int):
    player.clear()
    player.penup()
    player.goto(get_pxl_position(position, step))
    player.pendown()
    player.dot(step * CONFIGS.CHARACTER_RATIO,
               CONFIGS.CHARACTER_COLOR)


def move(direction: tuple):
    """Display the character's movement if possible.
    If the character encounters a door, call the function to open it.
    If the character comes across an object,
    call the function to display the object on screen and put it in the inventory.
    If the character reaches the exit, call the function to allow or deny it.

    Modify the global variables 'grid' and 'PLAYER_position'."""
    global grid, PLAYER_position
    step = get_step(grid)
    row, column = direction[0], direction[1]
    if 0 <= row <= len(grid) - 1 and \
            0 <= column <= len(grid[0]) - 1:
        if grid[row][column] == 4:
            pick_up_object((row, column))
            grid[row][column] = 0
        if grid[row][column] == 3:
            display_notice("La porte est verrouillé.")
            if unlock_door((row, column)):
                grid[row][column] = 0
        if grid[row][column] in [0, 2]:
            if grid[PLAYER_position[0]][PLAYER_position[1]] != 2:
                draw_box(PLAYER_position, CONFIGS.COLORS[5], step)
            elif grid[row][column] == 2:
                is_over()
            PLAYER_position = direction
            draw_player(PLAYER_position, step)


def move_right():
    """Activated when the user presses the right arrow key on the keyboard.
    Calls the function that allows or denies movement with the requested new position."""
    turtle.onkeypress(lambda: None, 'Right')
    row, column = PLAYER_position[0], PLAYER_position[1] + 1
    move((row, column))
    turtle.onkeypress(move_right, 'Right')


def move_left():
    """Activated when the user presses the left arrow key on the keyboard.
        Calls the function that allows or denies movement with the requested new position."""
    turtle.onkeypress(lambda: None, 'Left')
    row, column = PLAYER_position[0], PLAYER_position[1] - 1
    move((row, column))
    turtle.onkeypress(move_left, 'Left')


def move_up():
    """Activated when the user presses the up arrow key on the keyboard.
            Calls the function that allows or denies movement with the requested new position."""
    turtle.onkeypress(lambda: None, 'Up')
    row, column = PLAYER_position[0] - 1, PLAYER_position[1]
    move((row, column))
    turtle.onkeypress(move_up, 'Up')


def move_down():
    """Activated when the user presses the down arrow key on the keyboard.
            Calls the function that allows or denies movement with the requested new position."""
    turtle.onkeypress(lambda: None, 'Down')
    row, column = PLAYER_position[0] + 1, PLAYER_position[1]
    move((row, column))
    turtle.onkeypress(move_down, 'Down')

# -----------------------------------------------------------------------------
# LEVEL 3-4
# -----------------------------------------------------------------------------


def create_data_dict(filename: str) -> dict:
    """Returns a dictionary from a file where each line is in the format < (,), " " >.
    The dictionary has tuple(row, column) as keys and str objects as values."""
    with open(filename, 'r', encoding='utf-8') as file:
        data_dict = dict()
        for line in file.readlines():
            coord, obj = eval(line)
            data_dict[coord] = obj
    return data_dict


def display_inventory():
    margin_left, margin_bottom = 10, 30
    INVENTORY_FRAME.clear()
    INVENTORY_FRAME.penup()
    INVENTORY_FRAME.goto(CONFIGS.CORNER_INVENTORY)
    INVENTORY_FRAME.write(inventory[0], font=CONFIGS.STYLE_FONT_TITLE)
    for i, obj in enumerate(inventory[1:], 1):
        INVENTORY_FRAME.goto((CONFIGS.CORNER_INVENTORY[0] + margin_left,
                              CONFIGS.CORNER_INVENTORY[1] - i * margin_bottom))
        INVENTORY_FRAME.write(obj, font=CONFIGS.STYLE_FONT)


def display_notice(notice: str):
    """Displays the game announcements."""
    NOTICE_FRAME.clear()
    NOTICE_FRAME.penup()
    NOTICE_FRAME.goto(CONFIGS.CORNER_NOTICE)
    NOTICE_FRAME.write(notice, font=CONFIGS.STYLE_FONT)


def pick_up_object(indexes_box: tuple):
    obj = objects_dict[indexes_box]
    display_notice(f"Vous avez trouvé: {obj}")
    inventory.append(obj)
    objects_counter[0] -= 1
    display_inventory()


def unlock_door(indexes_box: tuple) -> bool:
    question = questions_dict[indexes_box][0]
    answer = questions_dict[indexes_box][1].lower()
    player_answer = turtle.textinput('Question', question)
    if isinstance(player_answer, str) and player_answer.lower() == answer:
        display_notice("La porte s'ouvre.")
        unlock = True
    else:
        display_notice("La porte reste fermée.")
        unlock = False
    turtle.listen()
    return unlock


def is_over():
    """Determines if the game is over or not."""
    if objects_counter[0] == 0:
        display_notice("Bravo vous avez trouvé l'ensemble des objets"
                       "\net la sortie !")
        turtle.onkeypress(lambda: None, 'Left')
        turtle.onkeypress(lambda: None, 'Right')
        turtle.onkeypress(lambda: None, 'Up')
        turtle.onkeypress(lambda: None, 'Down')
    else:
        display_notice("Vous n'avez pas trouvé l'ensemble des objets."
                       "\nCherchez encore !")


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    turtle.hideturtle()
    turtle.speed('fastest')

    screen = turtle.Screen()
    screen.title("Quête dans le sommet du Python des neiges")
    screen.tracer(0)  # speed up drawing
    screen.update()  # to be used when tracer is off

    grid = read_matrix(CONFIGS.MAP_FILE)
    display_map(grid)

    player = turtle.Turtle()
    draw_player(PLAYER_position, get_step(grid))

    inventory = ['Inventaire']
    display_inventory()
    objects_dict = create_data_dict(CONFIGS.OBJECTS_FILE)
    objects_counter = [len(objects_dict)]

    questions_dict = create_data_dict(CONFIGS.QUESTIONS_FILE)

    turtle.listen()
    turtle.onkeypress(move_left, 'Left')
    turtle.onkeypress(move_right, 'Right')
    turtle.onkeypress(move_up, 'Up')
    turtle.onkeypress(move_down, 'Down')

    turtle.mainloop()
