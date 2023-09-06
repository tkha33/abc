import pygame
from pygame.locals import *
import random
pygame.init()
#Màu nền
gray=(100,0,0)
green=(76,208,56)
yellow=(255,232,0)
red=(200,0,0)
white=(255,255,255)
#Tạo cửa sổ game
width=500
height=500
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption('Game đua xe')
#khởi tạo biến
gameover=False
speed=2
score=0
#đường xe chạy
road_width=300
street_width=10
street_height=50
#làn đường
lane_left=150
lane_center=250
lane_right=350
lanes=[lane_left,lane_center,lane_right]
lane_move_y=0
#đường xe và biên
road=(100,0,road_width,height)
left_edge=(95,0,street_width,height)
right_edge=(395,0,street_width,height)
#vị trí ban đầu xe
player_x=250
player_y=400
#đối tượng xe địch-vehicle
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)  
        #tỉ lệ hình
        image_scale= 45 / image.get_rect().width
        new_width = image.get_rect().width *image_scale
        new_height = image.get_rect().height *image_scale
        self.image = pygame.transform.scale(image,(new_width,new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
#xe player
class PlayerVehicle(Vehicle):
    def __init__(self,x,y):
        image = pygame.image.load('images/car.png')
        super().__init__(image,x,y)
#spriter groups(nhóm đối tượng hình 2d groups)
player_group = pygame.sprite.Group()
Vehicle_group = pygame.sprite.Group()
#tạo xe người chơi
player= PlayerVehicle(player_x,player_y)
player_group.add(player)
# xe lưu thông
image_name=['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
Vehicle_images = []
for name in image_name:
    image=pygame.image.load('images/' + name)
    Vehicle_images.append(image)
#load hình va chạm
crash=pygame.image.load('images/crash.png')
crash_rect=crash.get_rect()
#cài đặt fps
clock=pygame.time.Clock()
fps=120
#vòng lặp xử lý game
running=True
while running:
    #chỉnh frame hình trên giây
    clock.tick(fps)
    for event in pygame.event.get():     
        if event.type==QUIT:
            running=False
        #điều khiển xe(..............)
        if event.type==KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0]>lane_left:
                player.rect.x -=100
            if event.key == K_RIGHT and player.rect.center[0]<lane_right:
                player.rect.x +=100
        #check va chạm xe chạy
        for verhicle in Vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover=True
    #check va chạm khi xe đứng yên
    if pygame.sprite.spritecollide(player,Vehicle_group,True):
        gameover=True
        crash_rect.center = [player.rect.center[0],player.rect.top]
    #vẽ hình cỏ
    screen.fill(green)
    #đường chạy
    pygame.draw.rect(screen,gray,road)
    #vẽ biên đường
    pygame.draw.rect(screen,yellow,left_edge)
    pygame.draw.rect(screen,yellow,right_edge)
    #vẽ làn đường
    lane_move_y+=speed *2
    if lane_move_y >=street_height *2:
        lane_move_y=0
    for y in range(street_height* -2,height,street_height* 2):
        pygame.draw.rect(screen,white,(lane_left+45 ,y + lane_move_y,street_width,street_height))
        pygame.draw.rect(screen,white,(lane_center+45 ,y + lane_move_y,street_width,street_height))
    #vẽ xe player
    player_group.draw(screen)
    #vẽ phương thiện giao thông
    if len(Vehicle_group) <2:
        add_verhicle = True
        for verhicle in Vehicle_group:
            if verhicle.rect.top < verhicle.rect.height *1.5:
                add_verhicle = False
        if add_verhicle:
            lane= random.choice(lanes)
            image= random.choice(Vehicle_images)
            verhicle=Vehicle(image,lane,height / -2)
            Vehicle_group.add(verhicle)
    #Cho xe giao thông cản chạy
    for vehicle in Vehicle_group:
        vehicle.rect.y +=speed

        #remove verhicle
        if vehicle.rect.top >=height:
            vehicle.kill()
            score +=1
            #tăng tốc độ chạy xe player(bỏ được)
            if score>0 and score % 5 ==0:
                speed+=1
    #vẽ nhóm xe giao thông cản
    Vehicle_group.draw(screen)
    #hiển thị điểm(.....)
    font= pygame.font.Font(pygame.font.get_default_font(),16)
    text=font.render(f'Score:{score}',True,white)
    text_rect = text.get_rect()
    text_rect.center=(50,40)
    screen.blit(text,text_rect)
    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        font= pygame.font.Font(pygame.font.get_default_font(),16)
        text=font.render(f'Game Over! Play Again? (Y / N)',True,white)
        text_rect = text.get_rect()
        text_rect.center=(width/2,100)
        screen.blit(text,text_rect)
    pygame.display.update()
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
         
            if event.type==QUIT:
               gameover= False
               running = False


            if event.type==KEYDOWN:
                if event.key == K_y:
                  #reset game
                  gameover=False
                  score=0
                  speed=2
                  Vehicle_group.empty()
                  player.rect.center = [player_x,player_y]
                
                elif event.key == K_n:
                    #exit game
                    gameover=False
                    running=False
pygame.quit()
