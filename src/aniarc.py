import pygame
import os
import glob
from moviepy.editor import VideoFileClip


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
    

    #找到資料夾(測試
    pygame.init()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(base, "samples", "run_cycle")
    frames = load_seq(folder)

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

    #圖片大小/視窗大小 = 相對比例(用於縮放)
    scale = min(win_w / img_w, win_h / img_h, 1.0)

    # 計算 new size of img
    new_size = (int(img_w * scale), int(img_h * scale))
    
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

    # game logic
        if playing:
            current = (current + 1) % len(frames)
        
        # 獲取 Resize img (scaled = resized img)
        scaled = pygame.transform.smoothscale(frames[current], new_size)

        # 獲取置中座標
        x = (win_w - new_size[0]) // 2
        y = (win_h - new_size[1]) // 2

        # 將視窗清成被景色
        screen.fill((30, 30, 30))
        
        # 將圖片寫入視窗
        screen.blit(scaled, (x, y))

        # 寫入現在的frame
        current_frame = f"{current + 1} / {len(frames)}"
        text = font.render(current_frame, True, (255, 255, 255))
        screen.blit(text, (15, 20))

        # 反轉/顯示圖片
        pygame.display.flip()

        # 限制每一幀應為1/24秒，即24pfs
        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()