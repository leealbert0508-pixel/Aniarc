import pygame
import os
import glob


def load_seq(folder):
    img_seq = sorted(glob.glob(os.path.join(folder, "*.png")))
    frames = []
    for img in img_seq:
        frames.append(pygame.image.load(img))
    return frames

def get_user_screen_size():
    info = pygame.display.Info()
    screen_w = info.current_w
    screen_h = info.current_h
    width = screen_w*0.7
    height = screen_h*0.7
    return (height, width)

def main():
    #找到資料夾(測試
    pygame.init()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(base, "samples", "run_cycle")
    frames = load_seq(folder)

    #創建螢幕
    WINDOW_SIZE = get_user_screen_size()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Aniarc")
    clock = pygame.time.Clock()

    #起始frame
    current = 0
    playing = False

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
                    current = (current - 1) % len(frames)
                elif event.key == pygame.K_SPACE:
                    # change the result(true and false)
                    playing = not playing
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # game logic
        if playing:
            current = (current + 1) % len(frames)
        screen.blit(frames[current], (0, 0))
        pygame.display.flip()

        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()