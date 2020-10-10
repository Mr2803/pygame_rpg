import pygame


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Mr's RPG"

# RGB
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
# Clock used to update game events and frames
clock = pygame.time.Clock()
# Typical rate of 60, equivalent to FPS
TICK_RATE = 60
is_game_over = False
# create window of specified size in white to display game
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set game windows color to white
game_screen.fill(WHITE_COLOR)
pygame.display.set_caption(SCREEN_TITLE)
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))

while not is_game_over:
    # A loop to get all of the events occurring at any given time
    # Events are most often mouse movement, mouse and button clicks, or exit events
    for event in pygame.event.get():
        # If we have a quit type event (exit out) then exit out of the game loop
        if event.type == pygame.QUIT:
            is_game_over = True
        print(event)

    # create a rectangle(x,y,width,height)
    # pygame.draw.rect(game_screen, BLACK_COLOR, [350, 350, 100, 100])
    # # create a circle(x,y,radius)
    # pygame.draw.circle(game_screen, BLACK_COLOR, (400, 300), 50)
    # Draw the player image on top of the screen at (x, y) position
    game_screen.blit(player_image, (375, 375))

    # Update alla game graphics
    pygame.display.update()
    # tick the clock to update everything within the game
    clock.tick(TICK_RATE)

# Quite pygame and the program
pygame.quit()
quit()
