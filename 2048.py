###########################################
#
# 2048 recreation by RandomsongV2
#
###########################################
#
# Controls:
# 
# Arrow keys
#
###########################################






import turtle
import random



turtle.title('2048')
turtle.setup(512, 512, 720, 160)
turtle.hideturtle()
turtle.tracer(0)
turtle.penup()
turtle.bgcolor('#000000')
turtle.color('#FFFFFF')

turtle.goto(-264, -264)
turtle.fillcolor("#ffffff")
turtle.begin_fill()
turtle.goto(264, -264)
turtle.goto(264, 264)
turtle.goto(-264, 264)
turtle.end_fill()

colors = [
        '#f9f9f9',
        '#dfd5cb', '#ddd1b7', '#f2b179', '#f59563',
        '#f37f58', '#f45e3b', '#edce71', '#edcc61',
        '#efc851', '#ebc53e', '#ecc22e', '#ec9400',
        '#ff6600', '#fc3500', '#db0d00'
          ]

# tiles are stored as [1, 2, 3, 4] instead of [2, 4, 8, 16]
# these lists are to get what to print
scores = [
        None,
        2, 4, 8, 16,
        32, 64, 128, 256,
        512, 1024, 2048, 4096,
        8192, 16384, 32768
          ]
text_size = [
        None,
        80, 80, 80, 50,
        50, 50, 33, 33,
        33, 25, 25, 25,
        25, 20, 20
        ]
text_offset = [
        None,
        -5, -5, -5, 20,
        20, 20, 34, 34,
        34, 41, 41, 41,
        41, 44, 44
        ]

board = [[0 for i in range(4)] for j in range(4)]
tile_count = 0 # how much tiles does board contain

def draw_pixel(i, j):
    global score_count
    global board
    global text_size
    x, y = (i - 2) << 7, (j - 2) << 7 # i * 256 - 512
    turtle.fillcolor(colors[board[i][j]])
    turtle.goto(x + 8, y + 8)
    turtle.begin_fill()
    turtle.goto(x + 120, y + 8)
    turtle.goto(x + 120, y + 120)
    turtle.goto(x + 8, y + 120)
    turtle.end_fill()
    if board[i][j]: # != 0
        turtle.goto(x + 64, y + text_offset[board[i][j]])
        turtle.write(scores[board[i][j]], align = 'center', font = ['', text_size[board[i][j]]])

# checks for pose before the one with a tile
# for example [(0, 1), (1, 1), (2, 1)] will return (1, 1) if (2, 1) is a tile and (0, 1) and (1, 1) are empty
def check_for_first(poses):
    global board
    pos = False
    for i in range(len(poses)):
        if board[poses[i][0]][poses[i][1]]:
            break
        else:
            pos = poses[i]
    return pos
    
def spawn_tile():
    global tile_count
    global board
    if tile_count < 16:
        while True:
            x, y = random.randint(0, 3), random.randint(0, 3)
            if not board[x][y]:
                board[x][y] = random.randint(1, 2)
                draw_pixel(x, y)
                tile_count += 1
                return

def move_up(): # moves tiles at board[x][y] to +y
    global board
    fused = {} # to prevent multiple fuses of 1 tile on same turn
    old_board = [] # for drawing purposes
    for i in board:
        old_board.append(i[:])
    # for each tile
    for i in range(4):
        for j in range(3, -1, -1):
            if board[i][j] and j < 3:
                # gets position to put the tile to (ignoring fusing)
                pos = check_for_first([(i, x) for x in range(j, 4)][1:])
                # if pos is different from current position
                if pos:
                    # checks for fusing
                    if pos[1] < 3 and board[pos[0]][pos[1] + 1] == board[i][j] and not (pos[0], pos[1]) in fused:
                        #if it does fuse then delete current tile and increase fused tile by 1
                        board[pos[0]][pos[1] + 1] += 1
                        fused[(pos[0], pos[1])] = True
                    else:
                        #if it doesnt fuse then just move the tile to pos
                        board[pos[0]][pos[1]] = board[i][j]
                    board[i][j] = 0
                # checks for fusing
                elif board[i][j + 1] == board[i][j] and not (i, j) in fused:
                    #if it does fuse then delete current tile and increase fused tile by 1
                    board[i][j + 1] += 1
                    fused[(i, j)] = True
                    board[i][j] = 0
    # update the board visually
    for i in range(4):
        for j in range(4):
            if board[i][j] != old_board[i][j]:
                draw_pixel(i, j)
    global tile_count
    tile_count -= len(fused)
    spawn_tile()

