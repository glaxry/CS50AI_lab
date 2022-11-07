import numpy as np
import pygame
import sys
import tensorflow as tf
import time

# 检查命令行参数
if len(sys.argv) != 2:
    sys.exit("Usage: python recognition.py model")
model = tf.keras.models.load_model(sys.argv[1])

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 开始 pygame
pygame.init()
size = width, height = 600, 400
# 设置主屏窗口
screen = pygame.display.set_mode(size)

# 引入字体类型
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# 手写区域
ROWS, COLS = 28, 28

OFFSET = 20
CELL_SIZE = 10

handwriting = [[0] * COLS for _ in range(ROWS)]
classification = None

while True:

    # 检查游戏是否退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # 检查鼠标是否按下
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
    else:
        mouse = None

    # 绘制每个网格单元
    cells = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            rect = pygame.Rect(
                OFFSET + j * CELL_SIZE,
                OFFSET + i * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )

            # 如果单元格已被写入，则使单元格变暗
            if handwriting[i][j]:
                channel = 255 - (handwriting[i][j] * 255)
                pygame.draw.rect(screen, (channel, channel, channel), rect)

            # 绘制空白单元格
            else:
                pygame.draw.rect(screen, WHITE, rect)
            # 绘制边界
            pygame.draw.rect(screen, BLACK, rect, 1)

            # 如果在这个单元格上写，填写当前单元格和邻居

            if mouse and rect.collidepoint(mouse):
                handwriting[i][j] = 250 / 255
                if i + 1 < ROWS:
                    handwriting[i + 1][j] = 220 / 255
                if j + 1 < COLS:
                    handwriting[i][j + 1] = 220 / 255
                if i + 1 < ROWS and j + 1 < COLS:
                    handwriting[i + 1][j + 1] = 190 / 255

    # 复位按钮
    resetButton = pygame.Rect(
        30, OFFSET + ROWS * CELL_SIZE + 30,
        100, 30
    )
    # 绘制文本内容
    resetText = smallFont.render("Reset", True, BLACK)
    # 获得显示对象的 rect区域大小
    resetTextRect = resetText.get_rect()
    #设置显示对象居中
    resetTextRect.center = resetButton.center
    # 绘制白色背景
    pygame.draw.rect(screen, WHITE, resetButton)
  
    screen.blit(resetText, resetTextRect)

    # 分类按钮
    classifyButton = pygame.Rect(
        150, OFFSET + ROWS * CELL_SIZE + 30,
        100, 30
    )
    classifyText = smallFont.render("Classify", True, BLACK)
    classifyTextRect = classifyText.get_rect()
    classifyTextRect.center = classifyButton.center
    pygame.draw.rect(screen, WHITE, classifyButton)
    screen.blit(classifyText, classifyTextRect)

    # 重置绘图
    if mouse and resetButton.collidepoint(mouse):
        handwriting = [[0] * COLS for _ in range(ROWS)]
        classification = None

    # 生成分类
    if mouse and classifyButton.collidepoint(mouse):
        classification = model.predict(
            [np.array(handwriting).reshape(1, 28, 28, 1)]
        ).argmax()

    # 如果存在则显示分类
    if classification is not None:
        classificationText = largeFont.render(str(classification), True, WHITE)
        classificationRect = classificationText.get_rect()
        grid_size = OFFSET * 2 + CELL_SIZE * COLS
        classificationRect.center = (
            grid_size + ((width - grid_size) / 2),
            100
        )
        screen.blit(classificationText, classificationRect)

    pygame.display.flip()
