import random
import os

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
save_status_msg = ""

def setup():
    size(400, 460)
    init_game()

def init_game():
    global board, target_final_color, moves_left, game_state, selected_color, save_status_msg
    
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
    save_status_msg = ""

def save_game():
    global save_status_msg
    try:
        with open("savegame.txt", "w") as file:
            file.write(target_final_color + "\n")
            file.write(str(moves_left) + "\n")
            file.write(str(selected_color) + "\n")
            
            row_idx = 0
            while row_idx < GRID_ROWS:
                row_string = ",".join(board[row_idx])
                file.write(row_string + "\n")
                row_idx += 1
                
        save_status_msg = "SAVED!"
    except:
        save_status_msg = "SAVE ERROR!"

def load_game():
    global board, target_final_color, moves_left, selected_color, game_state, save_status_msg
    
    if not os.path.exists("savegame.txt"):
        save_status_msg = "NO SAVE FILE!"
        return
        
    try:
        with open("savegame.txt", "r") as file:
            lines = file.readlines()
            
        target_final_color = lines[0].strip()
        moves_left = int(lines[1].strip())
        
        # จัดการเรื่องสีที่ถูกเลือกค้างไว้
        saved_color = lines[2].strip()
        if saved_color == "None":
            selected_color = None
        else:
            selected_color = saved_color
            
        # โหลดกระดาน
        board = []
        row_idx = 0
        while row_idx < GRID_ROWS:
            color_list = lines[row_idx + 3].strip().split(",")
            board.append(color_list)
            row_idx += 1
            
        game_state = "PLAYING"
        save_status_msg = "LOADED!"
    except:
        save_status_msg = "LOAD ERROR!"

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
        "RED": (255, 130, 130),
        "GREEN": (130, 215, 150),
        "BLUE": (140, 190, 255),
        "YELLOW": (255, 225, 120)
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

    # โชว์ข้อความ Save / Load
    fill(80)
    textSize(12)
    text("[S] Save  [L] Load", 225, 345)
    
    fill(0, 150, 0)
    text(save_status_msg, 335, 345)
    
    # ข้อความตอนจบเกม
    if game_state == "WON":
        fill(0, 200, 0)
        textSize(40)
        text("YOU WIN!", 110, 160)
    elif game_state == "LOST":
        fill(200, 0, 0)
        textSize(40)
        text("GAME OVER", 90, 160)

def keyPressed():
    # ใช้คำสั่ง in ทำให้เช็คตัวเล็กหรือตัวใหญ่ได้ในบรรทัดเดียว
    if key in ('s', 'S'):
        save_game()
    elif key in ('l', 'L'):
        load_game()

def mousePressed():
    global selected_color, save_status_msg
    
    if game_state != "PLAYING":
        # ถ้าจบเกมแล้วคลิก ให้เริ่มเกมใหม่เลย
        init_game()
        return

    clicked_on_button = False
    btn_idx = 0
    
    # ตรวจสอบว่าผู้เล่นคลิกโดนปุ่มเลือกสีหรือไม่
    while btn_idx < len(COLORS):
        btn_x = 50 + (btn_idx * 100)
        btn_y = 400
        
        in_x_range = abs(mouseX - btn_x) <= 25
        in_y_range = abs(mouseY - btn_y) <= 25
        
        if in_x_range and in_y_range:
            selected_color = COLORS[btn_idx]
            clicked_on_button = True
            save_status_msg = ""
            break # เจอแล้วหยุดเช็คปุ่มอื่น
            
        btn_idx += 1
            
    # ถ้าไม่ได้คลิกปุ่มสี แต่มีสีถูกเลือกไว้อยู่แล้ว ให้ตรวจสอบการคลิกในกระดาน
    if not clicked_on_button and selected_color is not None:
        mouse_in_board = (0 <= mouseX < 400) and (0 <= mouseY < 320)
        
        if mouse_in_board:
            grid_col = int(mouseX / BLOCK_SIZE)
            grid_row = int(mouseY / BLOCK_SIZE)
            change_colour(grid_col, grid_row, selected_color)

def draw():
    background(245)
    
    # วาดกระดานหลัก
    row_idx = 0
    while row_idx < GRID_ROWS:
        col_idx = 0
        while col_idx < GRID_COLS:
            current_color = board[row_idx][col_idx]
            get_color_fill(current_color)
            
            stroke(255)
            block_x = col_idx * BLOCK_SIZE
            block_y = row_idx * BLOCK_SIZE
            rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)
            
            col_idx += 1
        row_idx += 1
            
    # วาดปุ่มเลือกสี 4 สีด้านล่าง
    btn_idx = 0
    while btn_idx < len(COLORS):
        btn_color = COLORS[btn_idx]
        get_color_fill(btn_color)
        
        if btn_color == selected_color:
            stroke(255)
            strokeWeight(3) # ทำไฮไลท์ให้ปุ่มที่โดนเลือก
        else:
            stroke(0)
            strokeWeight(1)
            
        btn_x = 50 + (btn_idx * 100)
        btn_y = 400
        ellipse(btn_x, btn_y, 50, 50)
        
        btn_idx += 1
        
    # รีเซ็ตความหนาเส้น และเรียกวาด UI
    strokeWeight(1)
    draw_hud()
