###########################################
#
# Tetris recreation by RandomsongV2
#
###########################################
#
# Controls:
# 
# Left - move shape left
# Right - move shape right
# Down - move shape down
# Up - drop shape (move down to the ground)
# C - rotate shape cw
# Z - rotate shape ccw
# X - swap current shape with next in queue
#
###########################################
#
# Controls are configur-able:

def setup_controls():
    turtle.onkey(rotate_shape_left, 'z')
    turtle.onkey(swap_shape, 'x')
    turtle.onkey(rotate_shape_right, 'c')

    turtle.onkey(move_right, 'Right')
    turtle.onkey(move_left, 'Left')
    turtle.onkey(update, 'Down')
    turtle.onkey(drop_shape, 'Up')

#
###########################################







import turtle
import random

#520 720
#10 * 20
#36 * 36
# I J L O S T Z
color =       ['#000000', '#00f0f0', '#0000f0', '#f0a000', '#f0f000', '#00f000', '#a000f0', '#f00000', '#999999', '#ffffff']
light_color = ['#000000', '#6ff8f8', '#6f6ff8', '#f8c26f', '#f8f86f', '#6ff86f', '#c26ff8', '#f86f6f', '#c1c1c1', '#ffffff']
dark_color =  ['#000000', '#007878', '#000078', '#785000', '#787800', '#007800', '#500078', '#780000', '#4c4c4c', '#ffffff']
#               bg         cyan       blue       orange     yellow     green      purple     red        gray       text
#                          [][][][]   []             []     [][]         [][]       []       [][]
#                                     [][][]     [][][]     [][]       [][]       [][][]       [][]

# all of the shapes
# tetrominos[shape][rotation]
tetrominos = [ None,
              [
                  [
                      [0, 0, 0, 0],
                      [1, 1, 1, 1],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]
                      ],
                  [ [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0] ],
                  [ [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0] ],
                  [ [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0] ],
                  ],
              [
                  [ [1, 0, 0], [1, 1, 1], [0, 0, 0] ],
                  [ [0, 1, 1], [0, 1, 0], [0, 1, 0] ],
                  [ [0, 0, 0], [1, 1, 1], [0, 0, 1] ],
                  [ [0, 1, 0], [0, 1, 0], [1, 1, 0] ],
                  ],
              [
                  [ [0, 0, 1], [1, 1, 1], [0, 0, 0] ],
                  [ [0, 1, 0], [0, 1, 0], [0, 1, 1] ],
                  [ [0, 0, 0], [1, 1, 1], [1, 0, 0] ],
                  [ [1, 1, 0], [0, 1, 0], [0, 1, 0] ],
                  ],
              [
                  [ [1, 1], [1, 1] ],
                  [ [1, 1], [1, 1] ],
                  [ [1, 1], [1, 1] ],
                  [ [1, 1], [1, 1] ],
                  ],
              [
                  [ [0, 1, 1], [1, 1, 0], [0, 0, 0] ],
                  [ [0, 1, 0], [0, 1, 1], [0, 0, 1] ],
                  [ [0, 0, 0], [0, 1, 1], [1, 1, 0] ],
                  [ [1, 0, 0], [1, 1, 0], [0, 1, 0] ],
                  ],
              [
                  [ [0, 1, 0], [1, 1, 1], [0, 0, 0] ],
                  [ [0, 1, 0], [0, 1, 1], [0, 1, 0] ],
                  [ [0, 0, 0], [1, 1, 1], [0, 1, 0] ],
                  [ [0, 1, 0], [1, 1, 0], [0, 1, 0] ],
                  ],
              [
                  [ [1, 1, 0], [0, 1, 1], [0, 0, 0] ],
                  [ [0, 0, 1], [0, 1, 1], [0, 1, 0] ],
                  [ [0, 0, 0], [1, 1, 0], [0, 1, 1] ],
                  [ [0, 1, 0], [1, 1, 0], [1, 0, 0] ],
                  ]
              ]

tetromino_sizes = [None, 4, 3, 3, 2, 3, 3, 3]

base_lane_collapse = [[0, 1, 2], [1, 2], [0, 1, 2], [0, 1]]
tetromino_lane_collapse = [ # what lanes to check when landing the shape
        None,
        [[0, 1, 2, 3], [2], [0, 1, 2, 3], [1]],
        base_lane_collapse,
        base_lane_collapse,
        [[0, 1], [0, 1], [0, 1], [0, 1]],
        base_lane_collapse,
        base_lane_collapse,
        base_lane_collapse
        ]
del base_lane_collapse

rotation_tests_i = [
        [None, [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)], None, [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]],
        [[(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)], None, [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]],
        [None, [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)], None, [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]],
        [[(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)], None, [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]]
        ]
