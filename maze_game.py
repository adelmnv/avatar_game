import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (30,144,255)
BLUE1 = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BROWN= (139,69,19)

# Размеры экрана
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Размеры ячейки лабиринта
CELL_SIZE = 15

# Количество ячеек в ширину и высоту
GRID_WIDTH = (SCREEN_WIDTH // CELL_SIZE) 
GRID_HEIGHT = (SCREEN_HEIGHT // CELL_SIZE) 

# Скорость игрока
PLAYER_SPEED = 1

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лабиринт")

# Фоновое изображение
background = pygame.image.load("sources/images/water/maze_background.jpeg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка фоновой музыки
pygame.mixer.music.load("sources/sounds/water/maze_music.mp3")
pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

# Генерация лабиринта
def generate_maze():
    maze = [[1] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    # Установка начальной точки
    maze[1][1] = 0

    # Создание лабиринта
    stack = [(1, 1)]
    while stack:
        current_cell = stack[-1]
        maze[current_cell[1]][current_cell[0]] = 0

        neighbors = [(current_cell[0] + 2, current_cell[1]),
                     (current_cell[0] - 2, current_cell[1]),
                     (current_cell[0], current_cell[1] + 2),
                     (current_cell[0], current_cell[1] - 2)]
        unvisited_neighbors = [neighbor for neighbor in neighbors if 0 < neighbor[0] < GRID_WIDTH - 1 and 0 < neighbor[1] < GRID_HEIGHT - 1 and maze[neighbor[1]][neighbor[0]] == 1]

        if unvisited_neighbors:
            next_cell = random.choice(unvisited_neighbors)
            wall = ((current_cell[0] + next_cell[0]) // 2, (current_cell[1] + next_cell[1]) // 2)
            maze[wall[1]][wall[0]] = 0
            stack.append(next_cell)
        else:
            stack.pop()

    return maze

# Отображение лабиринта
def draw_maze(maze):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                pygame.draw.circle(screen, BROWN, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Отображение стартовой и конечной точек
def draw_start_end():
    pygame.draw.circle(screen, GREEN, (CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
    pygame.draw.circle(screen, RED, ((GRID_WIDTH - 3) * CELL_SIZE + CELL_SIZE // 2, (GRID_HEIGHT - 3) * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Главный игровой цикл
maze = generate_maze()
player_x = 1
player_y = 1
keys = {'up': False, 'down': False, 'left': False, 'right': False}  # Переменные для хранения состояния клавиш
player_path = []  # Изначально путь игрока пуст
game_over = False

clock = pygame.time.Clock()  # Создаем объект Clock для управления кадрами

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys['up'] = True
            elif event.key == pygame.K_DOWN:
                keys['down'] = True
            elif event.key == pygame.K_LEFT:
                keys['left'] = True
            elif event.key == pygame.K_RIGHT:
                keys['right'] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys['up'] = False
            elif event.key == pygame.K_DOWN:
                keys['down'] = False
            elif event.key == pygame.K_LEFT:
                keys['left'] = False
            elif event.key == pygame.K_RIGHT:
                keys['right'] = False

    if keys['up'] and player_y - PLAYER_SPEED > 0 and maze[player_y - PLAYER_SPEED][player_x] == 0:
        player_y -= PLAYER_SPEED
        player_path.append((player_x, player_y))  # Добавляем текущую позицию в путь
    if keys['down'] and player_y + PLAYER_SPEED < GRID_HEIGHT and maze[player_y + PLAYER_SPEED][player_x] == 0:
        player_y += PLAYER_SPEED
        player_path.append((player_x, player_y))
    if keys['left'] and player_x - PLAYER_SPEED > 0 and maze[player_y][player_x - PLAYER_SPEED] == 0:
        player_x -= PLAYER_SPEED
        player_path.append((player_x, player_y))
    if keys['right'] and player_x + PLAYER_SPEED < GRID_WIDTH and maze[player_y][player_x + PLAYER_SPEED] == 0:
        player_x += PLAYER_SPEED
        player_path.append((player_x, player_y))

    # Проверка, попал ли игрок на свои следы
    if (player_x, player_y) in player_path[:-1]:
        game_over = True
    # Проверка, достиг ли игрок конечной точки
    if (player_x, player_y) == ((GRID_WIDTH - 3), (GRID_HEIGHT - 3)):
        game_over = True

    # Отображение фона
    screen.blit(background, (0, 0))

    # Отображение лабиринта
    draw_maze(maze)

    # Отображение стартовой и конечной точек
    draw_start_end()

    # Отображение следов игрока
    for px, py in player_path:
        pygame.draw.rect(screen, BLUE, (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
    # Отображение игрока
    pygame.draw.circle(screen, BLUE, (player_x * CELL_SIZE + CELL_SIZE // 2, player_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

    pygame.display.flip()
    
    clock.tick(60)  # Устанавливаем частоту кадров

# Вывод "Game Over" на экран
screen.fill(BLACK)  # Заливаем экран черным цветом
font = pygame.font.SysFont(None, 48)
game_over_text = font.render("Game Over", True, RED)
text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
screen.blit(game_over_text, text_rect)
pygame.display.flip()

# Ждем некоторое время перед завершением
pygame.time.delay(1000)
