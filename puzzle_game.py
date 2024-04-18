import pygame
import sys
import random

class PuzzleGame:
    def __init__(self):
        pygame.init()

        # Size of the window
        self.WIDTH, self.HEIGHT = 600, 600
        self.ROWS, self.COLS = 3, 3
        self.TILE_SIZE = self.WIDTH // self.COLS

        # Colors
        self.WHITE = (255, 255, 255)

        # Initializing the window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Slide Puzzle")

        # Uploading an image for a puzzle and breaking it into pieces
        self.tiles = self._load_and_split_image("sources/images/earth/pazzle-earth.png", self.WIDTH, self.HEIGHT)
        self.tiles = self._shuffle_tiles(self.tiles)
        self.empty_index = self.tiles.index(None)

        # Uploading an image for the background
        self.background = self._load_image("sources/images/earth/pazzle-earth_dark.png", self.WIDTH, self.HEIGHT)

        self.running = True
        self.solved = False

        pygame.mixer.music.load('sources/sounds/earth/puzzle_soundtrack.mp3')

    def _load_image(self, image_path, width, height):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def _load_and_split_image(self, image_path, width, height):
        image = self._load_image(image_path, width, height)
        tile_width = image.get_width() // self.COLS
        tile_height = image.get_height() // self.ROWS
        tiles = []
        for y in range(self.ROWS):
            for x in range(self.COLS):
                rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                tile = image.subsurface(rect)
                tiles.append(tile)
        return tiles

    def _shuffle_tiles(self, tiles):
        shuffled_tiles = tiles[:-1]  # Exclude the last (empty) piece from mixing
        random.shuffle(shuffled_tiles)
        shuffled_tiles.append(None)  # Add an empty piece to the end
        return shuffled_tiles

    def _draw_tiles(self):
        for i, tile in enumerate(self.tiles):
            if tile is not None:
                row, col = i // self.COLS, i % self.COLS
                x, y = col * self.TILE_SIZE, row * self.TILE_SIZE
                self.screen.blit(tile, (x, y))

    def _handle_click(self, row, col):
        index = row * self.COLS + col
        if index - self.COLS == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif index + self.COLS == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif index % self.COLS != 0 and index - 1 == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif (index + 1) % self.COLS != 0 and index + 1 == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]

    def _display_congratulations(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Congratulations! The puzzle is complete!", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        background_rect = text_rect.inflate(20, 20)  #Enlarging the rectangle for filling
        pygame.draw.rect(self.screen, (71, 107, 4), background_rect)  #Fill the rectangle with white color
        self.screen.blit(text, text_rect)  #Drawing the text
        pygame.display.update()  #Updating the screen to display text and fill
        pygame.time.delay(2000)
        self.running = False

    def run(self):
        # count = 0
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.solved:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        col = x // self.TILE_SIZE
                        row = y // self.TILE_SIZE
                        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
                            index = row * self.COLS + col
                            if index - self.COLS == self.empty_index or index + self.COLS == self.empty_index or \
                               (index % self.COLS != 0 and index - 1 == self.empty_index) or \
                               ((index + 1) % self.COLS != 0 and index + 1 == self.empty_index):
                                pygame.mixer.Sound('sources/sounds/earth/move.mp3').play()
                                self._handle_click(row, col)
                                self.empty_index = self.tiles.index(None)
                                #count+=1
                                if all(self.tiles[i] == i for i in range(len(self.tiles))):
                                    self.solved = True
                                # if count == 1:
                                #     self.solved = True

            # Drawing the background
            self.screen.blit(self.background, (0, 0))

            # Drawing the puzzle pieces
            self._draw_tiles()

            # If the puzzle is assembled, we display congratulations
            if self.solved:
                self._display_congratulations()
                pygame.mixer.music.stop()
                
            pygame.display.flip()

if __name__ == "__main__":
    game = PuzzleGame()
    game.run()