rotation_tests_other = [
        [None, [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)], None, [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]],
        [[(0, 0), (-1, 0), (-1, 1), (0,-2), (-1, -2)], None, [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]],
        [None, [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], None, [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]],
        [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], None, [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]]
        ]
rotation_tests = [
        None, rotation_tests_i, rotation_tests_other, rotation_tests_other, rotation_tests_other, rotation_tests_other, rotation_tests_other, rotation_tests_other
        ]
# rotation_tests[figure][old_rotation][new_rotation]
del rotation_tests_other
del rotation_tests_i


board = [[0  for i in range(20)] + [8] for j in range(10)] + [[8 for i in range(21)]]
 
def ttsp(x, y): #transform to screen pos
    return x - 270, y - 360

def draw_pixel(i, j, index):
    x, y = ttsp(i * 36, j * 36)
    if index:
        #light color
        turtle.fillcolor(light_color[index])
        turtle.goto(x, y)
        turtle.begin_fill()
        turtle.goto(x, y + 36)
        turtle.goto(x + 36, y + 36)
        turtle.goto(x + 30, y + 30)
        turtle.goto(x + 6, y + 30)
        turtle.goto(x + 6, y + 6)
        turtle.end_fill()
        #dark color
        turtle.fillcolor(dark_color[index])
        turtle.begin_fill()
        turtle.goto(x, y)
        turtle.goto(x + 36, y)
        turtle.goto(x + 36, y + 36)
        turtle.goto(x + 30, y + 30)
        turtle.goto(x + 30, y + 6)
        turtle.end_fill()
        #side color
        #center
        turtle.fillcolor(color[index])
        turtle.begin_fill()
        turtle.goto(x + 6, y + 6)
        turtle.goto(x + 6, y + 30)
        turtle.goto(x + 30, y + 30)
        turtle.end_fill()
    else:
        turtle.fillcolor(color[index])
        turtle.goto(x, y)
        turtle.begin_fill()
        turtle.goto(x + 36, y)
        turtle.goto(x + 36, y + 36)
        turtle.goto(x, y + 36)
        turtle.end_fill()


def draw_shape(shape, rotation, x, y):
    global tetromino_sizes
    global tetrominos
    for i in range(tetromino_sizes[shape]):
        for j in range(tetromino_sizes[shape]):
            if tetrominos[shape][rotation][i][j]:
                if j + y < 20:
                    draw_pixel(i + x, j + y, shape)

# if shape overlaps with anything on the board then return false
def check_shape_collision(shape, rotation, x, y):
    global tetromino_sizes
    global tetrominos
    global board
    for i in range(tetromino_sizes[shape]):
        for j in range(tetromino_sizes[shape]):
            if tetrominos[shape][rotation][i][j]:
                if j + y < 20 and board[i + x][j + y] > 0 or i + x < 0 or i + x >= 10:
                    return False
    return True

def rotate_shape_right():
    #                 (shape, rotation, x, y)
    global shape
    global shape_pos
    global rotation_tests
    global shape_rotation
    rotation = shape_rotation
    x, y = shape_pos
    new_rotation = (rotation + 1)%4
    for i in rotation_tests[shape][rotation][new_rotation]:
        if check_shape_collision(shape, new_rotation, x + i[0], y + i[1]):
            shape_rotation =  new_rotation
            shape_pos = (x + i[0], y + i[1])
            draw_moved_shape(shape, rotation, x, y, shape, new_rotation, x + i[0], y + i[1], False)
            return True

def rotate_shape_left():
    #                 (shape, rotation, x, y)
    global shape
    global shape_pos
    global rotation_tests
    global shape_rotation
    rotation = shape_rotation
    x, y = shape_pos
    new_rotation = (rotation - 1)%4
    for i in rotation_tests[shape][rotation][new_rotation]:
        if check_shape_collision(shape, new_rotation, x + i[0], y + i[1]):
            shape_rotation =  new_rotation
            shape_pos = (x + i[0], y + i[1])
            draw_moved_shape(shape, rotation, x, y, shape, new_rotation, x + i[0], y + i[1], False)
            return True

# draw buffer shape
def draw_side_shape():
    global next_shape
    #black rectangle
    turtle.fillcolor(color[0])
    turtle.goto(126, -36)
    turtle.begin_fill()
    turtle.goto(306, -36)
    turtle.goto(306, 72)
    turtle.goto(126, 72)
    turtle.end_fill()
    #shape
    if next_shape == 1:
        x, y = 11.5, 8.5
    elif next_shape == 4:
        x, y = 12.5, 10
    else:
        x, y = 12, 9
    draw_shape(next_shape, 1, x, y)

