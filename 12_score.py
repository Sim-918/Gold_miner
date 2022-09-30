#게임의 스코어(점수) 처리
#목표점수
#현재점수

import pygame
import os
import math
#집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image=image
        self.original_image=image
        self.rect=image.get_rect(center=position)

    #접게의 이동될 위치
        self.offset=pygame.math.Vector2(default_offset_x_claw,0)
        self.position=position
    
    #집게의 이동방향
        self.direction=LEFT     
        self.angle_speed= 2.5 #집계의 각도변경 폭 (좌우 이동속도)
        self.angle=10         #최초각도 (오른쪽 끝)
        

    #집게 이동 함수
    def update(self,to_x):
        if self.direction==LEFT: #왼쪽방향으로 이동하고 있다 면
            self.angle+=self.angle_speed    #이동속도(angle_speed)만큼 각도 증가
        elif self.direction==RIGHT:  #오른쪽 방향으로 이동 하고 있다 면
            self.angle-=self.angle_speed
        #만약 허용 각도 범위를 벗어나면
        if self.angle>170:
            self.angle=170
            self.set_direction(RIGHT)
        elif self.angle<10:
            self.angle=10
            self.set_direction(LEFT)
        
        self.offset.x+=to_x

        self.rotate()   #회전처리

        
        # rect_center=self.position+self.offset
        # self.rect=self.image.get_rect(center=rect_center)
        #print(self.angle,self.direction)
        
    #집게 회전 함수
    def rotate(self):
        #회전하고나서 새롭게 이미지 전환
        self.image=pygame.transform.rotozoom(self.original_image,-self.angle,1)   #회전 대상 이미지,회전 각도(음수), 이미지 크기

        offset_rotated=self.offset.rotate(self.angle)
        #print(offset_rotated)

        #rect의 범위를 벗어서 회전 할때마다 값이 고정되어 회전하는데 아래코드를 적으면 회전할때마다 rect의 크기가 맞춰지면서 회전함
        self.rect=self.image.get_rect(center=self.position+offset_rotated)

        #print(self.rect)
        #pygame.draw.rect(screen,RED,self.rect,1)

    def set_direction(self,direction):
        self.direction=direction

    #보석클래스에서 draw라는 함수를 한번써서 다시정의
    def draw(self,screen):
        screen.blit(self.image,self.rect)   #이미지,좌표
        #중심 찾기
        #pygame.draw.circle(screen,RED,self.position,3)  #중심점 표시
        #직선그리기(screen에다 검은색으로 self.position(화면 중심 위치)에서 부터 self.rect(집게이미지 직사각형)의 중심까지 두께는 5)
        pygame.draw.line(screen,BLACK,self.position,self.rect.center,5)
    
    #집게가 돌아오고 다시 회전하는 함수
    def set_init_state(self):
        self.offset.x=default_offset_x_claw
        self.angle=10
        self.direction=LEFT

#보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self,image,position,price,speed): 
        super().__init__()
        self.image=image                 #게임 이미지 데이터
        self.rect=image.get_rect(center=position)       #캐릭터가 가지는 데이터
        self.price=price    #보석 가치
        self.speed=speed    #보석에 충돌하고 따른 돌아오는 속도
    
    #각도에 따른 보석 가운데에 오기위한 함수(set_position.png) 보석을 끌고오는 함수
    def set_position(self,position,angle):
        r=self.rect.size[0]//2     #rect의 0번째 값=사각형의 높이에서 2를 나눈 값 즉 반지름 
        rad_angle=math.radians(angle)       #집게의 각도 즉 집게를 중심으로부터 출발했을 때의 각도(θ)
        #claw이미지의 반지름만큼 보석이미지가 닿으면 보석이미지를 끌어옴 
        #claw이미지의 반지름과 보석들의 이미지반지름 
        #claw이미지의 중심좌표가 필요하고 보석이미지의 중심좌표가 필요함 
        #claw center=x,y 라고 가정하고 보석이미지의 좌표는 x',y'라고 가정하면
        #(x+x',y+y') 즉 이 좌표가 됬을 때 보석을 끌어옴
        #각 좌표를 구하기 위해서는 sin함수와 cos함수가 필요함
        to_x=r*math.cos(rad_angle)  #삼각형의 밑변
        to_y=r*math.sin(rad_angle)  #삼격형의 높이
        self.rect.center=(position[0]+to_x,position[1]+to_y)    #집게 이미지의 중심점

def setup_gemstone():

    #각 보석 별 가치 (price), 속도(speed)
    small_gold_price,small_gold_speed=100,5
    big_gold_price,big_gold_speed=300,2
    stone_price,stone_speed=10,2
    diamond_price,diamond_speed=600,7

    #작은 금
    small_gold=Gemstone(gemstone_images[0],(200,380),small_gold_price,small_gold_speed)   #0번째의 이미지를 (200,380)위치
    gemstone_group.add(small_gold) #그룹에 추가
    #큰 금
    gemstone_group.add(Gemstone(gemstone_images[1],(300,500),big_gold_price,big_gold_speed))
    #돌
    gemstone_group.add(Gemstone(gemstone_images[2],(500,500),stone_price,stone_speed))
    #다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3],(900,700),diamond_price,diamond_speed))

