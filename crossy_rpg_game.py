import pygame
SCREEN_TITLE = "Mr's RPG"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# RGB
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

font_level = pygame.font.SysFont('comicsansms', 45)


class Game:

    # Typical rate of 60, equivalent to FPS
    TICK_RATE = 60
    is_game_over = False
    # Initializer for the game class to set up the width, height, and title

    def __init__(self, image_path_bg, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # create window of specified size in white to display game
        self.game_screen = pygame.display.set_mode((width, height))
        # set game windows color to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        # Load and set the background image for the scene
        background_image = pygame.image.load(image_path_bg)
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):

        is_game_over = False
        did_win = False
        direction = 0
        player_character = PlayerCharacter(
            'player.png', 375, 700, 50, 50)

        enemy_0 = Enemy("enemy.png", 20, 600, 50, 50)
        enemy_0.SPEED *= level_speed

        enemy_1 = Enemy("enemy.png", self.width - 40, 400, 50, 50)
        enemy_1.SPEED *= level_speed

        enemy_2 = Enemy("enemy.png", 20, 200, 50, 50)
        enemy_2.SPEED *= level_speed
        treasure = GameObject("treasure.png", 375, 50, 50, 50)
        enemies = [enemy_0, enemy_1, enemy_2]
        # for enemy in enemies:
        #     enemy = Enemy("enemy.png", 20)
        # Main game loop, used to update all gameplay such as movement, checks, and graphics
        # Runs until is_game_over = True
        while not is_game_over:
            level = font_level.render(
                "Livello " + str(level_speed), 1, WHITE_COLOR)
            # A loop to get all of the events occurring at any given time
            # Events are most often mouse movement, mouse and button clicks, or exit events
            for event in pygame.event.get():
                # If we have a quit type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    is_game_over = True
                elif event.type == pygame.KEYDOWN:
                    # Move up if up key pressed
                    if event.key == pygame.K_w:
                        direction = 1
                    # Move down if down key pressed
                    elif event.key == pygame.K_s:
                        direction = -1
                # Detect when key is released
                elif event.type == pygame.KEYUP:
                    # Stop movement when key no longer pressed
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        direction = 0
                print(event)

            # Redraw the screen to be a black white window
            self.game_screen.fill(WHITE_COLOR)
            # Draw the image into the bg
            self.game_screen.blit(self.image, (0, 0))
            self.game_screen.blit(level, (0, 0))

            # self.game_screen.draw.text(
            #     str(level_speed), bottomright=(500, 400), align="left")

            # Draw treasure
            treasure.draw(self.game_screen)

            # Update the player position
            player_character.move(direction, self.height)
            # Draw the player at the new position
            player_character.draw(self.game_screen)

            # Move and draw the enemy character
            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            if level_speed > 2:
                enemy_1.move(self.width)
                enemy_1.draw(self.game_screen)
            if level_speed > 4:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_screen)

            # End game if collision between enemy and treasure
            # Close game if we lose
            # Restart game loop if we win
            for enemy in enemies:
                if player_character.detect_collision(enemy):
                    is_game_over = True
                    did_win = False
                    text = font.render("Hai perso !", True, BLACK_COLOR)
                    self.game_screen.blit(text, (275, 350))
                    pygame.display.update()
                    clock.tick(1)
            if player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render("Hai vinto !", True, BLACK_COLOR)
                self.game_screen.blit(text, (275, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # Update alla game graphics
            pygame.display.update()
            # tick the clock to update everything within the game
            clock.tick(self.TICK_RATE)

        # Restart game loop if we won
        # Break out of game loop and quit if we lose
        if did_win:
            self.run_game_loop(level_speed + 1)
        else:
            return

# Generic game object class to be subclassed by other objects in the game


class GameObject:

    def __init__(self, image_path, x, y, width, height):
        obj_image = pygame.image.load(image_path)
        # scale the image up
        self.image = pygame.transform.scale(obj_image, (width, height))
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
    # Draw the object by blitting it onto the background (game screen)

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))


# Class to represent the character controlled by the player


class PlayerCharacter(GameObject):
    # How many tiles the character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
    # Move function will move character up if direction > 0 and down if < 0

    def move(self, direction, max_height):
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED
    # Make sure the character never goes past the bottom of the screen
        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True


# Class to represent the enemies moving left to right and right to left
class Enemy(GameObject):
    # How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    # Move function will move character right once it hits the far left of the
    # screen and left once it hits the far right of the screen
    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - (20 + self.width):
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED


pygame.init()

new_game = Game("background.png", SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)


# Quite pygame and the program
pygame.quit()
quit()
