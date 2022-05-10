import pygame, random, sys, time
from pygame.locals import *

#set up some variables

WINDOWWIDTH = 1024   #kích thước chiều rộng là 1024   
WINDOWHEIGHT = 600  #kích thước chiều cao là 600
FPS = 60            # Thiết lập chỉ số khung hình trên giây

MAXGOTTENPASS = 10   
ZOMBIESIZE = 70
ADDNEWZOMBIERATE = 50
ADDNEWKINDZOMBIE = ADDNEWZOMBIERATE

NORMALZOMBIESPEED = 2
NEWKINDZOMBIESPEED = NORMALZOMBIESPEED/2     #Kích thước và tốc độ

PLAYERMOVERATE = 15
BULLETSPEED = 12
ADDNEWBULLETRATE = 15

TEXTCOLOR = (255, 255, 255)
RED = (255, 0, 0)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # nhấn nút thoát
                    terminate()
                if event.key == K_RETURN:
                    return

def playerHasHitZombie(playerRect, zombies):  # Người chơi đã đụng trúng zombie
    for z in zombies:
        if playerRect.colliderect(z['rect']):
            return True
    return False

def bulletHasHitZombie(bullets, zombies):  # Đạn trúng zombie
    for b in bullets:
        if b['rect'].colliderect(z['rect']):
            bullets.remove(b)
            return True
    return False

def bulletHasHitCrawler(bullets, newKindZombies): # Đạn trúng zombie
    for b in bullets:
        if b['rect'].colliderect(c['rect']):
            bullets.remove(b)
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# thiết lập pygame, cửa sổ và con trỏ chuột
pygame.init()   #khởi tạo tất cả các mô-đun cần thiết cho PyGame.
mainClock = pygame.time.Clock() #Xác định FPS
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #Tạo màn hành hiển thị 
pygame.display.set_caption('Plants and zombies') #Tên trò chơi
pygame.mouse.set_visible(False) # Thiết lập hiển thị con trỏ

# front chữ
font = pygame.font.SysFont(None, 50)

# Thiết lập âm thanh
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('grasswalk.mp3')

# Thiết lập hoạt ảnh
playerImage = pygame.image.load('SnowPea.gif')
playerRect = playerImage.get_rect()

bulletImage = pygame.image.load('SnowPeashooterBullet.gif')
bulletRect = bulletImage.get_rect()

zombieImage = pygame.image.load('tree.png')
newKindZombieImage = pygame.image.load('tree2.png')

backgroundImage = pygame.image.load('background.png')
rescaledBackground = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

