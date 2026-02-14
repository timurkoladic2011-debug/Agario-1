# Імпортуємо бібліотеку для створення ігор
import pygame

# Імпортуємо функцію для генерації випадкових чисел
from random import randint

# Імпортуємо всі класи та функції з файлу my_class.py
from my_class import *

# Ініціалізуємо всі модулі Pygame
pygame.init()

# Задаємо ширину і висоту вікна гри
WIDTH, HEIGHT = 500, 500

# Описуємо коліри у форматі RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)


# Створюємо вікно гри з заданими розмірами
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Створюємо об'єкт для контролю частоти кадрів (FPS)
clock = pygame.time.Clock()

# Змінна для збереження зображення фону (поки що порожня)
fon = pygame.image.load("fon.png")
fon = pygame.transform.scale(fon, (WIDTH, HEIGHT))
#Гравець - eat
player = Player(x=WIDTH//2,radius=20,speed=5,color=GREEN)

foods = [Food()for i in range(300)]


# Змінна для керування роботою гри
run = True

fon_x,fon_y = 0,0 




# Головний цикл гри, працює поки run == True
while run:


    # Зафарбовуємо екран чорним кольором
    window.fill(BLACK)


    # Малюємо фон у верхньому лівому куті (помилка, якщо fon == None)
    window.blit(fon,(fon_x,fon_y)) 
    window.blit(fon,(fon_x-WIDTH,fon_y)) 
    window.blit(fon,(fon_x,fon_y-HEIGHT)) 
    window.blit(fon,(fon_x-WIDTH,fon_y-HEIGHT))
    player.draw(window)
    player.move()

    fon_x += player.move_x
    fon_y += player.move_y
    fon_x %=WIDTH
    fon_y %=HEIGHT

#cerepawka == eat 

    for food in foods:
        food.draw(window)
        food.update(player)
        if food.eat_me(player):
             foods.remove(food)


    # Перебираємо всі події (натискання клавіш, закриття вікна тощо)
    for event in pygame.event.get():
        

        # Перевіряємо, чи користувач закрив вікно
        if event.type == pygame.QUIT:

                # Зупиняємо гру
                run = False

    # Оновлюємо зображення на екрані
    pygame.display.flip()

    # Обмежуємо швидкість гри до 60 кадрів на секунду
    clock.tick(60)