#점수 함수
def update_score(score):
    global curr_score
    curr_score+=score

#점수 정보를 보여주는 함수
def display_score():
    txt_curr_score=game_font.render(f"Curr Score: {curr_score:,}",True,BLACK)
    screen.blit(txt_curr_score,(50,20))

    txt_goal_socre=game_font.render(f"Goal Score: {goal_score:,}",True,BLACK)
    screen.blit(txt_goal_socre,(50,80))

#게임 환경
pygame.init()
screen_width=1280
screen_height=720
screen=pygame.display.set_mode((screen_width,screen_height))        #크기에 맞는 GUI
pygame.display.set_caption("Gold Miner")                            #제목
clock=pygame.time.Clock()
game_font=pygame.font.SysFont("arialrounded",30)

#점수관련 변수
goal_score=1500     #목표점수
curr_score=0        #현재점수



#게임 관련 변수
default_offset_x_claw= 40 #중심점으로부터 집게까지의 기본 x간격()
to_x=0  #x좌표 기준으로 집게이미지를 이동시킬 값 저장 변수
caught_gemstone=None    #집게를 뻗어서 잡은보석정보



#속도 변수
move_speed=12   #발사할때 이동 스피드(x좌표기준으로 증가 되는 값)
return_speed=20 #아무것도 없이 돌아오는 스피드

#방향변수
LEFT=-1 #왼쪽 방향
RIGHT=1 #오른쪽 방향
STOP=0  #이동 방향이 좌우가 아닌 고정인 상태(집게를 뻗는 상태)

#색깔 변수
RED=(255,0,0)   #RGB,빨간색
BLACK=(0,0,0)   #RGB,검은색


#배경 이미지 불러오기
current_path=os.path.dirname(__file__)      #현재 디렉토리 위치 반환
background=pygame.image.load(os.path.join(current_path,"background.png"))

#4개 보석 이미지 불러오기(작은 금,큰 금, 돌, 다이이몬드)
#리스트로 관리
gemstone_images=[
    pygame.image.load(os.path.join(current_path,"small_gold.png")).convert_alpha(),  #작은금
    pygame.image.load(os.path.join(current_path,"big_gold.png")).convert_alpha(),    #큰 금
    pygame.image.load(os.path.join(current_path,"stone.png")).convert_alpha(),       #돌
    pygame.image.load(os.path.join(current_path,"diamond.png")).convert_alpha(),]    #다이이몬드

# 보석 그룹
gemstone_group=pygame.sprite.Group()
setup_gemstone()    #게임의 원하는 만큼의 보석을 정의

#집게 이미지 불러오기
claw_image=pygame.image.load(os.path.join(current_path,"claw.png")).convert_alpha()
claw=Claw(claw_image,(screen_width//2,110))     #가로위치는 화면 가로를 2로 나눈 좌표,세로위치는 위에서 110


#게임 루프
runnig=True
while runnig:
    clock.tick(30)  #FPS 값이 30으로 고정
    for event in pygame.event.get():        
        if event.type ==pygame.QUIT:
            runnig=False
        if event.type==pygame.MOUSEBUTTONDOWN:  #마우스 버튼 누를때 
            claw.set_direction(STOP)    #좌우 멈춤
            to_x=move_speed #move_speed만큼 빠르게 뻗음

    #경계값일때 집게status
    #집게이미지왼쪽이 0보다 작거나 집게이미지 오른쪽이 screen 넓이보다 크거나 집게이미지바텀부분이 screen높이보다 크면
    if claw.rect.left<0 or claw.rect.right>screen_width or claw.rect.bottom>screen_height:
        to_x=-return_speed
    if claw.offset.x<default_offset_x_claw: #원위치에 오면
        to_x=0
        claw.set_init_state()   #처음상태로 돌아감

        if caught_gemstone: #잡힌 보석이 있다면
            update_score(caught_gemstone.price)    #점수 업데이트 처리(later)
            gemstone_group.remove(caught_gemstone)  #그룹에서 잡힌 보석은 제외
            caught_gemstone=None

    if not caught_gemstone: #잡힌보석이 없다면 충돌 체크
        for gemstone in gemstone_group:
            #if claw.rect.colliderect(gemstone.rect):       #직사각형기준으로 충돌처리
            if pygame.sprite.collide_mask(claw,gemstone):   #투명영역은 제외하고 실제 이미지 영역은 부분에 충돌처리
                caught_gemstone=gemstone    #잡힌 보석 정보
                to_x=-gemstone.speed        #잡힌 보석의 속도에 -한 값을 설정
                break
    
    if caught_gemstone: #잡힌보석이 있으면 업데이트 하는 문
        caught_gemstone.set_position(claw.rect.center,claw.angle)


    screen.blit(background,(0,0))

    gemstone_group.draw(screen) #gemstone_group의 데이터를 screen에 그려줌
    claw.update(to_x)
    claw.draw(screen)

    #점수 정보를 보여주는 함수호출
    display_score()

    pygame.display.update()
    
pygame.quit()