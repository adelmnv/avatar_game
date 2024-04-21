import pygame
import random
import sys

class WaterGame:
    """
    A class representing the 'Water - Flow Control' game.
    """
    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (30, 144, 255)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255, 165, 0)
        self.BROWN = (139, 69, 19)

        # Screen dimensions
        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 600

        # Maze cell dimensions
        self.CELL_SIZE = 15

        # Number of cells in width and height
        self.GRID_WIDTH = self.SCREEN_WIDTH // self.CELL_SIZE
        self.GRID_HEIGHT = self.SCREEN_HEIGHT // self.CELL_SIZE

        # Player speed
        self.PLAYER_SPEED = 1

        # Create window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Water - Flow Control")

        # Background image
        self.background = pygame.image.load("sources/images/water/maze_background.jpeg")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load background music
        pygame.mixer.music.load("sources/sounds/water/maze_music.mp3")
        pygame.mixer.music.play(-1)

        # Flag to track if the intro has been shown
        self.intro_shown = False

        # Clock object to control frame rate
        self.clock = pygame.time.Clock()
        
        # Flag to track if mouse has been clicked
        self.clicked = False

    def generate_maze(self):
        """
        Generate a maze using a modified version of the recursive backtracking algorithm.

        Returns:
            list: A 2D list representing the generated maze.
        """
        # Create a grid filled with walls
        maze = [[1] * self.GRID_WIDTH for _ in range(self.GRID_HEIGHT)]

        # Set starting point of the maze
        maze[1][1] = 0

        # Create a stack to keep track of visited cells
        stack = [(1, 1)]

        # Generate the maze
        while stack:
            # Get the current cell from the top of the stack
            current_cell = stack[-1]

            # Mark the current cell as visited
            maze[current_cell[1]][current_cell[0]] = 0

            # Get the neighbors of the current cell
            neighbors = [(current_cell[0] + 2, current_cell[1]),
                         (current_cell[0] - 2, current_cell[1]),
                         (current_cell[0], current_cell[1] + 2),
                         (current_cell[0], current_cell[1] - 2)]
            
            # Filter the unvisited neighbors
            unvisited_neighbors = [neighbor for neighbor in neighbors if
                                   0 < neighbor[0] < self.GRID_WIDTH - 1 and 0 < neighbor[1] < self.GRID_HEIGHT - 1 and
                                   maze[neighbor[1]][neighbor[0]] == 1]

            # If there are unvisited neighbors
            if unvisited_neighbors:
                # Choose a random unvisited neighbor
                next_cell = random.choice(unvisited_neighbors)

                # Calculate the wall between the current cell and the next cell
                wall = ((current_cell[0] + next_cell[0]) // 2, (current_cell[1] + next_cell[1]) // 2)

                # Remove the wall between the current cell and the next cell
                maze[wall[1]][wall[0]] = 0

                # Push the next cell onto the stack
                stack.append(next_cell)
            else:
                # If there are no unvisited neighbors, pop the current cell from the stack
                stack.pop()

        return maze

    def draw_maze(self, maze):
        """
        Draw the maze on the screen.

        Args:
            maze (list): A 2D list representing the maze.
        """
        # Iterate over each cell in the maze
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                # If the cell is a wall (marked as 1), draw a circle to represent it
                if maze[y][x] == 1:
                    pygame.draw.circle(self.screen, self.BROWN, (x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

    def draw_start_end(self):
        """
        Draw the start and end points on the maze.
        """
        # Draw the start point (green circle)
        pygame.draw.circle(self.screen, self.GREEN, (self.CELL_SIZE + self.CELL_SIZE // 2, self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)
        # Draw the end point (red circle)
        pygame.draw.circle(self.screen, self.RED, ((self.GRID_WIDTH - 3) * self.CELL_SIZE + self.CELL_SIZE // 2, (self.GRID_HEIGHT - 3) * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

    def show_intro(self):
        """
        Display the game introduction.
        """
        # Display the intro only if it has not been displayed yet
        if not self.intro_shown:
            # Load and scale the intro image
            intro_image = pygame.transform.scale(pygame.image.load("sources/images/water/water_intro.jpg"), (600, 600))
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
        # Generate the maze
        maze = self.generate_maze()

        # Initialize player position, tracking pressed keys, tracking player's path, flag to indicate game over, flag to indicate win
        player_x = 1
        player_y = 1
        keys = {'up': False, 'down': False, 'left': False, 'right': False}
        player_path = []
        game_over = False
        win = False

        # Show intro
        self.show_intro()

        # Main game loop
        while not game_over:
            # Event handling
            for event in pygame.event.get():
                # If the user closes the window
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    game_over = True
                    return win
                # If a key is pressed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.clicked == False:
                        keys['up'] = True
                        self.clicked = True
                    elif event.key == pygame.K_DOWN and self.clicked == False:
                        keys['down'] = True
                        self.clicked = True
                    elif event.key == pygame.K_LEFT and self.clicked == False:
                        keys['left'] = True
                        self.clicked = True
                    elif event.key == pygame.K_RIGHT and self.clicked == False:
                        keys['right'] = True
                        self.clicked = True
                # If a key is released
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        keys['up'] = False
                    elif event.key == pygame.K_DOWN:
                        keys['down'] = False
                    elif event.key == pygame.K_LEFT:
                        keys['left'] = False
                    elif event.key == pygame.K_RIGHT:
                        keys['right'] = False
            # Delay to control game speed
            pygame.time.delay(50)
            self.clicked = False

            # Move the player based on pressed keys
            if keys['up'] and player_y - self.PLAYER_SPEED > 0 and maze[player_y - self.PLAYER_SPEED][player_x] == 0:
                player_y -= self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['down'] and player_y + self.PLAYER_SPEED < self.GRID_HEIGHT and maze[player_y + self.PLAYER_SPEED][player_x] == 0:
                player_y += self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['left'] and player_x - self.PLAYER_SPEED > 0 and maze[player_y][player_x - self.PLAYER_SPEED] == 0:
                player_x -= self.PLAYER_SPEED
                player_path.append((player_x, player_y))
            if keys['right'] and player_x + self.PLAYER_SPEED < self.GRID_WIDTH and maze[player_y][player_x + self.PLAYER_SPEED] == 0:
                player_x += self.PLAYER_SPEED
                player_path.append((player_x, player_y))

            # Check for game over conditions
            # If the player hits itself
            if (player_x, player_y) in player_path[:-1]:
                game_over = True
            # If the player reaches the end
            if (player_x, player_y) == ((self.GRID_WIDTH - 3), (self.GRID_HEIGHT - 3)):
                game_over = True
                win = True

            self.screen.blit(self.background, (0, 0))
            self.draw_maze(maze)
            self.draw_start_end()

            # Draw player's path and current position
            for px, py in player_path:
                pygame.draw.rect(self.screen, self.BLUE, (px * self.CELL_SIZE, py * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
            pygame.draw.circle(self.screen, self.BLUE, (player_x * self.CELL_SIZE + self.CELL_SIZE // 2, player_y * self.CELL_SIZE + self.CELL_SIZE // 2), self.CELL_SIZE // 2)

            pygame.display.flip()
            # Cap the frame rate
            self.clock.tick(60)

        # Display game over message
        self.screen.fill(self.BLACK)
        font = pygame.font.SysFont('Papyrus', 32)
        # If player won
        if win:
            game_over_text = font.render("You've managed to master water!", True, self.GREEN)
        # If player lost
        else:
            game_over_text = font.render("Flow can't be reversed...", True, self.RED)
        text_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        pygame.time.delay(2000)

        # Return win status
        return win

# Check if the script is being run as the main program
if __name__ == "__main__":
    game = WaterGame()
    game.run()
