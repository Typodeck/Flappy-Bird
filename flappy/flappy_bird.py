#from curses import KEY_DOWN
import random 
import sys 
import pygame
from pygame.locals import * 

fps=32
screenwidth=289
screenheight=511
screen=pygame.display.set_mode((screenwidth,screenheight))
groundY=0.8*screenheight
gameSprites={}
gameSounds={}
player='gallery/sprites/bird.png'
background='gallery/sprites/background.png'
pipe='gallery/sprites/pipe.png'

def welcomeScreen():
    playerx=int(screenwidth/5)
    playery=int((screenheight-gameSprites['player'].get_height())/2)
    messagex=int((screenwidth-gameSprites['message'].get_width())/2)
    messagey=int(screenheight*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            # if user presses cross or escape key ,close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if user presses space or up key ,start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                screen.blit(gameSprites['background'],(0,0))
                screen.blit(gameSprites['player'],(playerx,playery))
                screen.blit(gameSprites['message'],(messagex,messagey))
                screen.blit(gameSprites['base'],(basex,groundY))
                pygame.display.update() #screen doesn't changes
                fpsClock.tick(fps)
                

def mainGame():
    score=0
    playerX=int(screenwidth/5)
    playerY=int(screenwidth/2)
    basex=0

    pipe1=getRandompipe()
    pipe2=getRandompipe()

    upperpipes=[{'x':screenwidth+200,'y':pipe1[0]['y']},
               {'x':screenwidth+200+(screenwidth/2),'y':pipe2[0]['y']}]
    lowerpipes=[{'x':screenwidth+200,'y':pipe1[1]['y']},
               {'x':screenwidth+200+(screenwidth/2),'y':pipe2[1]['y']}]

    pipeVelX=-4

    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1

    playerFlapVelY=-8 # velocity while flapping
    playerFlapped=False # true when bird is flapping

    while True:
        for event in pygame.event.get():
            # if user presses cross or escape key ,close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playerY>0:
                    playerVelY=playerFlapVelY
                    playerFlapped=True
                    gameSounds['wing'].play()

        crash=isCollide(playerX,playerY,upperpipes,lowerpipes) # return true if player crashed
        if crash:
            return
        
        #check score
        playerMidpos=playerX+gameSprites['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos=pipe['x']+gameSprites['pipe'][0].get_width()/2
            if pipeMidpos<=playerMidpos<pipeMidpos+4:
                score+=1
                print(f"SCORE:{score}")
                gameSounds['point'].play()

        if playerVelY<playerMaxVelY and not playerFlapped:
            playerVelY+=playerAccY

        if playerFlapped:
            playerFlapped=False

        playerHeight=gameSprites['player'].get_height()
        playerY=playerY+min(playerVelY,(groundY-playerHeight-playerY))

        #moves pipe to the left
        for upperpipe, lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipeVelX
            lowerpipe['x']+=pipeVelX

        # add new pipe
        if 0<upperpipes[0]['x']<5:
            newPipe=getRandompipe()
            upperpipes.append(newPipe[0])
            lowerpipes.append(newPipe[1])


        # remove pipe which is out of the screen
        if upperpipes[0]['x']< -gameSprites['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        screen.blit(gameSprites['background'],(0,0))
        for upperpipe, lowerpipe in zip(upperpipes,lowerpipes):
            screen.blit(gameSprites['pipe'][0],(upperpipe['x'],upperpipe['y']))
            screen.blit(gameSprites['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        screen.blit(gameSprites['base'],(basex,groundY))
        screen.blit(gameSprites['player'],(playerX,playerY))

        digits=[int(x) for x in list(str(score))]
        width=0
        for digit in digits:
            width+=gameSprites['numbers'][digit].get_width()
        Xoffset=(screenwidth-width)/2

        for digit in digits:
            screen.blit(gameSprites['numbers'][digit],(Xoffset,screenheight*0.12))
            Xoffset+=gameSprites['numbers'][digit].get_width()

        pygame.display.update() 
        fpsClock.tick(fps)


def isCollide(playerX,playerY,upperpipes,lowerpipes):
    if playerY>groundY-25 or playerY<0:
        gameSounds['hit'].play() 
        return True

    for pipe in upperpipes:
        pipeHeight=gameSprites['pipe'][0].get_height()
        if(playerY<pipeHeight+pipe['y'] and abs(playerX-pipe['x'])<gameSprites['pipe'][0].get_width()):
            gameSounds['hit'].play() 
            return True

    for pipe in lowerpipes:
        if(playerY+gameSprites['player'].get_height()>pipe['y'] and abs(playerX-pipe['x'])<gameSprites['pipe'][0].get_width()):
            gameSounds['hit'].play() 
            return True

    return False


def getRandompipe():
    pipeHeight=gameSprites['pipe'][0].get_height()
    offset=screenheight/3
    y2=offset+random.randrange(0,int(screenheight-gameSprites['base'].get_height()-1.2*offset))
    y1=pipeHeight-y2+offset
    pipeX=screenwidth+10
    pipe=[{'x': pipeX, 'y':-y1}, #upper pipe
          {'x':pipeX , 'y':y2}] #lower pipe

    return pipe




if __name__ == "__main__":
    pygame.init()
    fpsClock=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    gameSprites['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    gameSprites['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    gameSprites['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    gameSprites['pipe']=(
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
        pygame.image.load(pipe).convert_alpha()
    )
    gameSprites['background']=pygame.image.load(background).convert()
    gameSprites['player']=pygame.image.load(player).convert_alpha()

    gameSounds['die']=pygame.mixer.Sound('gallery/audio/die.wav')
    gameSounds['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
    gameSounds['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    gameSounds['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')
    gameSounds['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')

    welcomeScreen()
    mainGame()




    #print('hello')






