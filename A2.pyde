import random

GRID_COLS = 10 # จำนวนช่องแนวนอน
GRID_ROWS = 8  # จำนวนช่องแนวตั้ง
BLOCK_SIZE = 40
COLORS = ["RED", "GREEN", "BLUE", "YELLOW"]

# ตัวแปรระบบของเกม
board = []
target_final_color = ""
moves_left = 12
game_state = "PLAYING"
selected_color = None

# สร้างกระดาน
def create_column(x):
    if x >= GRID_COLS: # เปลี่ยนเป็นเช็คแนวนอน
        return []
    return [random.choice(COLORS)] + create_column(x + 1)

def create_row(y):
    global board
    if y >= GRID_ROWS: # เปลี่ยนเป็นเช็คแนวตั้ง
        return
    board.append(create_column(0))
    create_row(y + 1)

def init_game():
    global board, target_final_color, moves_left, game_state, selected_color
    board = []
    create_row(0)
    target_final_color = random.choice(COLORS)
    moves_left = 12
    game_state = "PLAYING"
    selected_color = None

init_game()

# วาดกราฟิก
def get_color_fill(colour):
    if colour == "RED": fill(255, 80, 80)
    elif colour == "GREEN": fill(80, 255, 80)
    elif colour == "BLUE": fill(80, 80, 255)
    elif colour == "YELLOW": fill(255, 255, 80)

def draw_block(x, y, sizee, colour):
    get_color_fill(colour)
    stroke(255)
    rect(x * sizee, y * sizee, sizee, sizee)

def draw_grid_recursive(x, y):
    if y >= GRID_ROWS: return # เช็คแนวตั้ง
    if x >= GRID_COLS:        # เช็คแนวนอน
        draw_grid_recursive(0, y + 1)
        return
    draw_block(x, y, BLOCK_SIZE, board[y][x])
    draw_grid_recursive(x + 1, y)


def change_colour(colour):

# parameter colour(str)

# return -

pass


def check_spread(x,y,colour):

# parameter x(int),y(int),colour(str)

# return boolean(True/Flase)

pass

def setup():



