import pygame
import random

# pygameの初期化
pygame.init()

# 定数の設定
WIDTH, HEIGHT = 800, 600
FPS = 60
CLAY_RADIUS = 17
TARGET_RADIUS = 20
BULLET_RADIUS = 10  # 灰色の玉の半径
SCORE_FONT_SIZE = 36
GRAVITY = 0.5  # 重力加速度 (Y方向)
TIME_LIMIT = 40  # 制限時間（秒）
TARGET_DROP_INTERVAL = 10000  # 青い的が降り始める間隔（ミリ秒）
BULLET_UPDATE_INTERVAL = 10000  # 灰色の弾が増える間隔（ミリ秒）

# 色の設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # 青い的の色
GREEN = (0, 255, 0)  # ボタンの色
GRAY = (192, 192, 192)  # 灰色の弾の色

# 画面の作成
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clay Shooting Game")

# フォントの設定
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

# クレーのクラス定義


class Clay:
    def __init__(self):
        self.x = random.randrange(0, 200, 50)  # クレーはランダムに出現
        self.y = HEIGHT  # 初期Y座標（ウィンドウの底）
        self.velocity_x = random.uniform(0, 9)  # X方向の一定の初速度
        self.velocity_y = -25 + random.uniform(0, 9)  # 上向きの初速度（ランダムでばらつきあり）
        # 画像をロード
        clay_image = pygame.image.load('images/money.png').convert_alpha()

        # 新しいサイズを指定（例えば、幅100px、高さ100pxに変える場合）
        new_size = (40, 40)  # 幅と高さを指定するタプル
        self.clayimage = pygame.transform.scale(
            clay_image, new_size)  # 画像をリサイズ

        self.radius = self.clayimage.get_width() // 2  # 画像の半径
        self.alive = True  # クレーが生きているかどうか

    def update(self):
        if self.alive:
            self.velocity_y += GRAVITY  # Y成分に重力を加える
            self.x += self.velocity_x  # X成分の移動
            self.y += self.velocity_y  # Y成分の移動

            # 画面の外に出たら自分を非表示にする（aliveをFalseにする）
            if self.x > WIDTH or self.y > HEIGHT:
                self.alive = False

    def draw(self, surface):
        if self.alive:  # aliveの場合のみ描画
            surface.blit(self.clayimage, (self.x - self.radius,
                         self.y - self.radius))  # 画像を描画


# 青い的のクラス定義
class Target:
    def __init__(self):
        self.image_path = 'images/watch.png'  # 画像のパス
        self.width = TARGET_RADIUS * 4  # 画像の幅（円の直径）
        self.height = TARGET_RADIUS * 4  # 画像の高さ（円の直径）

        # 画像のロードとサイズ変更
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))  # 画像のサイズを変更

        self.x = random.randint(
            0 + TARGET_RADIUS, WIDTH - TARGET_RADIUS)  # ランダムなX位置
        self.y = 0  # 初期Y座標（ウィンドウの上）
        self.velocity_y = 3  # 下向きの一定の速度
        self.alive = True  # ターゲットが生きているかどうか

    def update(self):
        if self.alive:
            self.y += self.velocity_y  # Y成分の移動

            # 画面の外に出たら自分を非表示にする（aliveをFalseにする）
            if self.y > HEIGHT:
                self.alive = False

    def draw(self, surface):
        if self.alive:  # aliveの場合のみ描画
            # 画像を描画（位置を考慮してrectを指定)
            rect = self.image.get_rect(center=(self.x, self.y))  # 中心を指定
            surface.blit(self.image, rect)  # 画像を描画


