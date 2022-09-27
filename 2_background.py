#배경이미지 불러오기
import pygame
import os


pygame.init()
screen_width=1280
screen_height=720
screen=pygame.display.set_mode((screen_width,screen_height))        #크기에 맞는 GUI
pygame.display.set_caption("Gold Miner")                            #제목
clock=pygame.time.Clock()

#배경 이미지 불러오기
current_path=os.path.dirname(__file__)      #현재 디렉토리 위치 반환
background=pygame.image.load(os.path.join(current_path,"background.png"))


#게임 루프
runnig=True
while runnig:
    clock.tick(30)  #FPS 값이 30으로 고정
    for event in pygame.event.get():        
        if event.type ==pygame.QUIT:
            runnig=False
    screen.blit(background,(0,0))
    pygame.display.update()

pygame.quit()