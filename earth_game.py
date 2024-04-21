import pygame
import sys
import random

class EarthGame:
    """
    A class representing the 'Earth - Stone Mosaic' puzzle game.
    """
    def __init__(self):
        """
        Initialize the puzzle game.
        """
        pygame.init()

        # Size of the window
        self.WIDTH, self.HEIGHT = 600, 600
        self.ROWS, self.COLS = 3, 3
        self.TILE_SIZE = self.WIDTH // self.COLS

        # Initializing the window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Earth - Stone Mosaic")

        # Uploading an image for a puzzle and breaking it into pieces (original sequence, current sequence)
        self.original_tiles = self.tiles = self._load_and_split_image("sources/images/earth/pazzle-earth.png", self.WIDTH, self.HEIGHT)
        
        # Updating original_tiles (last element shoulb be empty)
        self.original_tiles = self.original_tiles[:-1]
        self.original_tiles.append(None)
        
        # Create a list with the correct order of tiles with None since the last tile should be empty
        self.correct_order = list(range(self.ROWS * self.COLS-1))
        self.correct_order.append(None)

        # Initialize an empty list to store the current order of tiles
        self.current_order = []

        # Shuffle the tiles
        self.tiles = self._shuffle_tiles(self.tiles)

        # Determine the index of the empty space
        self.empty_index = self.tiles.index(None)

        # Uploading an image for the background
        self.background = self._load_image("sources/images/earth/pazzle-earth_dark.png", self.WIDTH, self.HEIGHT)

        # flags
        # flag for game loop
        self.running = True 
        # flag if puzzle solved
        self.solved = False
        # flag if intro shown
        self.intro_shown = False

        # load game soundtrack
        pygame.mixer.music.load('sources/sounds/earth/puzzle_soundtrack.mp3')

    def _load_image(self, image_path, width, height):
        """
        Load an image and scale it to the specified width and height.

        Args:
            image_path (str): The path to the image file.
            width (int): The width to which the image should be scaled.
            height (int): The height to which the image should be scaled.

        Returns:
            pygame.Surface: The loaded and scaled image.
        """
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (width, height))
        return image

    def _load_and_split_image(self, image_path, width, height):
        """
        Load an image, split it into tiles, and return them as a list.

        Args:
            image_path (str): The path to the image file.
            width (int): The width of the image.
            height (int): The height of the image.

        Returns:
            list: A list of pygame.Surfaces, each representing a puzzle tile.
        """
        image = self._load_image(image_path, width, height)
        # Calculate the width and height of each tile
        tile_width = image.get_width() // self.COLS
        tile_height = image.get_height() // self.ROWS

        tiles = []
        # Iterate over rows and columns to split the image into tiles
        for y in range(self.ROWS):
            for x in range(self.COLS):
                # Create a rectangle representing the current tile
                rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                # Extract the tile from the image
                tile = image.subsurface(rect)
                tiles.append(tile)
        return tiles

    def _shuffle_tiles(self, tiles):
        """
        Shuffle the puzzle tiles randomly.

        Args:
            tiles (list): A list of puzzle tiles.

        Returns:
            list: The shuffled list of puzzle tiles.
        """
        # Exclude the last (empty) piece from mixing
        original_tiles = tiles[:-1]
        shuffled_tiles = tiles[:-1]

        # Shuffle the non-empty tiles randomly
        random.shuffle(shuffled_tiles)

        # Calculate the number of inversions in the shuffled tiles
        inversions = 0
        for i in range(len(shuffled_tiles)):
            for j in range(i + 1, len(shuffled_tiles)):
                if shuffled_tiles[i] is not None and shuffled_tiles[j] is not None and original_tiles.index(shuffled_tiles[i]) > original_tiles.index(shuffled_tiles[j]):
                    inversions += 1

        # If the number of inversions is odd, swap two random tiles to make it even
        if inversions % 2 != 0:
            while True:
                # Randomly select two distinct indices
                index1, index2 = random.sample(range(len(shuffled_tiles)), 2)
                # Swap the tiles
                shuffled_tiles[index1], shuffled_tiles[index2] = shuffled_tiles[index2], shuffled_tiles[index1]
                # Recalculate the number of inversions
                inversions = sum(1 for i in range(len(shuffled_tiles)) for j in range(i + 1, len(shuffled_tiles)) if shuffled_tiles[i] is not None and shuffled_tiles[j] is not None and original_tiles.index(shuffled_tiles[i]) > original_tiles.index(shuffled_tiles[j]))
                # If the number of inversions becomes even, break the loop
                if inversions % 2 == 0:
                    break

        # Add an empty piece to the end
        original_tiles.append(None)
        shuffled_tiles.append(None) 

        # Update the current order after the tile swap
        self.current_order = [original_tiles.index(tile) if tile is not None else None for tile in shuffled_tiles]

        return shuffled_tiles



    def _draw_tiles(self):
        """
        Draw the puzzle tiles on the screen.
        """
        for i, tile in enumerate(self.tiles):
            if tile is not None:
                # Calculating the row and column index for the current tile
                row, col = i // self.COLS, i % self.COLS
                # Calculating the (x, y) coordinates to display the current tile
                x, y = col * self.TILE_SIZE, row * self.TILE_SIZE
                # Displaying the current tile on the screen
                self.screen.blit(tile, (x, y))


    def _handle_click(self, row, col):
        """
        Handle a click on a puzzle tile.

        Args:
            row (int): The row index of the clicked tile.
            col (int): The column index of the clicked tile.
        """
        # Calculate the index of the clicked tile
        index = row * self.COLS + col

        # Check if the clicked tile is adjacent to the empty tile and swap if yes
        if index - self.COLS == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif index + self.COLS == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif index % self.COLS != 0 and index - 1 == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        elif (index + 1) % self.COLS != 0 and index + 1 == self.empty_index:
            self.tiles[index], self.tiles[self.empty_index] = self.tiles[self.empty_index], self.tiles[index]
        
        # Update the current order after the tile swap
        self.current_order = [self.original_tiles.index(tile) if tile is not None else None for tile in self.tiles]
        
        # Print the current order for debugging purposes
        # print(self.current_order)

    def _display_congratulations(self):
        """
        Display a message congratulating the player for solving the puzzle.
        """
        # Selecting the font and size for the message
        font = pygame.font.SysFont('Papyrus', 36)

        # Creating the message text and text surface
        text = font.render("You've managed to master earth!", True, (0, 0, 0))

        # Getting the rectangle that surrounds the text to center it on the screen
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))

        # Enlarging the rectangle to add padding for the background color
        background_rect = text_rect.inflate(20, 20)

        #Fill the rectangle with color 
        pygame.draw.rect(self.screen, (71, 107, 4), background_rect)  

        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        
        # Setting the 'running' flag to False to end the game loop
        self.running = False

    def show_intro(self):
        """
        Display the game introduction.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            # Load and scale the intro image
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/earth/earth_intro.jpg"), (600, 600))
            # Display the intro image on the screen
            self.screen.blit(intro_image, (0, 0))
            pygame.display.update()
            # Wait for the user to press the Enter key to continue
            intro_done = False
            while not intro_done:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        intro_done = True
                pygame.time.Clock().tick(30)

            # Mark the intro as shown
            self.intro_shown = True

    def run(self):
        """
        Run the main game loop.

        Returns:
            bool: True if the player wins, False otherwise.
        """

        # Start playing the background music
        pygame.mixer.music.play(-1)
        # Show the game introduction
        self.show_intro()
        # Main game loop
        while self.running:
            # Event handling loop
            for event in pygame.event.get():
                # Quit event handling
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.running = False
                    return self.solved
                # Mouse click event handling
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.solved:
                    if pygame.mouse.get_pressed()[0]:
                        # Get the row and column indices of the clicked tile
                        x, y = pygame.mouse.get_pos()
                        col = x // self.TILE_SIZE
                        row = y // self.TILE_SIZE
                        # Handle the click if it's within the puzzle grid
                        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
                            index = row * self.COLS + col

                            # Check if the clicked tile is adjacent to the empty tile
                            if index - self.COLS == self.empty_index or index + self.COLS == self.empty_index or \
                               (index % self.COLS != 0 and index - 1 == self.empty_index) or \
                               ((index + 1) % self.COLS != 0 and index + 1 == self.empty_index):
                                # Play the move sound effect
                                pygame.mixer.Sound('sources/sounds/earth/move.mp3').play()

                                # Handle the click (move the tile)
                                self._handle_click(row, col)
                                self.empty_index = self.tiles.index(None)

                # Check if the puzzle is solved
                if self.current_order == self.correct_order:
                    self.solved = True

            # Drawing the background
            self.screen.blit(self.background, (0, 0))

            # Drawing the puzzle pieces
            self._draw_tiles()

            # If the puzzle is solved, we display congratulations
            if self.solved:
                self._display_congratulations()
                pygame.mixer.music.stop()
                return self.solved
            mouse_pos = pygame.mouse.get_pos()
            img_of_cursor = pygame.transform.scale(pygame.image.load("sources/images/main_menu/mouse_cursor.png").convert_alpha(),(30,40))
            self.screen.blit(img_of_cursor, mouse_pos)    
            pygame.display.flip()

# Check if the script is being run as the main program
if __name__ == "__main__":
    game = EarthGame()
    game.run()