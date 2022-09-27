#집게 클래스 만들기
import pygame
import os

#집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image=image
        self.rect=image.get_rect(center=position)
        
    #보석클래스에서 draw라는 함수를 한번써서 다시정의
    def draw(self,screen):
        screen.blit(self.image,self.rect)   #이미지,좌표


#보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self,image,position): 
        super().__init__()
        self.image=image                 #게임 이미지 데이터
        self.rect=image.get_rect(center=position)       #캐릭터가 가지는 데이터

def setup_gemstone():
    #작은 금
    small_gold=Gemstone(gemstone_images[0],(200,380))   #0번째의 이미지를 (200,380)위치
    gemstone_group.add(small_gold) #그룹에 추가
    #큰 금
    gemstone_group.add(Gemstone(gemstone_images[1],(300,500)))
    #돌
    gemstone_group.add(Gemstone(gemstone_images[2],(500,500)))
    #다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3],(900,700)))

#보석 이미지 불러오기
pygame.init()
screen_width=1280
screen_height=720
screen=pygame.display.set_mode((screen_width,screen_height))        #크기에 맞는 GUI
pygame.display.set_caption("Gold Miner")                            #제목
clock=pygame.time.Clock()

#배경 이미지 불러오기
current_path=os.path.dirname(__file__)      #현재 디렉토리 위치 반환
background=pygame.image.load(os.path.join(current_path,"background.png"))

#4개 보석 이미지 불러오기(작은 금,큰 금, 돌, 다이이몬드)
#리스트로 관리
gemstone_images=[
    pygame.image.load(os.path.join(current_path,"small_gold.png")),  #작은금
    pygame.image.load(os.path.join(current_path,"big_gold.png")),    #큰 금
    pygame.image.load(os.path.join(current_path,"stone.png")),       #돌
    pygame.image.load(os.path.join(current_path,"diamond.png")),]    #다이이몬드

# 보석 그룹
gemstone_group=pygame.sprite.Group()
setup_gemstone()    #게임의 원하는 만큼의 보석을 정의

#집게 이미지 불러오기
claw_image=pygame.image.load(os.path.join(current_path,"claw.png"))
claw=Claw(claw_image,(screen_width//2,110))     #가로위치는 화면 가로를 2로 나눈 좌표,세로위치는 위에서 110


#게임 루프
runnig=True
while runnig:
    clock.tick(30)  #FPS 값이 30으로 고정
    for event in pygame.event.get():        
        if event.type ==pygame.QUIT:
            runnig=False
    screen.blit(background,(0,0))

    gemstone_group.draw(screen) #gemstone_group의 데이터를 screen에 그려줌
    claw.draw(screen)

    pygame.display.update()
    
pygame.quit()