class Bullet:
    def __init__(self):
        self.image_path = 'images/egg.png'  # 画像のパス
        self.width = BULLET_RADIUS * 2  # 画像の幅（円の直径）
        self.height = BULLET_RADIUS * 2  # 画像の高さ（円の直径）

        # 画像のロードとサイズ変更
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))  # 画像のサイズを変更

        self.x = random.randrange(0, WIDTH)  # X位置はランダム
        self.y = random.randrange(0, HEIGHT)  # Y位置はランダム
        self.velocity_x = random.uniform(-5, 5)  # X方向の速度（左または右へ、ランダム）
        self.velocity_y = random.uniform(-5, 5)  # Y方向の速度（上下へ、ランダム）
        self.alive = True  # 玉が生きているかどうか

    def update(self):
        if self.alive:
            self.x += self.velocity_x  # X成分の移動
            self.y += self.velocity_y  # Y成分の移動

            # 画面の端に衝突したか確認
            if self.x < BULLET_RADIUS or self.x > WIDTH - BULLET_RADIUS:
                self.velocity_x *= -1  # X速度を反転

            if self.y < BULLET_RADIUS or self.y > HEIGHT - BULLET_RADIUS:
                self.velocity_y *= -1  # Y速度を反転

    def draw(self, surface):
        if self.alive:  # aliveの場合のみ描画
            # 画像を描画（位置を考慮してrectを指定)
            rect = self.image.get_rect(center=(self.x, self.y))  # 中心を指定
            surface.blit(self.image, rect)  # 画像を描画

# スタート画面を表示する関数


