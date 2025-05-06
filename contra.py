import pygame
from threading import Timer
pygame.init()

width = 1300
height = 800

screen = pygame.display.set_mode ((width,height))
pygame.display.set_caption('Contra')
clock = pygame.time.Clock()
FPS = 60
BG = (144, 201, 120)
def draw_bg():
    screen.fill(BG)
   
move_left = False
move_right = False

def timer(self , update_animation):
    self.index += 1
    t1 = Timer(1,update_animation)
    t1.start()





class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale1, speed):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\enemy.png')
        
        self.img1 = pygame.transform.scale(img, (img.get_width()* scale1, img.get_height()* scale1))
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.img2 = pygame.image.load('C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\enemy.png')
        


        self.hitbox = self.img2.get_rect()
        self.hitbox.center = (x , y)
    
    def move(self,move_left, move_right):
        dx = 0
        dy = 0


        if move_left: 
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1


        
        
        self.hitbox.x += dx
        self.hitbox.y += dy    


   
       

    def draw(self):
        screen.blit(pygame.transform.flip(self.img2, self.flip , False),self.hitbox)
        



class Guy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.animation = []
        idle = []
        run = []
        self.index = 0
        self.action = 0
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        
        self.indexrun = 0
        for i in range(5):
         img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\soldier\\idle{i}.png')
         img = pygame.transform.scale(img, (img.get_width()* scale, img.get_height()* scale))
         idle.append(img)
        
        
        self.animation.append(idle)
        
        
        for i in range(1,7):
         img = pygame.image.load(f'C:\\Users\\Akhil\\OneDrive\\Desktop\\Contra Files\\soldier\\run{i}.png')
         img = pygame.transform.scale(img, (img.get_width()* scale, img.get_height()* scale))
         run.append(img)

      


        self.animation.append(run) 
        self.img = self.animation[self.action][1]
        

        self.hitbox = self.img.get_rect()
        self.hitbox.center = (x , y)

   

   
    def move(self,move_left, move_right):
        dx = 0
        dy = 0


        if move_left: 
            dx = -self.speed
            self.flip = True
            self.direction = -1
        
           
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            


        self.hitbox.x += dx
        self.hitbox.y += dy    



    def update(self):
         time = 100
         
         self.index += 0.5
        
             
         self.img = self.animation[int(self.action)]
         
         if self.index >= len(self.animation[self.action]):
             self.index = 0


    def update_action(self,new):
        if new != self.index:
            
            
            
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip , False),self.hitbox)
        


player = Guy(300, 500, 2.5, 5)







nigga = True
while nigga:
    draw_bg()

    player.update()


    player.draw()

    
    

    if move_left or move_right:
        player.update_action(1)
    else:
        player.update_action(0)
    player.move(move_left,move_right)
    
    clock.tick(FPS)

    bad_guy = Enemy(500,500,2.5,5)

    bad_guy.draw()

    

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            nigga = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:

               
                move_left = True    
            if event.key == pygame.K_d:
                move_right = True   
 #
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False 
            if event.key == pygame.K_d:
                move_right = False  



pygame.quit()            
bullet = Bullet(self.rect.centerx + (self.rect.size[0]* 0.75* self.direction ), self.rect.centery, self.direction)

dx = self.speed * self.direction