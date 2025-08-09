import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ trò chơi
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏃 Trò Chơi Chạy Kiểu Flash")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Nhân vật chạy
player = pygame.Rect(100, HEIGHT // 2, 50, 50)
player_speed = 5

# Chướng ngại vật
obstacles = []
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 7

# Điểm số
score = 0
font = pygame.font.Font(None, 36)

# Âm thanh
jump_sound = pygame.mixer.Sound("jump.wav")

# Hàm hiển thị điểm số
def draw_score():
    score_text = font.render(f"Điểm: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Hàm tạo chướng ngại vật
def create_obstacle():
    x = random.randint(WIDTH, WIDTH + 200)
    y = random.randint(0, HEIGHT - obstacle_height)
    return pygame.Rect(x, y, obstacle_width, obstacle_height)

# Vòng lặp chính
running = True
while running:
    screen.fill(BLACK)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Di chuyển nhân vật
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= player_speed
        jump_sound.play()
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += player_speed

    # Tạo chướng ngại vật
    if random.randint(1, 100) > 98:
        obstacles.append(create_obstacle())

    # Di chuyển chướng ngại vật
    for obstacle in obstacles[:]:
        obstacle.x -= obstacle_speed
        if obstacle.right < 0:
            obstacles.remove(obstacle)
            score += 1

    # Va chạm
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            running = False

    # Vẽ nhân vật và chướng ngại vật
    pygame.draw.rect(screen, RED, player)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)

    # Hiển thị điểm số
    draw_score()

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(FPS)

# Kết thúc trò chơi
pygame.quit()
