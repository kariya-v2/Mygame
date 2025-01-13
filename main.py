import pygame
import random

# ゲームの初期設定
pygame.init()

# ウィンドウサイズ
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("エンドレスジャンプゲーム")

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# プレイヤーの設定
player_width = 50
player_height = 50
player_x = 50
player_y = HEIGHT - player_height
player_y_change = 0
gravity = 0.5
jump_strength = -10
is_jumping = False

# 障害物の設定
obstacle_width = 50
obstacle_height = 50
obstacles = []
obstacle_speed = 5
obstacle_timer = 0
obstacle_interval = 1500  # 障害物生成間隔（ミリ秒）

# スコア
score = 0
font = pygame.font.Font(None, 36)

# ゲームループ
clock = pygame.time.Clock()
running = True
while running:
    window.fill(WHITE)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_y_change = jump_strength
                is_jumping = True

    # プレイヤーの動き
    player_y_change += gravity
    player_y += player_y_change

    # 地面に触れる処理
    if player_y >= HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_y_change = 0
        is_jumping = False

    # 障害物の生成
    obstacle_timer += clock.get_time()
    if obstacle_timer > obstacle_interval:
        obstacle_x = WIDTH
        obstacles.append((obstacle_x, HEIGHT - obstacle_height))  # 障害物の位置を追加
        obstacle_timer = 0

    # 障害物の移動
    for i in range(len(obstacles)):
        obstacles[i] = (obstacles[i][0] - obstacle_speed, obstacles[i][1])

    # 画面外の障害物を削除
    obstacles = [obs for obs in obstacles if obs[0] > -obstacle_width]

    # プレイヤーの描画
    pygame.draw.rect(window, BLACK, (player_x, player_y,
                     player_width, player_height))

    # 障害物の描画
    for obs in obstacles:
        pygame.draw.rect(
            window, RED, (obs[0], obs[1], obstacle_width, obstacle_height))

    # スコアの表示
    score += 1  # スコアを増加
    score_text = font.render("スコア: " + str(score), True, BLACK)
    window.blit(score_text, (10, 10))

    # 衝突判定
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obs in obstacles:
        obs_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obs_rect):
            running = False  # ゲームオーバー

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
