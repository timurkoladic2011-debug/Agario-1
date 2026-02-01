import pygame
from random import randint
class Sprite:
    def __init__(self,x=10,y=10,w=50,h=50,speed=0,image=None,color=(200,0,0)):
            self.image = image
            self.color = color
            self.rect = pygame.Rect(x,y,w,h)
            self.speed = speed
            self.load_img()
    def draw(self,window):
         if self.image:
              window.blit(self.image,self.rect)
         else:
              pygame.draw.rect(window,self.color,self.rect)
    def move(self,window):
         key = pygame.key.get_pressed()
         if key[pygame.K_w] and self.rect.y >= self.speed:
              self.rect.y -= self.speed
         if key[pygame.K_s] and self.rect.bottom <= window.get_height() - self.speed:
              self.rect.y += self.speed
         if key[pygame.K_a] and self.rect.x >= self.speed:
              self.rect.x -= self.speed
         if key[pygame.K_d] and self.rect.right <= window.get_wigth() - self.speed:
              self.rect.x += self.speed
    def load_img(self):
         if self.image:
              self.image = pygame.image.load(self.image)
              self.image = pygame.transform.scale(self.image,(self.rect.w, self.rect.h))

class Circle(Sprite):
    def __init__(self, x = 100, y = 100, radius= 50, 
                 speed = 0, color = (0,0,130)):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.speed = speed
        self.color = color

    def draw(self, surface):
        #pygame.draw.rect(surface, (0,0,0), self.rect, width=5)
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)

class Player(Circle):
      def __init__(self, x=100, y=100, radius=50, speed=0, color=(0, 0, 130)):
           super().__init__(x, y, radius, speed, color)
           self.move_x = 0
           self.move_y = 0
      def move(self):
           self.move_x = 0
           self.move_y = 0
           key = pygame.key.get_pressed()
           if key[pygame.K_w]:
                self.move_y = -self.speed
           if key[pygame.K_s]:
                self.move_y = self.speed
           if key[pygame.K_a]:
                self.move_x = -self.speed
           if key[pygame.K_d]:
                self.move_x = self.speed     

class Food(Circle):
     def __init__(self):
          x = randint(-5000,500)
          y = randint(-5000,500)
          radius = randint(2,5)
          speed = 0
          color = (randint(0,255),randint(0,255),randint(0,255))
          super().__init__(x, y, radius, speed, color)
     def update(self,player):
          self.rect.x -= player.move_x
          self.rect.y -= player.move_y
         # self.rect.x %= 500
         # self.rect.y %= 500
     def eat_me(self,player):
         if self.rect.colliderect(player.rect):
              x,y = player.rect.center
              player.radius += self.radius
              player.rect.w = player.radius*2
              player.rect.h = player.radius*2
              player.rect.center = (x,y)
              return True
         else:
              return False
              
