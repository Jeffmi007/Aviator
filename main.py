from pygame import * 
from random import randint
from datetime import datetime, timedelta

back = (255, 255, 255) 
win_width = 1000 
win_height = 700

lohotron = randint(-10, 40)
lobotron_y_speed = 1
lobotron_y_side = 'down'

start_money = True 
start_rate = False
fly_plane = False 
end_game = False

font.init() 
text = font.SysFont('Arial', 50) 
background = transform.scale( 
    image.load("sky.jpg"),  
    (win_width, win_height) 
) 
background2 = transform.scale( 
    image.load("back.jpg"),  
    (1010, 500) 
) 
 
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y))     
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y  
  
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
class MoneySetter(): 
    def __init__(self, player_x, player_y): 
        self.player_x = player_x 
        self.player_y = player_x 
        self.money = 0 
     
    def update_sum(self): 
        keys = key.get_pressed() 
        if keys[K_UP] and start_money == True: 
            self.money += 100 
        if keys[K_DOWN] and start_money == True: 
            if self.money >= 100: 
                self.money -= 100 
         
        text1 = text.render(f"Баланс: {int(self.money)} $", 1, (222, 170, 10)) 
        window.blit(text1, (10, 450)) 
class RateSetter(): 
    def __init__(self, player_x, player_y): 
        self.player_x = player_x 
        self.player_y = player_x 
        self.rate = 0 
     
    def update_sum(self): 
        keys = key.get_pressed() 
        if keys[K_UP] and start_rate == True: 
            self.rate += 100 
            if self.rate > moneys.money: 
                self.rate = moneys.money 
        if keys[K_DOWN] and start_rate == True: 
            if self.rate >= 100: 
                self.rate -= 100 
        text1 = text.render(f"Ставка: {self.rate} $", 1, (222, 170, 10)) 
        window.blit(text1, (370, 450)) 
 
window = display.set_mode((win_width, win_height)) 
window.fill(back) 
  
run = True 
finish = False 
clock = time.Clock() 
FPS = 60 
 
moneys = MoneySetter(200, 200) 
rate = RateSetter(200, 200) 
plane = GameSprite('airplane.png', 0, 380, 250, 80, 50, ) 
 
speed_x = 3 
speed_y = 3 
plane_fly_start = None
plane_fly_end = None
one_second_timer = None
time_since_start = 0
game_delay = None
shaking = False
probable_gain = None
is_pressed = False
winned_money = 0

while run: 
    window.blit(background, (0, 0)) 
    window.blit(background2, (0, 450)) 
 
    plane.update() 
    plane.reset() 
 
    moneys.update_sum() 
    rate.update_sum() 
 
    for e in event.get(): 
        if e.type == QUIT: 
           run = False 
 
    keys = key.get_pressed() 

    if keys[K_SPACE] and plane.rect.y == 380:
        if moneys.money > 0: 
            start_money = False 
            start_rate = True 
            probable_gain = rate.rate
        if rate.rate > 0: 
            start_rate = False

    if keys[K_RETURN] and game_delay == None:
        game_delay = randint(1, 30)
        print(game_delay)
        plane_fly_start = datetime.now()
        one_second_timer = datetime.now() + timedelta(seconds = 1)
        plane_fly_end = plane_fly_start + timedelta(seconds = game_delay)
        fly_plane = True

    if keys[K_TAB] and end_game == False:
        is_pressed = True
        winned_money = probable_gain
    
    if probable_gain:
        if one_second_timer and one_second_timer <= datetime.now() and end_game == False:
            probable_gain *= 1.3 
            one_second_timer = datetime.now() + timedelta(seconds = 1)
            
        text3 = text.render(f"Імовірний виграш: {int(probable_gain)} $", 1, (222, 170, 10)) 
        window.blit(text3, (170,550))

    if plane_fly_end and plane_fly_end < datetime.now() and end_game == False:
        end_game = True
        fly_plane = True
        shaking = False
        if is_pressed == True:
            moneys.money += winned_money
        else:
            probable_gain = 0

    
    if fly_plane == True and start_rate == False and start_money == False:
        plane_speed_x = randint(2, 8)
        plane_speed_y = randint(1, 4)
        plane.rect.x += plane_speed_x
        plane.rect.y -= plane_speed_y

        rand_speed = randint(1, 5)
        if rand_speed == 1:
            speed_x, speed_y = 3, 3
        elif rand_speed == 2:
            speed_x, speed_y = 5, 5
        elif rand_speed == 3:
            speed_x, speed_y = 7, 7
        elif rand_speed == 4:
            speed_x, speed_y = 9, 9
        elif rand_speed == 5:
            speed_x, speed_y = 11, 11
        if plane.rect.x >= 600 and end_game == False:
            fly_plane = False
            shaking = True


    if shaking == True:
        if plane.rect.x >= 600:
            lobotron_y_speed += 0.25

        if lobotron_y_side == 'down':
            plane.rect.y += lobotron_y_speed
        else:
            plane.rect.y -= lobotron_y_speed   
        if lobotron_y_speed >= 3:
            lobotron_y_speed = 1
            if lobotron_y_side == "down":
                lobotron_y_side = "up"
            else:
                lobotron_y_side = "down"
    

    display.update() 
    clock.tick(FPS)