def display_start_screen():
    screen.fill(WHITE)
    title_surface = score_font.render("Clay Shooting Game", True, (0, 0, 0))
    start_button = pygame.Rect(
        (WIDTH // 2 - 100, HEIGHT // 2 - 20), (200, 40))  # スタートボタンのサイズと位置
    pygame.draw.rect(screen, GREEN, start_button)  # スタートボタンを描画
    start_text_surface = score_font.render("Start", True, (255, 255, 255))

    # スタートボタンのテキストを中央に描画
    screen.blit(start_text_surface, (WIDTH // 2 -
                start_text_surface.get_width() // 2, HEIGHT // 2 - 15))
    screen.blit(title_surface, (WIDTH // 2 -
                title_surface.get_width() // 2, HEIGHT // 2 - 80))

    pygame.display.flip()  # 画面を更新


# ゲーム終了後に結果を表示し、リスタートボタンを描画する関数
def display_game_over(score):
    screen.fill(WHITE)  # 背景を再び白に
    final_score_surface = score_font.render(
        f"Final Score: {score}", True, (0, 0, 0))
    final_time_surface = score_font.render("Time's up!", True, (0, 0, 0))

    # スコアとメッセージを画面中央に描画
    screen.blit(final_score_surface, (WIDTH // 2 -
                final_score_surface.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(final_time_surface, (WIDTH // 2 -
                final_time_surface.get_width() // 2, HEIGHT // 2 - 60))

    # リスタートボタンの描画
    restart_button = pygame.Rect(
        (WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 40))  # リスタートボタンのサイズと位置
    pygame.draw.rect(screen, GREEN, restart_button)  # リスタートボタンを描画
    restart_text_surface = score_font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text_surface, (WIDTH // 2 -
                restart_text_surface.get_width() // 2, HEIGHT // 2 + 25))

    pygame.display.flip()  # 画面を更新


# ゲームループ
running = True
game_started = False  # ゲームが開始されたかどうかのフラグ
bullets = []  # 灰色の玉のリスト
bullet_spawn_time = 0  # 玉を生成するためのタイマー
initial_bullet_count = 2  # ゲーム開始時の玉の個数

while running:
    if not game_started:
        display_start_screen()  # スタート画面を表示
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリック
                    mouse_pos = pygame.mouse.get_pos()
                    start_button = pygame.Rect(
                        (WIDTH // 2 - 100, HEIGHT // 2 - 20), (200, 40))
                    # スタートボタンがクリックされたか確認
                    if start_button.collidepoint(mouse_pos):
                        game_started = True  # ゲーム開始フラグをセット
                        bullets = [Bullet() for _ in range(
                            initial_bullet_count)]  # ゲーム開始時に玉を生成
                        bullet_spawn_time = pygame.time.get_ticks()  # タイマー開始

    else:
        # クレー、ターゲット、スコアの初期化
        clays = []
        targets = []
        score = 0
        time_remaining = TIME_LIMIT  # 残り時間の初期化
        clock = pygame.time.Clock()
        pygame.time.set_timer(
            pygame.USEREVENT, TARGET_DROP_INTERVAL)  # ターゲットが降るイベントを設定

        while game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_started = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        mouse_pos = pygame.mouse.get_pos()

                        # クレーの当たり判定を設定
                        for clay in clays:
                            distance = (
                                (mouse_pos[0] - clay.x) ** 2 + (mouse_pos[1] - clay.y) ** 2) ** 0.5
                            if distance <= CLAY_RADIUS and clay.alive:
                                clays.remove(clay)  # クレーをリストから削除
                                score += 1
                                break

                        # ターゲットの当たり判定を設定
                        for target in targets:
                            distance = (
                                (mouse_pos[0] - target.x) ** 2 + (mouse_pos[1] - target.y) ** 2) ** 0.5
                            if distance <= TARGET_RADIUS and target.alive:
                                target.alive = False  # ターゲットを消す
                                time_remaining += 10  # タイムを10秒増加
                                break

                elif event.type == pygame.USEREVENT:  # ターゲットを降らせるイベント
                    target = Target()
                    targets.append(target)

            # 新しいクレーを生成
            if random.random() < 0.02:  # 2%の確率で新しいクレーを生成
                clay = Clay()
                clays.append(clay)

            # 時間経過に応じて灰色の玉を生成
            current_time = pygame.time.get_ticks()
            if current_time - bullet_spawn_time >= BULLET_UPDATE_INTERVAL:
                bullet_spawn_time = current_time
                bullets.extend([Bullet(), Bullet()])  # 2つの玉を追加

            # マウスの位置を取得
            mouse_pos = pygame.mouse.get_pos()

            # 灰色の玉の当たり判定を設定
            for bullet in bullets:
                distance = ((mouse_pos[0] - bullet.x) **
                            2 + (mouse_pos[1] - bullet.y) ** 2) ** 0.5
                if distance <= BULLET_RADIUS and bullet.alive:
                    bullet.alive = False  # 玉を消す
                    time_remaining -= 5  # タイムを5秒減少
                    break

                    # 画面の描画
            screen.fill(WHITE)  # 背景を白に

            # 残り時間の更新と描画
            if time_remaining > 0:
                time_remaining -= 1 / FPS  # フレームごとに時間を減少させる
            else:
                game_started = False  # 残り時間がゼロになったらゲームを停止

            time_surface = score_font.render(
                f"Time: {int(time_remaining)}", True, (0, 0, 0))
            screen.blit(time_surface, (10, 10))  # タイムを左上に描画

            # ターゲットの更新と描画
            for target in targets:
                target.update()  # ターゲットの位置を更新
                target.draw(screen)  # ターゲットを描画

            # クレーの更新と描画
            for clay in clays:
                clay.update()  # クレーの更新
                clay.draw(screen)  # クレーを描画

            # 灰色の玉の更新と描画
            for bullet in bullets:
                bullet.update()  # 玉の位置を更新
                bullet.draw(screen)  # 玉を描画

            # スコアの表示
            score_surface = score_font.render(
                f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_surface, (10, 50))  # スコアを左上に描画

            # 描画の更新
            pygame.display.flip()
            clock.tick(FPS)  # フレームレートの制御

        # ゲームオーバーの表示
        display_game_over(score)

        # リスタート待機
        while not game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_started = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        mouse_pos = pygame.mouse.get_pos()
                        restart_button = pygame.Rect(
                            (WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 40))
                        # リスタートボタンがクリックされたか確認
                        if restart_button.collidepoint(mouse_pos):
                            game_started = True  # ゲームをリスタート
                            break

            if not running:
                break  # メインループを抜ける

# ゲームを終了
pygame.quit()
