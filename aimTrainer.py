import pygame, random, sys, os
from pygame.locals import *

pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

WINDOWHEIGHT = 750
WINDOWWIDTH = 750

FONT = pygame.font.SysFont(None, 48)

def terminate():
    pygame.quit()
    sys.exit()

def Menu():
    timer = 0
    color = BLUE
    switch = False
    while True:
        windowSurface.fill(BLACK)
        difficultyRects = []
        difficultyRects.append(pygame.Rect(5, 450, 240, 100))
        difficultyRects.append(pygame.Rect(255, 450, 240, 100))
        difficultyRects.append(pygame.Rect(505, 450, 240, 100))
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == MOUSEBUTTONDOWN:
                if difficultyRects[0].collidepoint(pygame.mouse.get_pos()):
                    game("easy")
                if difficultyRects[1].collidepoint(pygame.mouse.get_pos()):
                    game("medium")
                if difficultyRects[2].collidepoint(pygame.mouse.get_pos()):
                    game("hard")
        for rect in difficultyRects:
            pygame.draw.rect(windowSurface, RED, rect)
        drawText("Pick a difficulty", windowSurface, 90, 150, pygame.font.SysFont(None, 112), color)
        drawText("Easy", windowSurface, 83, 485, FONT , BLACK)
        drawText("Medium", windowSurface, 312, 485,FONT , BLACK)
        drawText("Hard", windowSurface, 580, 485,FONT , BLACK)
        mainClock.tick(50)
        timer += 1
        if timer % 100 == 0:
            color = BLUE
        elif timer % 50 == 0:
            color = RED
        pygame.display.update()

def drawText(text, surface, x, y, font = FONT, color = RED):
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObject, textRect)

def gameOver(totalShots, hitShots, difficulty, score):
    pygame.mouse.set_visible(True)
    if totalShots != 0 and hitShots != 0:
        accuracy = round(hitShots/totalShots * 100)
    else:
        accuracy = 0
    windowSurface.fill(BLACK)
    drawText("GAME OVER", windowSurface, 200, 325, pygame.font.SysFont(None, 72, True))
    drawText("Click anywhere to restart", windowSurface, 170, 380)
    drawText("Accuracy: " + str(accuracy) + "%", windowSurface, 269, 414)
    drawText("Score: " + str(score), windowSurface, 308, 450)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONDOWN:
                windowSurface.fill(WHITE)
                Menu()
            if event.type == KEYDOWN:
                terminate()

def populateConfig(difficulty):
    global targetImage
    targetImage = pygame.image.load("target.png")
    config = {}
    if(difficulty == "easy"):
        difficultyFile = open("easy.txt", "r")
    elif(difficulty == "medium"):
        difficultyFile = open("medium.txt", "r")
    elif(difficulty == "hard"):
        difficultyFile = open("hard.txt", "r")
    for line in difficultyFile:
        splitLine = line.split(":")
        splitLine[1] = splitLine[1].strip("\n")
        config[splitLine[0]] = int(splitLine[1])
    targetImage = pygame.transform.scale(targetImage, (config["enemySize"],config["enemySize"]))
    difficultyFile.close()
    return config

mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption("sniper")

shootSound = pygame.mixer.Sound("snipersound.wav")
hitSound = pygame.mixer.Sound("metalHit.wav")
shootSound.set_volume(0.25)
hitSound.set_volume(1)


enemies = []

def game(difficulty):
    config = populateConfig(difficulty)
    
    pygame.mouse.set_visible(False)
    
    mouseY = (round(WINDOWHEIGHT / 2))
    mouseX = (round(WINDOWWIDTH / 2))
    
    tickCounter = 0
    enemies = []
    amountOfEnemies = 0
    score = 0
    FPS = 75
    hitShots = 0
    totalShots = 0
    STARTINGTIME = config.get("time")
    CIRCLERADIUS = 150
    while True:
        if(config.get("time") <= 0):
            gameOver(totalShots, hitShots, difficulty, score)
        tickCounter += 1
        if(tickCounter % FPS == 0):
            config["time"] -= 1
        windowSurface.fill(WHITE)

        if (amountOfEnemies == 0):
            config["time"] = STARTINGTIME
            while(amountOfEnemies != config.get("maxAmountOfEnemies")):
                enemies.append(pygame.Rect((random.randint(0,WINDOWWIDTH - config.get("enemySize"))),
                                           (random.randint(0,WINDOWHEIGHT - config.get("enemySize"))),
                                           config.get("enemySize"), config.get("enemySize")))
                if enemies[amountOfEnemies].topleft[0] < 135 and enemies[amountOfEnemies].topleft[1] < 65:
                    enemies.pop(amountOfEnemies)
                else:
                    amountOfEnemies += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                pass
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == MOUSEMOTION:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
            if event.type == MOUSEBUTTONDOWN:
                pygame.mixer.Channel(0).play(shootSound)
                totalShots += 1
                for enemy in enemies[:]:
                    if mouseX > enemy.topleft[0] and mouseX < enemy.bottomright[0]\
                       and mouseY > enemy.topleft[1] and mouseY < enemy.bottomright[1]:
                        pygame.mixer.Channel(1).play(hitSound)
                        enemies.remove(enemy)
                        amountOfEnemies -= 1
                        score += 1
                        hitShots += 1
                
                        
                                           
        pygame.draw.circle(windowSurface, WHITE, (mouseX,mouseY),
                           CIRCLERADIUS,0)
        for enemy in enemies:
            windowSurface.blit(targetImage, enemy)
        pygame.draw.circle(windowSurface, BLACK, (mouseX,mouseY),
                           CIRCLERADIUS + 1, 3)
        pygame.draw.line(windowSurface, BLACK, (mouseX, mouseY + 150),
                        (mouseX, mouseY - 150), 2)
        pygame.draw.line(windowSurface, BLACK, (mouseX + 150, mouseY),
                        (mouseX - 150, mouseY), 2)
        drawText("Time: " + str(config.get("time")), windowSurface, 8,8)
        drawText("Score: " + str(score), windowSurface, 8,38)
        pygame.display.update()
        mainClock.tick(FPS)
Menu()
