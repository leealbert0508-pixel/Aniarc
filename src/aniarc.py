import pygame
import os
import glob
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog

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
    def __init__(self, ox, oy):
        # Get original position
        self.ox = ox
        self.oy = oy

    def to_screen(self, x, y, scale):
         return x + self.ox * scale, y + self.oy * scale
    
    def draw(self, screen, x, y, scale, r):
        sx, sy = self.to_screen(x, y, scale)
        pygame.draw.circle(screen, (255, 0, 0), (int(sx), int(sy)), r)
    
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

    #繪製調整dot大小的條
    minus_btn = pygame.Rect(90, 9, 32, 32)
    plus_btn = pygame.Rect(170, 9, 32, 32)
    
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

    # stored the dot
    dots = {}
    dot_r = 5

    # History
    history = []

    # Game Loop
    running = True
    while running:

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current = (current + 1)%len(frames)
                elif event.key == pygame.K_LEFT:
                    current = (current - 1)%len(frames)
                elif event.key == pygame.K_SPACE:
                    # change the result(true and false)
                    playing = not playing
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and history:
                    action = history.pop()
                    if action[0] == 'add':
                        dots[action[1]].pop()
                    elif action[0] == "del":
                        dots[action[1]].insert(action[2], action[3])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and edit_btn.collidepoint(event.pos):
                edit_mode = not edit_mode

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
            # add dots
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and edit_mode == True and pygame.Rect(x, y, new_size[0], new_size[1]).collidepoint(event.pos):
                mx, my = event.pos

            # change dot size


            # screen size to image size
                ox = (mx - x) / scale
                oy = (my - y) / scale

                dots.setdefault(current, []).append(Dot(ox, oy))

                # stored dots history
                history.append(('add', current))
                

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
        if playing:
            current = (current + 1) % len(frames)
        #print(current)

        # 獲取 Resize img (scaled = resized img)
        scaled = pygame.transform.smoothscale(frames[current], new_size)

        # 將視窗清成被景色
        screen.fill((30, 30, 30))
        
        # 將圖片寫入視窗
        screen.blit(scaled, (x, y))

        for d in dots.get(current, []):
            d.draw(screen, x, y, scale, dot_r)

        # 畫工具列
        pygame.draw.rect(screen, (45, 45, 45), (0, 0, win_w, tool_bar_h))
        if edit_mode == True:
            btn_color = (60, 120, 220)
        else:
            btn_color = (80, 80, 80)
        pygame.draw.rect(screen, btn_color, edit_btn)
        btn_text = font.render("Edit", True, (255, 255, 255))
        screen.blit(btn_text, (edit_btn.x + 8, edit_btn.y + 4))
        
        # Draw -/+button
        pygame.draw.rect(screen, (80, 80, 80), minus_btn)
        minus_text = font.render("-", True, (255, 255, 255))
        screen.blit(minus_text, (minus_btn.x + 10, minus_btn.y + 4))
        
        pygame.draw.rect(screen, (80, 80, 80), plus_btn)
        plus_text = font.render("+", True, (255, 255, 255))
        screen.blit(plus_text, (plus_btn.x + 10, plus_btn.y + 4))

        #Print current dot size
        if dot_r != 10:
            current_dots = font.render(str(f"0{dot_r}"), True, (255, 255, 255))
            screen.blit(current_dots, (((plus_btn.x + minus_btn.x)//2) + 4, 15))
        else:
            current_dots = font.render(str(dot_r), True, (255, 255, 255))
            screen.blit(current_dots, (((plus_btn.x + minus_btn.x)//2) + 4, 15))
        
    # 寫入現在的frame
        # 二位數的情況
        if len(frames) > 9 and len(frames) < 100:
            if current + 1 < 10:
                #print("幀數是個位數")
                current_frame = f"0{current + 1} / {len(frames)}"
            elif current + 1 > 9:
                #print("幀數是二位數")
                current_frame = f"{current + 1} / {len(frames)}"

        #三位數的情況
        elif len(frames) > 99 and len(frames) < 1000:
            if current + 1 < 10:
                current_frame = f"00{current + 1} / {len(frames)}"
            elif current + 1 > 9 and current + 1< 100:
                current_frame = f"0{current + 1} / {len(frames)}"
            elif current + 1 > 99:
                current_frame = f"{current + 1} / {len(frames)}"
        
        # 一位數的情況
        else:
            current_frame = f"0{current + 1} / {len(frames)}"
            
        text = font.render(current_frame, True, (255, 255, 255))
        screen.blit(text, (15, 60))
        
        # 反轉/顯示圖片
        pygame.display.flip()

        # 限制每一幀應為1/24秒，即24pfs
        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()