import pygame
import os
import glob
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog

#color list
COLORS = [
    (255, 60, 60),
    (60, 150, 255),
    (60, 220, 100),
    (255, 220, 0),
    (200, 80, 255),
]

def input_file():
    # create file input window.
    input_window = tk.Tk()
    input_window.withdraw()

    file_path = filedialog.askopenfilename(
        title="Open image sequence or video file(gif/mp4)",
        filetypes=[("Media", "*.png *.gif *.mp4")])
    input_window.destroy()

    return file_path

class Dot:
    def __init__(self, ox, oy, color = (255, 60, 60)):
        # Get original position
        self.ox = ox
        self.oy = oy
        self.color = color

    def to_screen(self, x, y, scale):
         return x + self.ox * scale, y + self.oy * scale
    
    def draw(self, screen, x, y, scale, r):
        sx, sy = self.to_screen(x, y, scale)
        pygame.draw.circle(screen, self.color, (int(sx), int(sy)), r)
    
    def hit(self, mx, my, x, y, scale, r):
        sx, sy = self.to_screen(x, y, scale)
        return abs(mx - sx) <= r + 1 and abs(my - sy) <= r + 1

def load_seq(folder):
    img_seq = sorted(glob.glob(os.path.join(folder, "*.png")))
    frames = []
    for img in img_seq:
        frames.append(pygame.image.load(img))
    return frames

def load_video(file_path):
    clip = VideoFileClip(file_path)
    frames = []
    
    for f in clip.iter_frames():
        h, w = f.shape[:2]
        # convert data to img(frame)
        frames.append(pygame.image.frombuffer(f.tobytes(), (w, h), "RGB"))
    clip.close()
    return frames

def get_max_screen_size():
    info = pygame.display.Info()
    screen_w = info.current_w
    screen_h = info.current_h
    width = int(screen_w*0.7)
    height = int(screen_h*0.7)
    return (width, height)

def draw_button(screen, font, rect, label, active=False):
    if active:
        color = (60, 120, 220)  
    else:
        color = (80, 80, 80)
    pygame.draw.rect(screen, color, rect)
    text = font.render(label, True, (255, 255, 255))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def held_dots(dots, current):
    # if current frame not dots, find previous frames dots
    # star from current frame, go backward.
    for f in range(current, -1, -1):
        # if find dots, return the dot
        if dots.get(f):
            return dots[f]
    # if there are no dots, returen empty list
    return[]
    

def draw_trail(screen, dots, frames_count, x, y, scale):
    pts = []
    for f in range(frames_count):
        frames_dots = dots.get(f, [])
        if frames_dots:
            pts.append(frames_dots[0].to_screen(x, y, scale))
    if len(pts) >= 2:
        pygame.draw.lines(screen, (255, 200, 0), False, pts, 2)

def color_change(current_color):
    
    
    #創建點擊按鈕後的選單

    #當用戶點擊顏色按鈕時展開選單
    #當用戶點擊選單上的顏色後切換顏色
    
    return current_color

def main():
    
    #path = folder for seq/file path for gif or mp4
    path = input_file()
    if not path:
        return
    
    #初始化pygame
    pygame.init()
    # repeat
    pygame.key.set_repeat(300, 40)
    
    # get the file type
    ext = os.path.splitext(path)[1].lower()
    
    if ext in (".gif", ".mp4"):
        frames = load_video(path)
    else:
        # get only folder name of the input image
        frames = load_seq(os.path.dirname(path))

    #螢幕大小*0.7 = 軟件視窗大小
    max_w, max_h = get_max_screen_size()
    aspect = 16/9

    if max_w / max_h > aspect:
        win_h = max_h
        win_w = int(win_h * aspect)
    else:
        win_w = max_w
        win_h = int(win_w / aspect)

    #圖片大小
    img_w, img_h = frames[0].get_size()


### 工具列與按鈕

    #工具列
    tool_bar_h = 50

    #圖片大小/視窗大小 = 相對比例(用於縮放)
    scale = min(win_w / img_w, (win_h - tool_bar_h) / img_h, 1.0)

    # 計算 new size of img
    new_size = (int(img_w * scale), int(img_h * scale))

    # 獲取置中座標
    x = (win_w - new_size[0]) // 2
    y = tool_bar_h + (win_h - tool_bar_h - new_size[1]) // 2

    # Edit mode(to add dot)
    edit_mode = False
    # 繪製 botton of edit mode
    edit_btn = pygame.Rect(8, 9, 70, 32)

    #Trail Mode
    trail_mode = False
    #trail mode button
    trail_btn = pygame.Rect(215, 9, 80, 32)

    # Color changing mode
    menu_open = False

    #繪製調整dot大小的按鈕
    minus_btn = pygame.Rect(90, 9, 32, 32)
    plus_btn = pygame.Rect(170, 9, 32, 32)

    # 顏色按鈕
    color_btn = pygame.Rect(305, 9, 32, 32)
    color_menu_btn = [pygame.Rect(309, 49 + i * 28, 24, 24) for i in range(len(COLORS))]
    
    # 創建視窗(按照機算出的視窗大小)
    screen = pygame.display.set_mode((win_w, win_h))

    # 設定視窗標題
    pygame.display.set_caption("Aniarc")
    # 創建時鐘
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    # 起始frame
    current = 0
    # 設置自動撥放(默認關閉)
    playing = False
    space_held = False

    # stored the dot
    dots = {}
    dot_r = 5

    # History
    history = []

    # Current Dot Color
    current_color = (255, 60, 60)