# Hiển thị màn hành bắt đầu
windowSurface.blit(rescaledBackground, (0, 0))
windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
drawText('PLANT VS ZOMBIE!', font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 4))
drawText('Press Enter to start', font, windowSurface, (WINDOWWIDTH / 3) - 10, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()
while True:

    # thiết lập bắt đầu trò chơi

    zombies = []
    newKindZombies = []
    bullets = []

    zombiesGottenPast = 0
    score = 0

    playerRect.topleft = (50, WINDOWHEIGHT /2)
    moveLeft = moveRight = False
    moveUp=moveDown = False
    shoot = False

    zombieAddCounter = 0
    newKindZombieAddCounter = 0
    bulletAddCounter = 40
    pygame.mixer.music.play(-1, 0.0)

    # Cài đặt phím tắt cho người chơi
    while True: # vòng lặp trò chơi chạy trong khi người chơi đang chơi
        for event in pygame.event.get(): #Lấy ra các sự kiện xảy ra
            if event.type == QUIT: #Phát hiện thao tác thoát khỏi trò chơi của người dùng
                terminate()
            
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

                if event.key == K_SPACE:
                    shoot = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
                if event.key == K_SPACE:
                    shoot = False

        # Đưa zombies vào màn hình
        zombieAddCounter += 1
        if zombieAddCounter == ADDNEWKINDZOMBIE:
            zombieAddCounter = 0
            zombieSize = ZOMBIESIZE       
            newZombie = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-zombieSize-10), zombieSize, zombieSize),
                        'surface':pygame.transform.scale(zombieImage, (zombieSize, zombieSize)),
                        }

            zombies.append(newZombie)

        # Đưa zombies vào màn hình
        newKindZombieAddCounter += 1
        if newKindZombieAddCounter == ADDNEWZOMBIERATE:
            newKindZombieAddCounter = 0
            newKindZombiesize = ZOMBIESIZE
            newCrawler = {'rect': pygame.Rect(WINDOWWIDTH, random.randint(10,WINDOWHEIGHT-newKindZombiesize-10), newKindZombiesize, newKindZombiesize),
                        'surface':pygame.transform.scale(newKindZombieImage, (newKindZombiesize, newKindZombiesize)),
                        }
            newKindZombies.append(newCrawler)

        # Đưa đạn vào màn hình
        bulletAddCounter += 1
        if bulletAddCounter >= ADDNEWBULLETRATE and shoot == True:
            bulletAddCounter = 0
            newBullet = {'rect':pygame.Rect(playerRect.centerx+10, playerRect.centery-25, bulletRect.width, bulletRect.height),
                         'surface':pygame.transform.scale(bulletImage, (bulletRect.width, bulletRect.height)),
                        }
            bullets.append(newBullet)

        # Chuyển động của người chơi
        if moveUp and playerRect.top > 30:
            playerRect.move_ip(0,-1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT-10:
            playerRect.move_ip(0,PLAYERMOVERATE)

        # Chuyển động của zombies
        for z in zombies:
            z['rect'].move_ip(-1*NORMALZOMBIESPEED, 0)

        # Chuyển động của zombies
        for c in newKindZombies:
            c['rect'].move_ip(-1*NEWKINDZOMBIESPEED,0)

        # Chuyển động của đạn
        for b in bullets:
            b['rect'].move_ip(1 * BULLETSPEED, 0)

        # Xóa zombies khi tới đích
        for z in zombies[:]:
            if z['rect'].left < 0:
                zombies.remove(z)
                zombiesGottenPast += 1

        # Xóa zombies khi tới đích
        for c in newKindZombies[:]:
            if c['rect'].left <0:
                newKindZombies.remove(c)
                zombiesGottenPast += 1
        
        for b in bullets[:]:
            if b['rect'].right>WINDOWWIDTH:
                bullets.remove(b)
                
        # Kiểm tra đạn trúng zombies
        for z in zombies:
            if bulletHasHitZombie(bullets, zombies):
                score += 1
                zombies.remove(z)
    
        for c in newKindZombies:
            if bulletHasHitCrawler(bullets, newKindZombies):
                score += 1
                newKindZombies.remove(c)      

        # Vẽ thế giới trò chơi trên cửa sổ.
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, playerRect)   
        for z in zombies:
            windowSurface.blit(z['surface'], z['rect'])

        for c in newKindZombies:
            windowSurface.blit(c['surface'], c['rect'])

        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # Đưa ra số điểm và bao nhiêu thây ma đã vượt qua
        drawText('zombies gotten past: %s' % (zombiesGottenPast), font, windowSurface, 10, 20)
        drawText('score: %s' % (score), font, windowSurface, 10, 50)

        # update lại màn hình
        pygame.display.update()
            
        # Kiểm tra xem có zombies đụng trúng người chơi.
        if playerHasHitZombie(playerRect, zombies):
            break
        if playerHasHitZombie(playerRect, newKindZombies):
           break
        
        # Kiểm tra xem số zombies vượt qua
        if zombiesGottenPast >= MAXGOTTENPASS:
            break

        mainClock.tick(FPS)

    # Dừng trò chơi và hiển thị màn hình "Game Over"
    pygame.mixer.music.stop()
    gameOverSound.play()
    time.sleep(1)
    if zombiesGottenPast >= MAXGOTTENPASS:
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('CRAZY DAVE DIE', font, windowSurface, (WINDOWWIDTH / 4)- 80, (WINDOWHEIGHT / 3) + 100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update() 
        waitForPlayerToPressKey()              
    if playerHasHitZombie(playerRect, zombies):
        windowSurface.blit(rescaledBackground, (0, 0))
        windowSurface.blit(playerImage, (WINDOWWIDTH / 2, WINDOWHEIGHT - 70))
        drawText('score: %s' % (score), font, windowSurface, 10, 30)
        drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('YOU HAVE BEEN KILLED BY THE ZOMMBIE', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) +100)
        drawText('Press enter to play again or escape to exit', font, windowSurface, (WINDOWWIDTH / 4) - 80, (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey()
    gameOverSound.stop()