# create a new shape
def spawn_shape():
    global shape
    global shape_pos
    global shape_rotation
    global next_shape
    if check_shape_collision(next_shape, 0, 5, 19):
        shape = next_shape
        shape_pos = (5, 19)
        shape_rotation = 0
        next_shape = random.randint(1, 7)
        draw_side_shape()
        draw_shape(shape, shape_rotation, 5, 19)
    else:
        game_over()

# draw a digit
def draw_number(num, x, y, color, bg_color):
    turtle.fillcolor(color)
    match num:
        case '0':
            turtle.goto(x + 7, y + 3)
            turtle.begin_fill()
            turtle.goto(x + 16, y + 3)
            turtle.goto(x + 21, y + 12)
            turtle.goto(x + 21, y + 24)
            turtle.goto(x + 16, y + 33)
            turtle.goto(x + 7, y + 33)
            turtle.goto(x + 2, y + 24)
            turtle.goto(x + 2, y + 12)
            turtle.end_fill()

            turtle.fillcolor(bg_color)
            turtle.goto(x + 7, y + 22)
            turtle.begin_fill()
            turtle.goto(x + 7, y + 14)
            turtle.goto(x + 10, y + 9)
            turtle.goto(x + 13, y + 9)
            turtle.goto(x + 16, y + 14)
            turtle.goto(x + 16, y + 22)
            turtle.goto(x + 13, y + 27)
            turtle.goto(x + 10, y + 27)
            turtle.end_fill()
        case '1':
            turtle.goto(x + 2, y + 3)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 9)
            turtle.goto(x + 9, y + 9)
            turtle.goto(x + 9, y + 27)
            turtle.goto(x + 3, y + 27)
            turtle.goto(x + 9, y + 33)
            turtle.goto(x + 15, y + 33)
            turtle.goto(x + 15, y + 9)
            turtle.goto(x + 22, y + 9)
            turtle.goto(x + 22, y + 3)
            turtle.end_fill()
        case '2':
            turtle.goto(x + 2, y + 3)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 11)
            turtle.goto(x + 14, y + 23)
            turtle.goto(x + 14, y + 25)
            turtle.goto(x + 12, y + 27)
            turtle.goto(x + 8, y + 27)
            turtle.goto(x + 6, y + 25)
            turtle.goto(x + 6, y + 24)
            turtle.goto(x + 2, y + 24)
            turtle.goto(x + 2, y + 25)
            turtle.goto(x + 2, y + 29)
            turtle.goto(x + 6, y + 33)
            turtle.goto(x + 15, y + 33)
            turtle.goto(x + 19, y + 28)
            turtle.goto(x + 19, y + 21)
            turtle.goto(x + 9, y + 11)
            turtle.goto(x + 9, y + 8)
            turtle.goto(x + 19, y + 8)
            turtle.goto(x + 19, y + 3)
            turtle.end_fill()
        case '3':
            turtle.goto(x + 2, y + 8)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 12)
            turtle.goto(x + 4, y + 12)
            turtle.goto(x + 6, y + 8)
            turtle.goto(x + 11, y + 8)
            turtle.goto(x + 13, y + 10)
            turtle.goto(x + 13, y + 15)
            turtle.goto(x + 11, y + 17)
            turtle.goto(x + 6, y + 17)
            turtle.goto(x + 6, y + 20)
            turtle.goto(x + 11, y + 25)
            turtle.goto(x + 11, y + 28)
            turtle.goto(x + 4, y + 28)
            turtle.goto(x + 4, y + 33)
            turtle.goto(x + 20, y + 33)
            turtle.goto(x + 16, y + 23)
            turtle.goto(x + 21, y + 19)
            turtle.goto(x + 21, y + 10)
            turtle.goto(x + 14, y + 3)
            turtle.goto(x + 7, y + 3)
            turtle.end_fill()
        case '4':
            turtle.goto(x + 16, y + 3)
            turtle.begin_fill()
            turtle.goto(x + 16, y + 14)
            turtle.goto(x + 2, y + 14)
            turtle.goto(x + 2, y + 33)
            turtle.goto(x + 8, y + 33)
            turtle.goto(x + 8, y + 20)
            turtle.goto(x + 16, y + 20)
            turtle.goto(x + 16, y + 33)
            turtle.goto(x + 22, y + 33)
            turtle.goto(x + 22, y + 3)
            turtle.end_fill()
        case '5':
            turtle.goto(x + 2, y + 7)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 12)
            turtle.goto(x + 7, y + 12)
            turtle.goto(x + 7, y + 10)
            turtle.goto(x + 10, y + 7)
            turtle.goto(x + 13, y + 7)
            turtle.goto(x + 16, y + 10)
            turtle.goto(x + 16, y + 14)
            turtle.goto(x + 13, y + 17)
            turtle.goto(x + 3, y + 17)
            turtle.goto(x + 3, y + 33)
            turtle.goto(x + 21, y + 33)
            turtle.goto(x + 21, y + 26)
            turtle.goto(x + 8, y + 26)
            turtle.goto(x + 8, y + 23)
            turtle.goto(x + 18, y + 23)
            turtle.goto(x + 22, y + 19)
            turtle.goto(x + 22, y + 8)
            turtle.goto(x + 19, y + 3)
            turtle.goto(x + 6, y + 3)
            turtle.end_fill()
        case '6':
            turtle.goto(x + 2, y + 8)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 26)
            turtle.goto(x + 7, y + 33)
            turtle.goto(x + 20, y + 33)
            turtle.goto(x + 20, y + 28)
            turtle.goto(x + 11, y + 28)
            turtle.goto(x + 8, y + 25)
            turtle.goto(x + 8, y + 22)
            turtle.goto(x + 10, y + 20)
            turtle.goto(x + 18, y + 20)
            turtle.goto(x + 22, y + 16)
            turtle.goto(x + 22, y + 8)
            turtle.goto(x + 18, y + 3)
            turtle.goto(x + 5, y + 3)
            turtle.end_fill()

            turtle.fillcolor(bg_color)
            turtle.goto(x + 7, y + 11)
            turtle.begin_fill()
            turtle.goto(x + 7, y + 13)
            turtle.goto(x + 9, y + 15)
            turtle.goto(x + 15, y + 15)
            turtle.goto(x + 17, y + 13)
            turtle.goto(x + 17, y + 11)
            turtle.goto(x + 15, y + 9)
            turtle.goto(x + 9, y + 9)
            turtle.end_fill()
        case '7':
            turtle.goto(x + 2, y + 33)
            turtle.begin_fill()
            turtle.goto(x + 22, y + 33)
            turtle.goto(x + 22, y + 25)
            turtle.goto(x + 15, y + 18)
            turtle.goto(x + 15, y + 3)
            turtle.goto(x + 9, y + 3)
            turtle.goto(x + 9, y + 20)
            turtle.goto(x + 16, y + 27)
            turtle.goto(x + 2, y + 27)
            turtle.end_fill()
        case '8':
            turtle.goto(x + 6, y + 3)
            turtle.begin_fill()
            turtle.goto(x + 2, y + 7)
            turtle.goto(x + 2, y + 15)
            turtle.goto(x + 6, y + 19)
            turtle.goto(x + 2, y + 23)
            turtle.goto(x + 2, y + 29)
            turtle.goto(x + 6, y + 33)
            turtle.goto(x + 18, y + 33)
            turtle.goto(x + 22, y + 29)
            turtle.goto(x + 22, y + 23)
            turtle.goto(x + 18, y + 19)
            turtle.goto(x + 22, y + 15)
            turtle.goto(x + 22, y + 7)
            turtle.goto(x + 18, y + 3)
            turtle.end_fill()

            turtle.fillcolor(bg_color)
            turtle.goto(x + 7, y + 10)
            turtle.begin_fill()
            turtle.goto(x + 7, y + 12)
            turtle.goto(x + 9, y + 14)
            turtle.goto(x + 15, y + 14)
            turtle.goto(x + 17, y + 12)
            turtle.goto(x + 17, y + 10)
            turtle.goto(x + 15, y + 8)
            turtle.goto(x + 9, y + 8)
            turtle.end_fill()

            turtle.goto(x + 17, y + 26)
            turtle.begin_fill()
            turtle.goto(x + 17, y + 24)
            turtle.goto(x + 15, y + 22)
            turtle.goto(x + 9, y + 22)
            turtle.goto(x + 7, y + 24)
            turtle.goto(x + 7, y + 26)
            turtle.goto(x + 9, y + 28)
            turtle.goto(x + 15, y + 28)
            turtle.end_fill()
        case '9':
            turtle.goto(x + 22, y + 28)
            turtle.begin_fill()
            turtle.goto(x + 22, y + 10)
            turtle.goto(x + 17, y + 3)
            turtle.goto(x + 4, y + 3)
            turtle.goto(x + 4, y + 8)
            turtle.goto(x + 13, y + 8)
            turtle.goto(x + 16, y + 11)
            turtle.goto(x + 16, y + 14)
            turtle.goto(x + 14, y + 16)
            turtle.goto(x + 6, y + 16)
            turtle.goto(x + 2, y + 20)
            turtle.goto(x + 2, y + 28)
            turtle.goto(x + 6, y + 33)
            turtle.goto(x + 19, y + 33)
            turtle.end_fill()

            turtle.fillcolor(bg_color)
            turtle.goto(x + 17, y + 25)
            turtle.begin_fill()
            turtle.goto(x + 17, y + 23)
            turtle.goto(x + 15, y + 21)
            turtle.goto(x + 9, y + 21)
            turtle.goto(x + 7, y + 23)
            turtle.goto(x + 7, y + 25)
            turtle.goto(x + 9, y + 27)
            turtle.goto(x + 15, y + 27)
            turtle.end_fill()

