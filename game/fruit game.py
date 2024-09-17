import pygame
import random

# 定义常量
WIDTH, HEIGHT = 600, 800  # 游戏窗口的宽度和高度
TILE_SIZE1 = 100  # 每个方块的尺寸
ROWS1, COLS1 = 6, 6  # 游戏板的行数和列数
TILE_SIZE2 = 50  # 每个方块的尺寸
ROWS2, COLS2 = 12, 12  # 游戏板的行数和列数

WHITE = (255, 255, 255)  # 白色
BLACK = (0, 0, 0)  # 黑色
BG_COLOR = (189, 255, 126)  # 背景颜色


class MyGame:
    def __init__(self):
        super(MyGame, self).__init__()
        # 初始化 Pygame
        pygame.init()
        self.info = pygame.display.Info()
        # 创建窗口
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("玩转五水果")  # 设置窗口标题

        # 加载图案图片
        patterns1 = [pygame.image.load(f"{i}.png") for i in range(1, 6)]  # 加载1到5的图片
        patterns1 = [pygame.transform.scale(p, (TILE_SIZE1, TILE_SIZE1)) for p in patterns1]  # 将图片缩放到方块大小
        # 创建游戏板
        self.board1 = [[random.choice(patterns1) for _ in range(COLS1)] for _ in range(ROWS1)]  # 随机选择图案填充游戏板

        patterns2 = [pygame.image.load(f"{i}.png") for i in range(1, 6)]  # 加载1到5的图片
        patterns2 = [pygame.transform.scale(p, (TILE_SIZE2, TILE_SIZE2)) for p in patterns2]  # 将图片缩放到方块大小
        # 创建游戏板
        self.board2 = [[random.choice(patterns2) for _ in range(COLS2)] for _ in range(ROWS2)]  # 随机选择图案填充游戏板
        self.selected = []  # 用于存储用户选择的方块
        # 定义一个音效
        self.hover_sound = pygame.mixer.Sound('./sound/anjian.mp3')
        self.hover_sound.set_volume(0.5)
        # 定义音效flag
        self.hover_flag = [0, 0, 0, 0, 0]
        self.state = 1
        self.countdown = 200  # 设置倒计时为200秒

    def init(self):  # 游戏开始界面
        self.info = pygame.display.Info()
        background = pygame.image.load("back.png")
        self.screen.blit(background, (0, 0))
        x, y = self.info.current_w / 2, self.info.current_h / 2
        font = pygame.font.SysFont('华文行楷', 100)
        text = font.render("玩转五水果", True, (204, 204, 255))
        self.screen.blit(text, (x - text.get_width() / 2, (y - text.get_height() / 2) / 2))

        # 创建一个按钮不显示
        pos = pygame.mouse.get_pos()
        button = self.create_button("测 试 范 例")
        button_x, button_y = x - button.get_width() / 2, y - button.get_height() / 2

        # 检查鼠标是否在按钮上
        rect = button.get_rect()
        if self.check_mouse(pos, rect, button_x, button_y):
            play = self.create_button("开 始 游 戏", color=(182, 208, 226))
            if not self.hover_flag[0]:
                self.hover_sound.play()
            self.hover_flag[0] = 1
        else:
            self.hover_flag[0] = 0
            play = self.create_button("开 始 游 戏")

        if self.check_mouse(pos, rect, button_x, button_y, 100):
            close = self.create_button("关 闭 游 戏", color=(182, 208, 226))
            if not self.hover_flag[1]:
                self.hover_sound.play()
            self.hover_flag[1] = 1
        else:
            self.hover_flag[1] = 0
            close = self.create_button("关 闭 游 戏")

        self.screen.blit(play, (button_x, button_y))
        self.screen.blit(close, (button_x, button_y + 100))
        pygame.display.update()

    def create_button(self, text, color=(255, 255, 255), font='SmileySans-Oblique.ttf', size=40,
                      background=None):  # 创建按钮
        button_font = pygame.font.Font(font, size)
        button = button_font.render(text, True, color, background)
        return button

    def check_mouse(self, pos, rect, x, y, offset=0):
        a = x < pos[0] < x + rect[2]
        b = y + offset < pos[1] < y + offset + rect[3]
        return a and b

    def draw_board1(self):
        for row in range(ROWS1):
            for col in range(COLS1):
                tile = self.board1[row][col]
                if tile is not None:
                    self.screen.blit(tile, (col * TILE_SIZE1, row * TILE_SIZE1))  # 在屏幕上绘制方块

    def draw_board2(self):
        for row in range(ROWS2):
            for col in range(COLS2):
                tile = self.board2[row][col]
                if tile is not None:
                    self.screen.blit(tile, (col * TILE_SIZE2, row * TILE_SIZE2))  # 在屏幕上绘制方块

    def check_match1(self):
        if len(self.selected) == 3:  # 如果用户选择了三个方块
            r1, c1 = self.selected[0]  # 获取第一个方块的行和列
            r2, c2 = self.selected[1]  # 获取第二个方块的行和列
            r3, c3 = self.selected[2]  # 获取第三个方块的行和列
            if self.board1[r1][c1] == self.board1[r2][c2] == self.board1[r3][c3]:  # 如果三个方块图案相同
                self.board1[r1][c1] = None  # 将第一个方块置为空
                self.board1[r2][c2] = None  # 将第二个方块置为空
                self.board1[r3][c3] = None  # 将第三个方块置为空
            self.selected.clear()  # 清空选择列表

    def check_match2(self):
        if len(self.selected) == 3:  # 如果用户选择了三个方块
            r1, c1 = self.selected[0]  # 获取第一个方块的行和列
            r2, c2 = self.selected[1]  # 获取第二个方块的行和列
            r3, c3 = self.selected[2]  # 获取第三个方块的行和列
            if self.board2[r1][c1] == self.board2[r2][c2] == self.board2[r3][c3]:  # 如果三个方块图案相同
                self.board2[r1][c1] = None  # 将第一个方块置为空
                self.board2[r2][c2] = None  # 将第二个方块置为空
                self.board2[r3][c3] = None  # 将第三个方块置为空
            self.selected.clear()  # 清空选择列表

    def check_game_over1(self):  # 检查游戏结束(AIGC)
        for row in range(ROWS1):
            for col in range(COLS1):
                if self.board1[row][col] is not None:  # 如果游戏板上有方块
                    return False  # 游戏未结束
        return True  # 游戏结束

    def check_game_over2(self):  # 检查游戏结束(AIGC)
        for row in range(ROWS2):
            for col in range(COLS2):
                if self.board2[row][col] is not None:  # 如果游戏板上有方块
                    return False  # 游戏未结束
        return True  # 游戏结束

    def choose(self):  # 选择界面
        self.info = pygame.display.Info()
        background = pygame.image.load("back.png")
        self.screen.blit(background, (0, 0))
        x, y = self.info.current_w / 2, self.info.current_h / 2
        # 创建一个按钮不显示
        pos = pygame.mouse.get_pos()
        button = self.create_button("测 试 范 例")
        button_x, button_y = x - button.get_width() / 2, y - button.get_height() / 2

        # 检查鼠标是否在按钮上
        rect = button.get_rect()
        if self.check_mouse(pos, rect, button_x, button_y, -100):
            play = self.create_button("简 单 模 式", color=(182, 208, 226))
            if not self.hover_flag[2]:
                self.hover_sound.play()
            self.hover_flag[2] = 1
        else:
            self.hover_flag[2] = 0
            play = self.create_button("简 单 模 式")

        if self.check_mouse(pos, rect, button_x, button_y):
            close = self.create_button("眼 瞎 模 式", color=(182, 208, 226))
            if not self.hover_flag[3]:
                self.hover_sound.play()
            self.hover_flag[3] = 1
        else:
            self.hover_flag[3] = 0
            close = self.create_button("眼 瞎 模 式")

        if self.check_mouse(pos, rect, button_x, button_y, 100):
            back = self.create_button("返 回 菜 单", color=(182, 208, 226))
            if not self.hover_flag[4]:
                self.hover_sound.play()
            self.hover_flag[4] = 1
        else:
            self.hover_flag[4] = 0
            back = self.create_button("返 回 菜 单")

        self.screen.blit(play, (button_x, button_y - 100))
        self.screen.blit(close, (button_x, button_y))
        self.screen.blit(back, (button_x, button_y + 100))

        # 更新屏幕
        pygame.display.update()

    def game_over(self):  # 游戏结束（AIGC）
        while True:
            self.info = pygame.display.Info()
            x, y = self.info.current_w / 2, self.info.current_h / 2
            font = pygame.font.SysFont('华文行楷', 75)
            text = font.render("游戏已结束", True, (196, 180, 84))
            self.screen.blit(text, (x - text.get_width() / 2, (y - text.get_height() / 2) / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

    def game1(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // TILE_SIZE1, y // TILE_SIZE1
                    if self.board1[row][col] is not None:
                        self.selected.append((row, col))
                    if len(self.selected) == 3:
                        self.check_match1()
                    if self.check_game_over1():
                        self.game_over()
                    if self.countdown > 0:
                        self.countdown -= 1
                        if self.countdown == 0:
                            self.game_over()

            background = pygame.image.load("back.png")
            self.screen.blit(background, (0, 0))
            self.draw_countdown()
            self.draw_board1()
            pygame.display.update()

    def game2(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // TILE_SIZE2, y // TILE_SIZE2
                    if self.board2[row][col] is not None:
                        self.selected.append((row, col))
                    if len(self.selected) == 3:
                        self.check_match2()
                    if self.check_game_over2():
                        self.game_over()
                    if self.countdown > 0:
                        self.countdown -= 1
                        if self.countdown == 0:
                            self.game_over()

            background = pygame.image.load("back.png")
            self.screen.blit(background, (0, 0))
            self.draw_countdown()
            self.draw_board2()
            pygame.display.update()

    def draw_countdown(self):  # 倒计时组件（AIGC）
        font = pygame.font.Font('SmileySans-Oblique.ttf', 50)
        text = font.render(f"倒计时: {self.countdown}（点击方块开始计时）", True, (255, 0, 0))
        self.screen.blit(text, (10, 700))

    def start(self):
        while True:
            for event in pygame.event.get():  # 处理事件
                if event.type == pygame.QUIT:  # 如果用户点击关闭按钮
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果用户点击鼠标
                    if self.hover_flag[0] == 1:
                        self.state = 2
                    elif self.hover_flag[2] == 1:
                        self.state = 3
                    elif self.hover_flag[3] == 1:
                        self.state = 4
                    elif self.hover_flag[4] == 1:
                        self.state = 1
                    elif self.hover_flag[1] == 1:
                        exit()
                    self.hover_flag = [0, 0, 0, 0, 0]
            if self.state == 1:
                self.init()
            if self.state == 2:
                self.choose()
            if self.state == 3:
                self.game1()
            if self.state == 4:
                self.game2()

            pygame.display.update()


if __name__ == '__main__':
    Game = MyGame()
    Game.start()
