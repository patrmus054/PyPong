# -----importowanie bibliotek-----
import pygame
import time
from pygame import mixer
from os.path import exists

# ---Zmienne globalne---

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-W", "--width", dest="width", type=int, metavar="WIDTH", help="Set window width", default=800)
parser.add_argument("-H", "--height", dest="height", type=int, metavar="HEIGHT", help="Set window height", default=400)
parser.add_argument("-fps", "--framerate", dest="framerate", type=int, metavar="FRAMERATE",
                    help="Set desired framerate", default=60)
parser.add_argument("-fc", "--flipcolors", dest="sc", action="store_true", help="Flip black and white for another look of the game")
parser.set_defaults(fc=False)

args = parser.parse_args()

screenWidth = args.width
screenHeight = args.height
FPS = args.framerate
flipcolors = args.fc

goals = [0, 0]

# zmiana kolorów 
if(flipcolors):
    ownBlack = (255, 255, 255)
    ownWhite = (0, 0, 0)
else:
    ownBlack = (0, 0, 0)
    ownWhite = (255, 255, 255)

ownRed = (255, 0, 0)


# -----Initializing the game-------
def init():
    pygame.init()  # inicializacja modułu pygame module
    logo = pygame.image.load("resources/logo32x32.png")  # Ładowanie Logo
    pygame.display.set_icon(logo)  # Ustaianie logo
    pygame.display.set_caption("Pong")  # Ustawienie tytułu okna
    screen = pygame.display.set_mode(
        (screenWidth, screenHeight))  # Ustawienie wielkości okna
    screen.fill(ownBlack)
    settings(screen)