# Update score display
def draw_score():
    global score
    global drawn_score
    to_draw = str(min(score, 999999))
    to_draw = '0' * (6 - len(to_draw)) + to_draw
    for i in range(6):
        if drawn_score[i] != to_draw[i]:
            turtle.goto(139 + 26 * i, 198)
            turtle.fillcolor(color[0])
            turtle.begin_fill()
            turtle.goto(165 + 26 * i, 198)
            turtle.goto(165 + 26 * i, 234)
            turtle.goto(139 + 26 * i, 234)
            turtle.end_fill()
            draw_number(to_draw[i], 139 + 26 * i, 198, color[9], color[0])
    drawn_score = to_draw

# Update level display
def draw_level():
    global level
    global drawn_level
    to_draw = str(level)
    if len(to_draw) < 2:
        to_draw = '0' + to_draw
    for i in range(2):
        if drawn_level[i] != to_draw[i]:
            turtle.goto(211 + 26 * i, -162)
            turtle.fillcolor(color[0])
            turtle.begin_fill()
            turtle.goto(237 + 26 * i, -162)
            turtle.goto(237 + 26 * i, -126)
            turtle.goto(211 + 26 * i, -126)
            turtle.end_fill()
            draw_number(to_draw[i], 211 + 26 * i, -162, color[9], color[0])
    drawn_level = to_draw
 
