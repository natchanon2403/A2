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

def setup():
    size(400, 460)
    init_game()

def init_game():
    global board, target_final_color, moves_left, game_state, selected_color
    
    # สร้างกระดาน
    board = []
    row_idx = 0
    while row_idx < GRID_ROWS:
        new_row = []
        col_idx = 0
        while col_idx < GRID_COLS:
            random_color = random.choice(COLORS)
            new_row.append(random_color)
            col_idx += 1
            
        board.append(new_row)
        row_idx += 1
        
    # รีเซ็ตค่าตัวแปรสำหรับเริ่มเกมใหม่
    target_final_color = random.choice(COLORS)
    moves_left = 12
    game_state = "PLAYING"
    selected_color = None

def spread(start_x, start_y, target_colour, new_colour):
    # ถ้าสีเหมือนเดิมอยู่แล้วไม่ต้องทำอะไร
    if target_colour == new_colour:
        return
    
    # ใช้ List เพื่อจำตำแหน่งที่ต้องตรวจสอบ (Flood fill)
    points_to_check = [(start_x, start_y)]
    
    while len(points_to_check) > 0:
        current_x, current_y = points_to_check.pop()
        
        # ตรวจสอบว่าพิกัดไม่ออกนอกกระดาน
        is_x_valid = (0 <= current_x < GRID_COLS)
        is_y_valid = (0 <= current_y < GRID_ROWS)
        
        if is_x_valid and is_y_valid:
            if board[current_y][current_x] == target_colour:
                board[current_y][current_x] = new_colour
                
                # นำช่องรอบๆ 4 ทิศใส่เข้าไปใน Stack
                points_to_check.append((current_x + 1, current_y)) # ขวา
                points_to_check.append((current_x - 1, current_y)) # ซ้าย
                points_to_check.append((current_x, current_y + 1)) # ล่าง
                points_to_check.append((current_x, current_y - 1)) # บน

def check_win():
    row_idx = 0
    while row_idx < GRID_ROWS:
        col_idx = 0
        while col_idx < GRID_COLS:
            current_block = board[row_idx][col_idx]
            if current_block != target_final_color:
                return False # ถ้าเจอสีที่ไม่ตรงเป้าหมาย แปลว่ายังไม่ชนะ
            col_idx += 1
        row_idx += 1
        
    return True # สีตรงเป้าหมายทุกช่อง

def change_colour(start_x, start_y, new_colour):
    global moves_left, game_state, save_status_msg
    
    if game_state != "PLAYING": 
        return
    
    save_status_msg = ""
    old_colour = board[start_y][start_x]
    
    # เช็คก่อนว่าไม่ได้คลิกสีเดิม
    if old_colour != new_colour:
        spread(start_x, start_y, old_colour, new_colour)
        moves_left -= 1
        
        # ตรวจสอบสถานะเกมหลังจากการเปลี่ยนสี
        if check_win():
            game_state = "WON"
        elif moves_left <= 0:
            game_state = "LOST"

def get_color_fill(colour):
    # ใช้ Dictionary เพื่อจับคู่สี
    color_rgb = {
        "RED": (255, 80, 80),
        "GREEN": (80, 255, 80),
        "BLUE": (80, 80, 255),
        "YELLOW": (255, 255, 80)
    }
    
    # ดึงค่า RGB มาจาก Dictionary (ถ้าไม่มีค่าให้เป็นสีดำกัน error)
    r, g, b = color_rgb.get(colour, (0, 0, 0))
    fill(r, g, b)

def draw_hud():
    # แถบแสดงสถานะด้านล่าง
    fill(0)
    textSize(14)
    text("Moves Left: " + str(moves_left), 10, 345)
    text("Target:", 135, 345)
    
    # วาดเป้าหมาย
    get_color_fill(target_final_color)
    stroke(0)
    ellipse(195, 340, 20, 20)
    
    # ข้อความตอนจบเกม
    if game_state == "WON":
        fill(0, 200, 0)
        textSize(40)
        text("YOU WIN!", 110, 160)
    elif game_state == "LOST":
        fill(200, 0, 0)
        textSize(40)
        text("GAME OVER", 90, 160)
