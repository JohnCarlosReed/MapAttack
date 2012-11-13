'''
MapAttack is a Space Invaders-like Arcade game using Google Maps imagery

Created on Oct 22, 2012

@author: johnreed

Requirements:  You need to have Python 2.7 installed and pygame for 2.7
'''

import pygame, sys, random

# CONSTANTS
DISPLAYWIDTH = 500
DISPLAYHEIGHT = 600
NPC_START_Y = -20
FPS = 30
TEXTCOLOR = (255,0,0)

# GLOBALS -----------
max_npcs = 100   # npc = "non-player character" or "enemy" 
spawn_rate = 50  # number of while loop wait cycles
player_move_rate = 3
player_lives = 3 # would be nice to display this
npcs = []
player_bullets = []
score = 0


class Npc:
    def __init__(self):
        self.x = random.randint(10, DISPLAYWIDTH-10)
        self.y = NPC_START_Y
        self.move_rate = random.randint(3,8) 
        self.image = pygame.image.load('red.png')
        self.rect = pygame.Rect(self.x,self.y,15,30)
        
class PlayerBullet:
    def __init__(self, x, y):
        self.move_rate = 5 
        self.image = pygame.image.load('blue-pushpin.png')
        self.image = pygame.transform.scale(self.image, (11, 20))
        self.rect = pygame.Rect(x,y,15,30)


def terminate():
    pygame.quit()
    sys.exit()

def wait_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # pressing escape quits
                    terminate()
                return
            
def display_start_screen():
    font = pygame.font.SysFont(None, 48)
    textobj = font.render("Map Attack!", 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (DISPLAYWIDTH/3, DISPLAYHEIGHT/3)
    DISPLAY.blit(textobj, textrect)
    
    font = pygame.font.SysFont(None, 24)
    textobj = font.render("Press Any Key to Start", 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (DISPLAYWIDTH/3, DISPLAYHEIGHT/3 + 100)
    DISPLAY.blit(textobj, textrect)
    
    font = pygame.font.SysFont(None, 16)
    textobj = font.render("v0.1 John Reed johnnycarlos@gmail.com", 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (10, DISPLAYHEIGHT-25)
    DISPLAY.blit(textobj, textrect)    
    
    pygame.display.update()
    
def display_game_over_screen():
    font = pygame.font.SysFont(None, 64)
    textobj = font.render("GAME OVER!", 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (DISPLAYWIDTH/3-50, DISPLAYHEIGHT/3)
    DISPLAY.blit(textobj, textrect)
    pygame.display.update()

def display_score():
    font = pygame.font.SysFont(None, 30)
    textobj = font.render(str(score), 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (10, 6)
    DISPLAY.blit(textobj, textrect)
    
def check_lives_left():
    global player_lives
    global npcs
    npcs = []  # remove all enemies when player loses a life
    if (player_lives == 1):
        display_game_over_screen()
        wait_for_keypress()
        terminate()
    else:
        player_lives = player_lives - 1
        

pygame.init()

fpsClock = pygame.time.Clock()

DISPLAY = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), 0, 32)

pygame.display.set_caption('Map Attack!')

playerImg = pygame.image.load('player.png')

player = pygame.Rect(DISPLAYWIDTH/2, DISPLAYHEIGHT-50, 20, 25)

direction = 'stop'

background_position=[0,0]

background_image = pygame.image.load("mapbackground.png").convert()

npcs.append(Npc()) #  add first enemy

display_start_screen()

wait_for_keypress()

count = 1 #counts loops for calculating npc spawn rate

while True: 
    
    DISPLAY.blit(background_image, background_position)
    
    if direction == 'right':
        player.right += player_move_rate
        if player.right >= DISPLAYWIDTH: # acct for image width or it goes offscreen
            direction = 'stop'
    elif direction == 'down':
        player.bottom += player_move_rate
        if player.bottom >= DISPLAYHEIGHT: # acct for image height or it goes offscreen
            direction = 'stop'
    elif direction == 'left':
        player.left -= player_move_rate
        if player.left <= 0:
            direction = 'stop'
    elif direction == 'up':
        player.top -= player_move_rate
        if player.top <= 0:
            direction = 'stop'

    DISPLAY.blit(playerImg, player)
    
    # Player leveling.  As score increases, so does spawn rate
    # Would be nice to display "current level"
    if( score == 10):    spawn_rate = 25
    if( score == 100):   spawn_rate = 10
    if( score == 1000):  spawn_rate = 5
    if( score == 10000): spawn_rate = 1
     
    # each time through the game loop we test to see if more
    # npcs are needed by modulus.  As the score gets higher,
    # npcs are added at a faster pace
    if ( len(npcs)<max_npcs and (count%spawn_rate == 0) ):
        npcs.append(Npc())
     
    for npc in npcs[:]:  # use copy so as to not remove elements while counting them
        if player.colliderect(npc):
            check_lives_left()

        npc.rect.bottom += npc.move_rate
        if npc.rect.bottom >= DISPLAYHEIGHT:
            npc.rect.bottom = NPC_START_Y
            npc.rect.x = random.randint(10, DISPLAYWIDTH - 10)
        DISPLAY.blit(npc.image, npc.rect)


    for bullet in player_bullets:
        successful_hit = bullet.rect.collidelistall(npcs)
        for npc in successful_hit:
            npcs.pop(npc)
            
            try:
                player_bullets.remove(bullet)
            except:
                pass
            
            score += 1
            
        bullet.rect.top -= bullet.move_rate
        
        if(bullet.rect.top < -20): # 20 pixs above display
            try:
                player_bullets.remove(bullet)
            except:
                pass
            
        DISPLAY.blit(bullet.image, bullet.rect)
        
                            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'up'
            if event.key == pygame.K_DOWN:
                direction = 'down'
            if event.key == pygame.K_LEFT:
                direction = 'left'
            if event.key == pygame.K_RIGHT:
                direction = 'right'
            if event.key == pygame.K_SPACE:
                player_bullets.append(PlayerBullet(player.x+4,player.y))
        if event.type == pygame.KEYUP:  #stop player moving when keyup(except spacebar)
            if event.key != pygame.K_SPACE:
                direction = 'stop'
                
    display_score()            
    pygame.display.update()
    fpsClock.tick(FPS)
    count += 1