# do most of preparations for the game
def init_game():
    turtle.title('Tetris')
    turtle.setup(540 + 72,720 + 72, 720 - 36, 160 - 36)
    turtle.hideturtle()
    turtle.tracer(0)
    turtle.penup()
    turtle.goto(*ttsp(360, 0))
    turtle.bgcolor('#000000')
    for i in range(-1, 17):
        for j in range(-1, 21):
            if i >= 0 and i < 11 and j >= 0 and j < 21:
                draw_pixel(i, j, board[i][j])
            else:
                draw_pixel(i, j, 8)
    global next_shape
    next_shape = random.randint(1, 7)
    spawn_shape()
    global score
    global level
    global lanes_cleared
    score = 0
    level = 0
    lanes_cleared = 0
    global game_running
    game_running = True
    global drawn_score
    global drawn_level
    drawn_score = '------'
    drawn_level = '--'
    global top_score
    #top_score = 272060
    try:
        score_file = open('top_score', 'rb')
        top_score = int.from_bytes(score_file.read())
        score_file.close()
    except:
        top_score = 0

    global used_keys
    used_keys = []

######## Draw letters area
    turtle.fillcolor(color[0])

    #top rectangle
    turtle.goto(126, 180)
    turtle.begin_fill()
    turtle.goto(306, 180)
    turtle.goto(306, 360)
    turtle.goto(126, 360)
    turtle.end_fill()

    draw_score()

    # draw top score
    to_draw = str(top_score)
    to_draw = '0' * (6 - len(to_draw)) + to_draw
    for i in range(6):
        draw_number(to_draw[i], 139 + 26 * i, 270, color[9], color[0])

    #middle rectangle
    turtle.goto(126, 72)
    turtle.begin_fill()
    turtle.goto(306, 72)
    turtle.goto(306, 144)
    turtle.goto(126, 144)
    turtle.end_fill()

    #bottom rectangle
    turtle.goto(126, -180)
    turtle.begin_fill()
    turtle.goto(306, -180)
    turtle.goto(306, -72)
    turtle.goto(126, -72)
    turtle.end_fill()

    draw_level()

######## Draw letters
    turtle.fillcolor(color[9])

#### Middle lane text
    #N
    x, y = 144, 90
    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 33)
    turtle.goto(x + 9, y + 33)
    turtle.goto(x + 27, y + 15)
    turtle.goto(x + 27, y + 33)
    turtle.goto(x + 33, y + 33)
    turtle.goto(x + 33, y + 3)
    turtle.goto(x + 27, y + 3)
    turtle.goto(x + 9, y + 21)
    turtle.goto(x + 9, y + 3)
    turtle.end_fill()
    #E
    x += 36
    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 33)
    turtle.goto(x + 33, y + 33)
    turtle.goto(x + 33, y + 27)
    turtle.goto(x + 9, y + 27)
    turtle.goto(x + 9, y + 21)
    turtle.goto(x + 27, y + 21)
    turtle.goto(x + 27, y + 15)
    turtle.goto(x + 9, y + 15)
    turtle.goto(x + 9, y + 9)
    turtle.goto(x + 33, y + 9)
    turtle.goto(x + 33, y + 3)
    turtle.end_fill()
    #X
    x += 36
    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 9)
    turtle.goto(x + 27, y + 33)
    turtle.goto(x + 33, y + 33)
    turtle.goto(x + 33, y + 27)
    turtle.goto(x + 9, y + 3)
    turtle.end_fill()
    turtle.goto(x + 3, y + 33)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 27)
    turtle.goto(x + 27, y + 3)
    turtle.goto(x + 33, y + 3)
    turtle.goto(x + 33, y + 9)
    turtle.goto(x + 9, y + 33)
    turtle.end_fill()
    #T
    x += 36
    turtle.goto(x + 3, y + 33)
    turtle.begin_fill()
    turtle.goto(x + 33, y + 33)
    turtle.goto(x + 33, y + 27)
    turtle.goto(x + 21, y + 27)
    turtle.goto(x + 21, y + 3)
    turtle.goto(x + 15, y + 3)
    turtle.goto(x + 15, y + 27)
    turtle.goto(x + 3, y + 27)
    turtle.end_fill()
