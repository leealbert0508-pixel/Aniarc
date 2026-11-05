import pygame
import os
import glob


def load_seq(folder):
    img_seq = sorted(glob.glob(os.path.join(folder, "*.png")))
    frames = []
    for img in img_seq:
        frames.append(pygame.image.load(img))
    return frames

def main():
    #找到資料夾(測試
    pygame.init()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(base, "samples", "run_cycle")
    frames = load_seq(folder)

    #創建螢幕
    screen = pygame.display.set_mode(frames[0].get_size())
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
            if event.key == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current = (current + 1)%len(frames)
            elif event.key == pygame.K_LEFT:
                current = (current - 1) % len(frames)
            elif event.key == pygame.K_SPACE:
                # change the result(true and false)
                playing = not playing

        # game logic
        if playing:
            current = (current + 1) % len(frames)
        screen.bilt(frames[current], (0, 0))
        pygame.display.filp()

        clock.tick(24)

    pygame.quit()

if __name__ == "__main__":
    main()