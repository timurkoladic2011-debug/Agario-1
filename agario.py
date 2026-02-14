# Імпортуємо бібліотеку для створення ігор
import pygame  # Імпорт Pygame для графіки

# Імпортуємо функцію для генерації випадкових чисел
from random import randint  # Генерація випадкових чисел

# Імпортуємо всі класи та функції з файлу my_class.py
from my_class import*  # Класи Player, Food

'''1. Імпортуємо модулі для мережі і потоків'''
from socket import socket, AF_INET,SOCK_STREAM  # socket для роботи з сервером
from threading import Thread # Thread для паралельного отримання даних
from launcher import Launcher
''''''''''''
menu = Launcher()
menu.window_start()
pygame.init()
nickname = menu.nick
ip = menu.ip
port = menu.port

# Задаємо ширину і висоту вікна гри
WIDTH, HEIGHT = 500, 500

# Описуємо кольори у форматі RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (200, 0,0)

# Створюємо вікно гри з заданими розмірами
window = pygame.display.set_mode((WIDTH,HEIGHT))
# Створюємо об'єкт для контролю частоти кадрів (FPS)
clock = pygame.time.Clock()

# Змінна для збереження зображення фону (поки що порожня)
fon = pygame.image.load("fon.png")
fon = pygame.transform.scale(fon,(WIDTH,HEIGHT))

# Гравець
player = Player(x=WIDTH//2,y=HEIGHT//2,radius=20,
                speed=5,color=((randint(0,255)),randint(0,255),randint(0,255)),nickname=nickname)

# Їжа
foods = [Food() for i in range(300)]

# Змінна для керування роботою гри
run = True

fon_x,fon_y = 0,0

'''2. Початкові координати "світу"(цент екрану) та словник інших гравців(порожній), змінна для буфера'''
word_x, word_y = 0,0
other_player = {}  #id:{x:x, y:y, r:r, c:c}
buffer = ""


'''3. Налаштовуємо сокет клієнта'''
''''''
client = socket(AF_INET,SOCK_STREAM ) # створити сокет
client.connect(("6.tcp.eu.ngrok.io",13371))#зв'язатись із сервером
''''''

'''3.Функція для оновлення даних інших гравців для потоку, постійного оновлення '''
def update_players():
    # доступ до змінної буфера
    global buffer
    # цикл завжди для прийому даних від серевра
    while True:
        #спробувати прийняти дані від сервера
        try:
            #принімаємо дані від сервера, декодуємо
            data = client.recv(4096).decode()
            #якщо дані порожін - пропустити
            if not data:
                continue
    
            #додаємо дані до буфера
            #така сама схема роботи з буфером як і у сервера
            buffer += data
            # поки символ кінця рядка є у буфері
            while "\n" in buffer:
                #розбити буфер на два значення по символу кінця рядка
                line, buffer = buffer.split("\n",1)
                #якщо повідомлення порожнє - пропустити
                if not line:
                    continue
                    
                # розбити на частини повідомлення в одну зміну-список!
                # щоб впевнитись що все є і нічого зайвого немає    
                parts = line.split("|") 
                '''перевірити якщо там два значення та друге значення exit
                то це повідомлення про відключення клієнта,
                де перше значення - це айді клієнта, а друге значення - це слово exit
                якщо це так, то видалити цього клієнта зі словника інших гравців та пропустити далі'''
                #if
                #перевірити чи все є - потрібно 7 значень
                #айді, ч, у, радійс, колір - 3 значення
                if len(parts)!= 8:
                    continue 
                # розпкаовуємо список в окремі змінін
                ids,x,y,radius,R,G,B,nickname = parts
                # перетворити окремі значення кольору в кортеж
                color =(int(R),int(G),int(B))
                #онвоити дані в словнику інших гравців
                other_player [ids] = {
                    "x":int(x),
                    "y":int(y),
                    "r":int(radius),
                    "color":color,
                    "nick": nickname
                }

        except:
            pass
#запустити потік на прйимо даних
Thread(target=update_players,daemon=True).start()

''''''  

font = pygame.font.Font(None, 16)
# Головний цикл гри
while run:

    # Зафарбовуємо екран чорним кольором
    window.fill(BLACK)

    player.move()
    '''4. формуємо та відправляємо власні дані на сервер'''
    #оновити свої координати у світі(всі змішення без центрування відносоно камери)
    word_x += player.move_x
    word_y += player.move_y
    # формуємо рядко з моїми даними
    #!незабудь по симовл кінця рядка - \n
    R,G,B = player.color
    my_data = f"{word_x}|{word_y}|{player.radius}|{R}|{G}|{B}|{nickname}\n"  # формує рядок з моїми даними - регеструємось в грі, незабудь про символ кінця рядка!

    # спробуємо відправити серверу наші дані
    try:
        client.send(my_data.encode()) #відправити усе
    except (BlockingIOError, BrokenPipeError):
        pass
    ''''''

    # Малюємо фон у верхньому лівому куті
    window.blit(fon,(fon_x,fon_y))
    window.blit(fon,(fon_x-WIDTH,fon_y))
    window.blit(fon,(fon_x,fon_y-HEIGHT))
    window.blit(fon,(fon_x-WIDTH,fon_y-HEIGHT))
    player.draw(window)

    # Оновлюємо координати фону для ефекту руху
    fon_x -=player.move_x
    fon_y -=player.move_y
    fon_x %=WIDTH
    fon_y %=HEIGHT 

    
    '''5. Відобрадаємо усіх інших граців та перевірка зіткнення з ними'''
    # перебираємо словник іншиг гравці по ключу та значенню
    #де ключ - це айді, значення - усі його дані
    for ids,player_data in other_player.items():
        # розраховуємо координати гравця 
        # відносно камери + половина камери
        # відносно нас -наші координати в світі
        x = player_data["x"] + WIDTH//2 - word_x
        y = player_data["y"]  + HEIGHT//2 - word_y
        #малюємо коло за координатами, радіус та колір зі словникі

        pygame.draw.circle(window,player_data["color"],(x,y),player_data["r"])
        name = font.render(player_data["nick"],True,(0,0,0))
        window.blit(name,(x,y-player_data["r"]-8))
        rect = pygame.Rect(x - player_data["r"],y - player_data["r"],
                           player_data["r"] * 2 ,player_data["r"] * 2)
        if player.rect.colliderect(rect):
            '''порівняти радіуси гравців, 
            якщо наш радіус більший - збільшити свій радіус на радіус іншого гравця(викликати метод зміни розміру гравця)
            інакше - програти, тобто закрити клієнта та вийти з гри'''
            pass
        # викликати метод гравця для перевірки зіткнення з іншим гравцем
        #передати координати та радіус іншого гравця
        # отримаємо виграв/програв
        #якщо інший гравець програв - видалити відправити повідомення на серевр

    ''''''
    #  Промальовка їжі, оновлення координат та перевірка з’їдання

    for food in foods:
        food.draw(window)
        food.update(player)
        if food.eat_me(player):
            foods.remove(food)

    # Перебираємо всі події (натискання клавіш, закриття вікна тощо)
    for event in pygame.event.get():
        # Перевіряємо, чи користувач закрив вікно
        if event.type == pygame.QUIT:
            run = False

    # Оновлюємо зображення на екрані
    pygame.display.flip()

    # Обмежуємо швидкість гри до 60 кадрів на секунду
    clock.tick(60)