######## Top text
    #T
    x, y = 144, 306
    turtle.goto(x + 2, y + 33)
    turtle.begin_fill()
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 15, y + 27)
    turtle.goto(x + 15, y + 3)
    turtle.goto(x + 9, y + 3)
    turtle.goto(x + 9, y + 27)
    turtle.goto(x + 2, y + 27)
    turtle.end_fill()

    #O
    x += 24
    turtle.goto(x + 8, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 17, y + 3)
    turtle.goto(x + 22, y + 12)
    turtle.goto(x + 22, y + 24)
    turtle.goto(x + 17, y + 33)
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 3, y + 24)
    turtle.goto(x + 3, y + 12)
    turtle.end_fill()

    turtle.fillcolor(color[0])
    turtle.goto(x + 9, y + 22)
    turtle.begin_fill()
    turtle.goto(x + 9, y + 14)
    turtle.goto(x + 12, y + 9)
    turtle.goto(x + 13, y + 9)
    turtle.goto(x + 16, y + 14)
    turtle.goto(x + 16, y + 22)
    turtle.goto(x + 13, y + 27)
    turtle.goto(x + 12, y + 27)
    turtle.end_fill()

    #P
    turtle.fillcolor(color[9])
    x += 24

    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 33)
    turtle.goto(x + 19, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 22, y + 21)
    turtle.goto(x + 19, y + 15)

    turtle.goto(x + 9, y + 15)
    turtle.goto(x + 9, y + 3)
    turtle.end_fill()
    
    turtle.fillcolor(color[0])
    turtle.goto(x + 9, y + 28)
    turtle.begin_fill()
    turtle.goto(x + 15, y + 28)
    turtle.goto(x + 15, y + 20)
    turtle.goto(x + 9, y + 20)
    turtle.end_fill()