# Game Loop
    running = True
    while running:

# event loop
    # 偵測用戶每幀內的動作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current = (current + 1)%len(frames)
                elif event.key == pygame.K_LEFT:
                    current = (current - 1)%len(frames)
                elif event.key == pygame.K_SPACE and not space_held:
                    # change the result(true and false)
                    space_held = True
                    playing = not playing
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and history:
                    action = history.pop()
                    if action[0] == 'add':
                        dots[action[1]].pop()
                    elif action[0] == "del":
                        dots[action[1]].insert(action[2], action[3])
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_held = False

            # Edit mode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and edit_btn.collidepoint(event.pos):
                edit_mode = not edit_mode

            # Trail Mode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and trail_btn.collidepoint(event.pos):
                trail_mode = not trail_mode

            #change dot size
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and minus_btn.collidepoint(event.pos):
                if dot_r > 1:
                    dot_r = dot_r - 1
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and plus_btn.collidepoint(event.pos):
                if dot_r <= 9:
                    dot_r = dot_r + 1
                else:
                    pass

            # change color
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and color_btn.collidepoint(event.pos):
                menu_open = not menu_open
                print(menu_open)

            # close menu when clicking outside it
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu_open and not color_btn.collidepoint(event.pos) and not any(rect.collidepoint(event.pos) for rect in color_menu_btn):
                menu_open = False

            # add dots
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and edit_mode == True and pygame.Rect(x, y, new_size[0], new_size[1]).collidepoint(event.pos):
                mx, my = event.pos
            # screen size to image size
                ox = (mx - x) / scale
                oy = (my - y) / scale
                dots.setdefault(current, []).append(Dot(ox, oy, current_color))
                # stored dots history
                history.append(('add', current))
                
            #remove dot
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and edit_mode:
            # button 3 == right mouse
                mx, my = event.pos
                for i, d in enumerate(dots.get(current, [])):

                    if d.hit(mx, my, x, y, scale, dot_r):
                        # stored history
                        history.append(('del', current, i, d))
                        dots[current].pop(i)
                        break
            

# game logic
    # 接收動作後與數據之後更新畫面
        if playing:
            current = (current + 1) % len(frames)

        # 獲取 Resize img (scaled = resized img)
        scaled = pygame.transform.smoothscale(frames[current], new_size)

        # 將視窗清成被景色
        screen.fill((30, 30, 30))
        
        # 將圖片寫入視窗
        screen.blit(scaled, (x, y))

        # Draw Trail
        if trail_mode:
            draw_trail(screen, dots, len(frames), x, y, scale)

        for d in held_dots(dots, current):
            d.draw(screen, x, y, scale, dot_r)

        # 畫工具列
        pygame.draw.rect(screen, (45, 45, 45), (0, 0, win_w, tool_bar_h))
        
    # Draw Button
        draw_button(screen, font, edit_btn, "Edit", edit_mode)
        draw_button(screen, font, trail_btn, "Trail", trail_mode)
        draw_button(screen, font, minus_btn, "-")
        draw_button(screen, font, plus_btn, "+")

        # Draw Color Button
        if menu_open:
            pygame.draw.rect(screen, (80, 80, 80), (305, 45, 32, len(COLORS) * 28 + 4))
            for i, rect in enumerate(color_menu_btn):
                pygame.draw.rect(screen, COLORS[i], rect)
        pygame.draw.rect(screen, current_color, color_btn)
        pygame.draw.rect(screen, (80, 80, 80), color_btn, 2)

    # Show current dot size
        current_dots = font.render(f"{dot_r:02d}", True, (255, 255, 255))
        screen.blit(current_dots, (((plus_btn.x + minus_btn.x)//2) + 4, 15))
        
    # 寫入現在的frame
        width = len(str(len(frames)))
        current_frame = f"{current + 1:0{width}d} / {len(frames)}"
        text = font.render(current_frame, True, (255, 255, 255))
        screen.blit(text, (15, 60))
        
    # 反轉/顯示圖片
        pygame.display.flip()

    # 限制每一幀應為1/24秒，即24pfs
        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()