# -----Ustawienia-----
def settings(screen):
    font = pygame.font.SysFont("arialroundedmtbold", 24)
    settingsText = font.render("Settings", True, ownWhite)
    screen.blit(settingsText, (screenWidth // 2 - settingsText.get_width() // 2, 10))
    pygame.display.flip()

    done = False
    startgame = False

    settingsList = [
        "Initial speed of the ball",
        "Number of players",
        "Moving speed of the players",
        "Ball size",
        "Paddle Length",
        "DONE"
    ]
    settingsIterator = 0
    settingsLength = len(settingsList)

    playerSpeed = 10  # Prędkość zawodnika pixel/sekunde
    ballSpeed = 4  # Prędkośc piłki
    ballSize = 1
    playerNumber = 1
    paddleLength = 1
    lengthText = ["Short    ", "Normal", "Long     "] # Dodatkowe miejsce zostwawiamy by by wyczyścić pole tekstowe po zminie tekstu


    renderAndUpdate(screen, str(ballSpeed), ownWhite, ownBlack,
                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(playerNumber), ownWhite, ownBlack,
                    (screenWidth // 2, 40 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(playerSpeed), ownWhite, ownBlack,
                    (screenWidth // 2, 60 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(ballSize), ownWhite, ownBlack,
                    (screenWidth // 2, 80 + 20 * settingsIterator + settingsText.get_height()))
    time.sleep(0.1)
    renderAndUpdate(screen, str(lengthText[paddleLength]), ownWhite, ownBlack,
                    (screenWidth // 2, 100 + 20 * settingsIterator + settingsText.get_height()))

    while not done:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jak jest event type quite to koniec gry
                done = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                settingsIterator += 1
                if settingsIterator == settingsLength:
                    settingsIterator = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                settingsIterator -= 1
                if settingsIterator == -1:
                    settingsIterator = settingsLength - 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                # określanie, które ustawienie jest wybrane i zwiększanie (lub zmniejszanie) wartości tego ustawienia
                if settingsIterator == 0:
                    ballSpeed += 1
                    renderAndUpdate(screen, str(ballSpeed), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 1:
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    renderAndUpdate(screen, str(playerNumber), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 2:
                    playerSpeed += 1
                    renderAndUpdate(screen, str(playerSpeed), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 3:
                    if (ballSize < 10):
                        ballSize += 1
                    renderAndUpdate(screen, str(ballSize), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 4:
                    paddleLength += 1
                    if (paddleLength > 2):
                        paddleLength = 0
                    renderAndUpdate(screen, str(lengthText[paddleLength]), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if settingsIterator == 0:
                    ballSpeed -= 1
                    if ballSpeed == 0:
                        ballSpeed = 1
                    renderAndUpdate(screen, str(ballSpeed), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 1:
                    if playerNumber == 1:
                        playerNumber = 2
                    else:
                        playerNumber = 1
                    renderAndUpdate(screen, str(playerNumber), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 2:
                    playerSpeed -= 1
                    if playerSpeed == 0:
                        playerSpeed = 1
                    renderAndUpdate(screen, str(playerSpeed), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 3:
                    if (ballSize > 1):
                        ballSize -= 1
                    renderAndUpdate(screen, str(ballSize), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))
                elif settingsIterator == 4:
                    paddleLength -= 1
                    if (paddleLength < 0):
                        paddleLength = 2
                    renderAndUpdate(screen, str(lengthText[paddleLength]), ownWhite, ownBlack,
                                    (screenWidth // 2, 20 + 20 * settingsIterator + settingsText.get_height()))

            # jeżeli wybrano opcję "done" i naciśnięto klawisz powrotu wywoływana jest funkcja głównav
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if settingsIterator == settingsLength - 1: # Prawda dla ostatniego ustawienia na liście
                    done = True
                    startgame = True

        # renderowanie (wybranych) ustawień
        for i in range(settingsLength):
            if i == settingsIterator:
                setText = font.render(settingsList[i], True, ownBlack, ownWhite)
                screen.blit(setText, (10, 20 + 20 * i + setText.get_height()))
                pygame.display.flip()
            else:
                setText = font.render(settingsList[i], True, ownWhite, ownBlack)
                screen.blit(setText, (10, 20 + 20 * i + setText.get_height()))
                pygame.display.flip()

    if startgame:
        if exists('resources/gamemusic.mp3'):
            pygame.mixer.init()
            playerMusic = pygame.mixer.music.load('resources/gamemusic.mp3')
            pygame.mixer.music.play(-1)
        screen.fill(ownBlack)
        main(screen, playerNumber, ballSpeed, playerSpeed, ballSize, paddleLength)


# -----Aktualizowanie wyświetlacza za pomocą tekstu-----
def renderAndUpdate(screen, text, textColor, backgroundColor, pos):
    font = pygame.font.SysFont("arialroundedmtbold", 24)
    if len(text) == 2:
        text += "  "
    elif len(text) == 1:
        text += "   "
    valueText = font.render(text, True, textColor, backgroundColor)
    screen.blit(valueText, pos)
    pygame.display.flip()


# -----Aktualizacja pozycji----- 
def updatePos(xPos, yPos, oldRect, screen, image):
    screen.fill(ownBlack)
    updatedRect = screen.blit(image, (xPos, yPos))
    font = pygame.font.SysFont("arialroundedmtbold", 18)
    goalText = font.render(str(goals[0]) + " : " + str(goals[1]), True, ownWhite, ownBlack)
    pygame.display.update(updatedRect)
    pygame.display.update(oldRect)
    pygame.display.update(screen.blit(goalText, (screenWidth // 2 - goalText.get_width() // 2, 10)))
    return updatedRect


# -----Główna funkcja--------------
def main(screen, playerCount, ballSpeed, playerSpeed, ballSize, paddleLength):
    clock = pygame.time.Clock()

    xstepB = ballSpeed
    ystepB = ballSpeed
    running = True  # Zmienna do sterowania pętlą główną

    playerImg = pygame.image.load("resources/player.png")  # Wczytywanie obrazu gracza
    playerImg = pygame.transform.scale(playerImg, (playerImg.get_size()[0],
                                       (int) (playerImg.get_size()[1] * [0.66, 1.0, 1.5][paddleLength]))) # ustawienie długości paletki 
    ballImg = pygame.image.load("resources/ball.png")
    ballImg = pygame.transform.scale(ballImg, [x * ballSize for x in ballImg.get_size()]) # ustawienie rozmiaru piłki 

    screen.fill(ownBlack)  # zmienianie tła na jednolity kolor (czarny)

    playerWidth = playerImg.get_width()  # Szerokośc gracza
    playerHeight = playerImg.get_height()  # Wysokość gracza
    xpos1 = 20  # pozycja x of the player 1
    xpos2 = screenWidth - 20 - playerWidth  # pozycja x of the player 2
    ypos1 = screenHeight // 2 - playerHeight // 2  # pozycja y of the player 1
    ypos2 = ypos1  # pozycja y of the player 2

    ballWidth = ballImg.get_width()  # szerokość piłki 
    ballHeight = ballImg.get_height()  # wysokość piłki 
    xposB = xpos1 + playerWidth + 10  # pozycja x piłki 
    yposB = ypos1 + playerHeight // 2 - ballHeight // 2  # pozycja y piłki 

    lastRects = [screen.blit(playerImg, (xpos1, ypos1)),  # sprawdzanie, która część planszy 
                 screen.blit(playerImg, (xpos2, ypos2)),  # musi zostać zmodyfikowana
                 screen.blit(ballImg, (xposB, yposB))]

    curRects = lastRects.copy()

    pygame.display.flip()  # Odświezanie planszy 

    firstStart = True
    upPressed = False
    downPressed = False
    wPressed = False
    sPressed = False

    # -----główna pętla-----
    while running:
        # ---obsługa zdarzeń, pobiera wszystkie zdarzenia z kolejki zdarzeń---
        clock.tick(FPS)

        if not firstStart:

            # ktoś zdobył punkt
            if (xposB >= screenWidth) or (xposB <= 0):
                firstStart = True
                if xposB >= screenWidth:
                    goals[0] += 1
                else:
                    goals[1] += 1

                # ustawianie piłki 
                xposB = screenWidth // 2 - ballWidth // 2 - xstepB
                yposB = screenHeight // 2 - ballHeight // 2 - ystepB

                # ustawianie prędkości piłki 
                xstepB = ballSpeed
                ystepB = ballSpeed

            # piłka cofająca, jeśli jest za oknem (górna lub dolna)
            if (yposB + ballHeight >= screenHeight) or (yposB <= 0): 
                ystepB = -ystepB

            # Kontrola zderzenia z graczem 1
            # jeśli piłka z prędkością byłaby na lewo od gracza 1
            if xposB - abs(xstepB) <= (xpos1 + playerWidth):
                # upDist = abs(yposB + ballHeight - ypos1)
                # downDist = abs(yposB - ypos1 - playerHeight)
                ystepBAbs = abs(ystepB)

                if (xposB - xstepB - 3 <= (xpos1 + playerWidth) and (
                        yposB + ballHeight >= ypos1 and yposB <= ypos1 + playerHeight)):
                    # Piłka weszła przez górę lub dół i nadal jest w paletce
                    ystepB = +ystepBAbs
                elif (yposB + ballHeight > ypos1) and (yposB < ypos1 + playerHeight):
                    xAccelerator = 1 if xstepB > 1 else -1
                    xstepB = (-xstepB - xAccelerator)
                    yAccelerator = 1 if ystepB > 1 else -1
                    ystepB += yAccelerator

            # Kontrola zderzenia z graczem 2
            # jeśli piłka z prędkością byłaby na lewo od gracza 2
            if (xposB + ballWidth) + abs(xstepB) >= xpos2:

                # upDist = abs(yposB + ballHeight - ypos2)
                # downDist = abs(yposB - ypos2 - playerHeight)
                ystepBAbs = abs(ystepB)

                if (xposB + ballWidth - xstepB + 3 >= xpos2) and (
                        yposB + ballHeight >= ypos2 and yposB <= ypos2 + playerHeight):
                    # Piłka weszła przez górę lub dół i nadal jest w paletce
                    ystepB = +ystepBAbs

                elif (yposB + ballHeight > ypos2) and (yposB < ypos2 + playerHeight):
                    xAccelerator = 1 if xstepB > 1 else -1
                    xstepB = (-xstepB - xAccelerator)
                    yAccelerator = 1 if ystepB > 1 else -1
                    ystepB += yAccelerator

            xposB += xstepB
            yposB += ystepB
            curRects[2] = updatePos(xposB, yposB, lastRects[2], screen, ballImg)
            lastRects[2] = curRects[2]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Event type = quit:
                running = False  # Zmiana running na False -> koniec działania głównej pętli gry 

            # Przełącza zmienną firstStart jeśli gra jest uruchomiona
            if firstStart:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    firstStart = False

            # Przełącza zmienne dla wciśniętych klawiszy, gdy są one wciśnięte lub zwolnione
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                downPressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                upPressed = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                sPressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                wPressed = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                downPressed = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                upPressed = False

            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                sPressed = False
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                wPressed = False

            # --- Bot --- #
        if playerCount == 1:
            if yposB > ypos2 + playerSpeed and ypos2 <= screenHeight - playerSpeed - playerHeight:
                # upPressed = False
                # downPressed = True
                ypos2 += playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            elif yposB < ypos2 - playerSpeed and ypos2 >= playerSpeed - playerHeight:
                # downPressed = False
                # upPressed = True
                ypos2 -= playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]

        # Faktycznie przesuwa graczy, jeśli zostanie naciśnięty klawisz
        # Pierwszy gracz
        if sPressed and ypos1 <= screenHeight - playerSpeed - playerHeight:
            ypos1 += playerSpeed
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]
        if wPressed and ypos1 >= playerSpeed:
            ypos1 -= playerSpeed
            curRects[0] = updatePos(xpos1, ypos1, lastRects[0], screen, playerImg)
            lastRects[0] = curRects[0]

            # Drugi gracz
        if playerCount == 2:
            if downPressed and ypos2 <= screenHeight - playerSpeed - playerHeight:
                ypos2 += playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]
            if upPressed and ypos2 >= playerSpeed:
                ypos2 -= playerSpeed
                curRects[1] = updatePos(xpos2, ypos2, lastRects[1], screen, playerImg)
                lastRects[1] = curRects[1]


if __name__ == "__main__":  
    init()  