######## Top text 2
    #S
    x, y = 144, 234
    turtle.fillcolor(color[9])

    turtle.goto(x + 22, y + 33)
    turtle.begin_fill()
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 10, y + 27)
    turtle.goto(x + 8, y + 25)

    turtle.goto(x + 8, y + 23)
    turtle.goto(x + 10, y + 21)
    turtle.goto(x + 17, y + 21)
    turtle.goto(x + 22, y + 15)

    turtle.goto(x + 22, y + 8)
    turtle.goto(x + 17, y + 3)
    turtle.goto(x + 2, y + 3)
    turtle.goto(x + 2, y + 9)

    turtle.goto(x + 14, y + 9)
    turtle.goto(x + 16, y + 11)
    turtle.goto(x + 16, y + 13)
    turtle.goto(x + 14, y + 15)

    turtle.goto(x + 5, y + 15)
    turtle.goto(x + 2, y + 20)
    turtle.goto(x + 2, y + 28)
    turtle.goto(x + 7, y + 33)
    turtle.end_fill()

    #C
    x += 24

    turtle.goto(x + 8, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 2, y + 9)
    turtle.goto(x + 2, y + 27)
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 12, y + 27)
    turtle.goto(x + 8, y + 23)
    turtle.goto(x + 8, y + 13)
    turtle.goto(x + 12, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()

    #O
    x += 24
    turtle.goto(x + 8, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 17, y + 3)
    turtle.goto(x + 22, y + 12)
    turtle.goto(x + 22, y + 24)
    turtle.goto(x + 17, y + 33)
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 3, y + 24)
    turtle.goto(x + 3, y + 12)
    turtle.end_fill()

    turtle.fillcolor(color[0])
    turtle.goto(x + 9, y + 22)
    turtle.begin_fill()
    turtle.goto(x + 9, y + 14)
    turtle.goto(x + 12, y + 9)
    turtle.goto(x + 13, y + 9)
    turtle.goto(x + 16, y + 14)
    turtle.goto(x + 16, y + 22)
    turtle.goto(x + 13, y + 27)
    turtle.goto(x + 12, y + 27)
    turtle.end_fill()

    #R
    turtle.fillcolor(color[9])
    x += 24
    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 33)
    turtle.goto(x + 19, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 22, y + 21)
    turtle.goto(x + 19, y + 15)

    turtle.goto(x + 15, y + 15)
    turtle.goto(x + 22, y + 3)
    turtle.goto(x + 16, y + 3)

    turtle.goto(x + 9, y + 15)
    turtle.goto(x + 9, y + 3)
    turtle.end_fill()

    turtle.fillcolor(color[0])
    turtle.goto(x + 9, y + 28)
    turtle.begin_fill()
    turtle.goto(x + 15, y + 28)
    turtle.goto(x + 15, y + 20)
    turtle.goto(x + 9, y + 20)
    turtle.end_fill()

    #E
    turtle.fillcolor(color[9])
    x += 24
    turtle.goto(x + 3, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 3, y + 33)
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 9, y + 27)
    turtle.goto(x + 9, y + 21)
    turtle.goto(x + 9, y + 21)
    turtle.goto(x + 16, y + 21)
    turtle.goto(x + 16, y + 15)
    turtle.goto(x + 9, y + 15)
    turtle.goto(x + 9, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()
    
######## Bottom text
    x, y = 144, -126

    #L
    turtle.goto(x + 2, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 2, y + 33)
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 8, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()

    #E
    x += 24
    turtle.goto(x + 2, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 2, y + 33)
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 8, y + 27)
    turtle.goto(x + 8, y + 21)
    turtle.goto(x + 18, y + 21)
    turtle.goto(x + 18, y + 15)
    turtle.goto(x + 8, y + 15)
    turtle.goto(x + 8, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()

    #V
    x += 24
    turtle.goto(x + 2, y + 33)
    turtle.begin_fill()
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 12, y + 12)
    turtle.goto(x + 16, y + 33)
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 15, y + 3)
    turtle.goto(x + 9, y + 3)
    turtle.end_fill()

    #E
    x += 24
    turtle.goto(x + 2, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 2, y + 33)
    turtle.goto(x + 22, y + 33)
    turtle.goto(x + 22, y + 27)
    turtle.goto(x + 8, y + 27)
    turtle.goto(x + 8, y + 21)
    turtle.goto(x + 18, y + 21)
    turtle.goto(x + 18, y + 15)
    turtle.goto(x + 8, y + 15)
    turtle.goto(x + 8, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()

    #L
    x += 24
    turtle.goto(x + 2, y + 3)
    turtle.begin_fill()
    turtle.goto(x + 2, y + 33)
    turtle.goto(x + 8, y + 33)
    turtle.goto(x + 8, y + 9)
    turtle.goto(x + 22, y + 9)
    turtle.goto(x + 22, y + 3)
    turtle.end_fill()





# turn movable shape into frozen
def solidify_shape(shape, rotation, x, y):
    global tetromino_sizes
    global tetrominos
    global board
    for i in range(tetromino_sizes[shape]):
        for j in range(tetromino_sizes[shape]):
            if tetrominos[shape][rotation][i][j]:
                if y + j < 20:
                    board[x + i][y + j] = shape
                else:
                    game_over()
                    return

# gravity
def update():
    global shape
    global shape_pos
    global shape_rotation
    if check_shape_collision(shape, shape_rotation, shape_pos[0], shape_pos[1] - 1):
        draw_moved_shape(shape, shape_rotation, *shape_pos, shape, shape_rotation, shape_pos[0], shape_pos[1] - 1, False)
        shape_pos = (shape_pos[0], shape_pos[1] - 1)
    else:
        solidify_shape(shape, shape_rotation, *shape_pos)
        
        collapse_lanes(tetromino_lane_collapse[shape][shape_rotation], shape_pos[1])
        spawn_shape()

def game_over():
    global game_running
    if game_running:
        game_running = False
        print('GAME OVER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        global score
        global top_score
        to_save = min(score, 999999)
        if to_save > top_score:
            score_file = open('top_score', 'wb')
            score_file.write(bytes([to_save//65536, (to_save%65536)//256, to_save%256]))
            score_file.close()
        global used_keys
        for i in used_keys:
            turtle.onkey(None, i)

def move_right():
    global shape
    global shape_pos
    global shape_rotation
    if check_shape_collision(shape, shape_rotation, shape_pos[0] + 1, shape_pos[1]):
        draw_moved_shape(shape, shape_rotation, *shape_pos, shape, shape_rotation, shape_pos[0] + 1, shape_pos[1], False)
        shape_pos = (shape_pos[0] + 1, shape_pos[1])


def move_left():
    global shape
    global shape_pos
    global shape_rotation
    if check_shape_collision(shape, shape_rotation, shape_pos[0] - 1, shape_pos[1]):
        draw_moved_shape(shape, shape_rotation, *shape_pos, shape, shape_rotation, shape_pos[0] - 1, shape_pos[1], False)
        shape_pos = (shape_pos[0] - 1, shape_pos[1])

# swap current shape with buffer shape
def swap_shape():
    global shape
    global shape_pos
    global shape_rotation
    global next_shape
    for i in range(4):
        if check_shape_collision(next_shape, (shape_rotation + i)%4, *shape_pos):
            draw_moved_shape(shape, shape_rotation, *shape_pos, next_shape, (shape_rotation + i)%4, *shape_pos, True)
            shape, next_shape = next_shape, shape
            shape_rotation = (shape_rotation + i)%4
            draw_side_shape()
            return

# check if lane is fully filled
def check_lane(lane):
    if lane > 19:
        return False
    global board
    for i in board[:-1]:
        if not i[lane]:
            return False
    return True

# 
def collapse_lane(lane):
    global board
    for i in board[:-1]:
        i[lane:20] = i[lane + 1:]
        i[19] = 0

# collapse fully filled lanes
def collapse_lanes(lanes, y):
#                 (lanes from tetromino_lane_collapse, shape's y pos)
    to_collapse = []
    collapsed_lanes = 0
    for i in lanes:
        if check_lane(i + y):
            to_collapse.append(i + y - collapsed_lanes)
            collapsed_lanes += 1
    if collapsed_lanes:
        global board
        old_board = []
        for i in board:
            old_board.append(i.copy())
        for i in to_collapse:
            collapse_lane(i)
        for i in range(10):
            for j in range(20):
                if old_board[i][j] != board[i][j]:
                    draw_pixel(i, j, board[i][j])
        lane_scores = [0, 40, 100, 300, 1200]
        global score
        global level
        global lanes_cleared
        lanes_cleared += collapsed_lanes
        score += lane_scores[collapsed_lanes]*(level + 1)
        draw_score()
        if level * 10 < lanes_cleared - 10:
            level = lanes_cleared//10
            draw_level()

# get non-overlapping squares of shape1 and shape2 between each other
# 3rd returning value contains overlapping squares of shape1 and shape2
def get_non_overlapping(shape1, rotation1, x1, y1, shape2, rotation2, x2, y2):
    poses1 = {}
    poses2 = {}
    poses3 = {}
    global tetromino_sizes
    global tetrominos
    for i in range(tetromino_sizes[shape1]):
        for j in range(tetromino_sizes[shape1]):
            if tetrominos[shape1][rotation1][i][j]:
                poses1[(i + x1, j + y1)] = True
    for i in range(tetromino_sizes[shape2]):
        for j in range(tetromino_sizes[shape2]):
            if tetrominos[shape2][rotation2][i][j]:
                if (i + x2, j + y2) in poses1:
                    poses1.pop((i + x2, j + y2))
                    poses3[(i + x2, j + y2)] = True
                else:
                    poses2[(i + x2, j + y2)] = True
    return poses1, poses2, poses3

# update shape visual
def draw_moved_shape(old_shape, old_rotation, old_x, old_y, shape, rotation, x, y, draw_overlap):
    black, draw, overlap = get_non_overlapping(old_shape, old_rotation, old_x, old_y, shape, rotation, x, y)
    for i in black:
        if i[1] < 20:
            draw_pixel(*i, 0)
    for i in draw:
        if i[1] < 20:
            draw_pixel(*i, shape)
    if draw_overlap:
        for i in overlap:
            if i[1] < 20:
                draw_pixel(*i, shape)

def drop_shape():
    global shape
    global shape_pos
    global shape_rotation
    x, y = shape_pos
    while check_shape_collision(shape, shape_rotation, x, y - 1):
        y -= 1
    draw_moved_shape(shape, shape_rotation, *shape_pos, shape, shape_rotation, x, y, False)
    shape_pos = (x, y)
    update()

#level_speeds = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6] + [5]*3 + [4]*3 + [3]*3 + [2]*10 + [1]
level_speeds = [1600, 1433, 1266, 1100, 933, 766, 600, 433, 266, 200] + [166]*3 + [133]*3 + [100]*3 + [66]*10 + [33]

# calls update() on loop
def time_loop():
    global game_running
    if game_running:
        global level_speeds
        global level
        update()
        turtle.ontimer(time_loop, level_speeds[min(level, 29)])


 

init_game()




# add all of control keys to the list for later unbinding
onkey_hook = turtle.onkey
def onkey_hooked(fun, key):
    global used_keys
    used_keys.append(key)
    onkey_hook(fun, key)
turtle.onkey = onkey_hooked

setup_controls()

turtle.onkey = onkey_hook




time_loop()

turtle.listen()

turtle.mainloop()
