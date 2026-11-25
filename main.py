import sys
import pygame
import random


# INITIALIZATION
pygame.init()

# Create the width/height of the screen
width = 800
height = 600
size = (width, height)

# Define black for painting the screen
black = (0, 0, 0)

# Set the size of your screen and display caption
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chicken Click")

# Load the chicken image
chicken = pygame.image.load("chicken.png")
snowflake = pygame.image.load("Snowflake.png")

# Set up variables for chickens
iterator = 0
numOfChickens = 5
startX = []
startY = []
speed = []
isFrozen = False
snowActive = False
snowSpawn = 600
waitTimer = 0
freezeDuration = 600
freezeTimer = 0
snowX = random.randint(0, width - snowflake.get_width())
snowY = random.randint(0, height - snowflake.get_height())

while iterator < numOfChickens:
    startX.append(random.randint(0, width - chicken.get_width() + 1))
    startY.append(random.randint(-chicken.get_height() * 2, -chicken.get_height()))
    speed.append(random.random() + float(random.randint(0, 3)) + 0.1)
    iterator += 1



# Game states and Fonts
replayScreen = False

bigFont = pygame.font.SysFont(None, 200)
playAgainText = bigFont.render("Play Again?", True, (0, 200, 0))
pax = width / 2 - playAgainText.get_rect().width / 2

smallFont = pygame.font.SysFont(None, 100)
yesText = smallFont.render("YES", True, (0, 200, 0))
yesX = width / 4 - yesText.get_rect().width / 2

noText = smallFont.render("NO", True, (0, 200, 0))
nox = width - width / 4 - yesText.get_rect().width / 2

# GAME LOOP
gameOver = False


while not gameOver:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    # CHECKING CLICKS
    if pygame.mouse.get_pressed()[0]:
        coords = pygame.mouse.get_pos()
        if not replayScreen:
            iterator = 0
            while iterator < numOfChickens:
                if (
                    coords[0] >= startX[iterator]
                    and coords[0] <= startX[iterator] + chicken.get_width()
                    and coords[1] >= startY[iterator]
                    and coords[1] <= startY[iterator] + chicken.get_height()
                ):
                    startX[iterator] = random.randint(
                        0, width - chicken.get_width() + 1
                    )
                    startY[iterator] = random.randint(
                        -chicken.get_height() * 2, -chicken.get_height()
                    )
                    speed[iterator] = random.random() + float(random.randint(0, 3)) + 1.1
                    break
                iterator += 1

            if (
                snowActive
                and coords[0] >= snowX
                and coords[0] <= snowX + snowflake.get_width()
                and coords[1] >= snowY
                and coords[1] <= snowY + snowflake.get_height()
            ):
                isFrozen = True
                snowActive = False
                freezeTimer = 0
        else:
            # Check YES button
            if (
                coords[0] > yesX
                and coords[0] < yesX + yesText.get_rect().width
                and coords[1] > 450
                and coords[1] < 450 + yesText.get_rect().height
            ):
                iterator = 0
                while iterator < numOfChickens:
                    startX[iterator] = random.randint(
                        0, width - chicken.get_width() + 1
                    )
                    startY[iterator] = random.randint(
                        -chicken.get_height() * 2, -chicken.get_height()
                    )
                    speed[iterator] = random.random() + float(random.randint(0, 3)) + 0.1
                    iterator += 1
                replayScreen = False
                isFrozen = False
                snowActive = False
                waitTimer = 0
                freezeTimer = 0
                replayScreen = False

            # Check NO button
            if (
                coords[0] > nox
                and coords[0] < nox + noText.get_rect().width
                and coords[1] > 450
                and coords[1] < 450 + noText.get_rect().height
            ):
                gameOver = True

    # UPDATING STUFF
    if isFrozen:
      freezeTimer += 1
      if freezeTimer >= freezeDuration:
        isFrozen = False
        freezeTimer = 0

    if not snowActive and not isFrozen:
            waitTimer += 1
            if waitTimer > snowSpawn:
                snowX = random.randint(0, width - snowflake.get_width())
                snowY = random.randint(0, height - snowflake.get_height())
                snowActive = True
                waitTimer = 0

    if not replayScreen:
        if not isFrozen:
            iterator = 0
            while iterator < numOfChickens:
                if startY[iterator] + chicken.get_height() > height:
                    replayScreen = True
                    break
                startY[iterator] += speed[iterator]
                iterator += 1

    # DRAWING STUFF
    if not replayScreen:
        screen.fill(black)
        iterator = 0
        while iterator < numOfChickens:
            screen.blit(chicken, (startX[iterator], startY[iterator]))
            iterator += 1

        if snowActive:
            screen.blit(snowflake, (snowX, snowY))

    else:
        screen.fill((200, 0, 0))
        screen.blit(playAgainText, (pax, 150))
        screen.blit(yesText, (yesX, 450))
        screen.blit(noText, (nox, 450))

    # Flip the screen to update display for the new frame
    pygame.display.flip()

# Quit Pygame when loop ends
pygame.display.quit()
sys.exit()