def move_down():
    global board
    fused = {}
    old_board = []
    for i in board:
        old_board.append(i[:])
    for i in range(4):
        for j in range(4):
            if board[i][j] and j > 0:
                pos = check_for_first([(i, x) for x in range(j, -1, -1)][1:])
                if pos:
                    if pos[1] > 0 and board[pos[0]][pos[1] - 1] == board[i][j] and not (pos[0], pos[1]) in fused:
                        board[pos[0]][pos[1] - 1] += 1
                        fused[(pos[0], pos[1])] = True
                    else:
                        board[pos[0]][pos[1]] = board[i][j]
                    board[i][j] = 0
                elif board[i][j - 1] == board[i][j] and not (i, j) in fused:
                    board[i][j - 1] += 1
                    fused[(i, j)] = True
                    board[i][j] = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != old_board[i][j]:
                draw_pixel(i, j)
    global tile_count
    tile_count -= len(fused)
    spawn_tile()

def move_left():
    global board
    fused = {}
    old_board = []
    for i in board:
        old_board.append(i[:])
    for i in range(4):
        for j in range(4):
            if board[i][j] and i > 0:
                pos = check_for_first([(x, j) for x in range(i, -1, -1)][1:])
                if pos:
                    if pos[0] > 0 and board[pos[0] - 1][pos[1]] == board[i][j] and not (pos[0], pos[1]) in fused:
                        board[pos[0] - 1][pos[1]] += 1
                        fused[(pos[0], pos[1])] = True
                    else:
                        board[pos[0]][pos[1]] = board[i][j]
                    board[i][j] = 0
                elif board[i - 1][j] == board[i][j] and not (i, j) in fused:
                    board[i - 1][j] += 1
                    fused[(i, j)] = True
                    board[i][j] = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != old_board[i][j]:
                draw_pixel(i, j)
    global tile_count
    tile_count -= len(fused)
    spawn_tile()

def move_right():
    global board
    fused = {}
    old_board = []
    for i in board:
        old_board.append(i[:])
    for i in range(3, -1, -1):
        for j in range(4):
            if board[i][j] and i < 3:
                pos = check_for_first([(x, j) for x in range(i, 4)][1:])
                if pos:
                    if pos[0] < 3 and board[pos[0] + 1][pos[1]] == board[i][j] and not (pos[0], pos[1]) in fused:
                        board[pos[0] + 1][pos[1]] += 1
                        fused[(pos[0], pos[1])] = True
                    else:
                        board[pos[0]][pos[1]] = board[i][j]
                    board[i][j] = 0
                elif board[i + 1][j] == board[i][j] and not (i, j) in fused:
                    board[i + 1][j] += 1
                    fused[(i, j)] = True
                    board[i][j] = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != old_board[i][j]:
                draw_pixel(i, j)
    global tile_count
    tile_count -= len(fused)
    spawn_tile()

for i in range(4):
    for j in range(4):
        draw_pixel(i, j)

spawn_tile()

turtle.onkey(move_up, 'Up')
turtle.onkey(move_down, 'Down')
turtle.onkey(move_left, 'Left')
turtle.onkey(move_right, 'Right')
turtle.listen()

turtle.mainloop()
