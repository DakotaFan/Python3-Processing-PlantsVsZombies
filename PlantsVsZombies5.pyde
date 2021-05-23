
#Group Members: Ricardo, Dakota
#Ricardo: Zombie Super and subclasses, Game logic, Check end of game condition, animation
#Dakota: Game class, Plants super and subclasses, animation and sound effect, mouse handling, restart and check win/lose
add_library('minim')
import os
import random
import time

path = os.getcwd()
player = Minim(this)

#upper left corner of the yard coordinate(252,85), lower right corner (981, 85),
#lower left corner of the yard coordinate(252,575), upper right corner (981, 575)
Coordinates = { "UpperLeft": [252,85], "UpperRight": [981, 85], "LowerLeft" : [252,575], "LowerRight" : [981, 575], 'Road': [1100, 575]}
NUM_ROWS = 5
NUM_COLS = 9
CELL_WIDTH = 81
CELL_HEIGHT = 98
Cards_list = ["SunFlowerG.png", "WallNutG.png", "PeashooterG.png", "CherryBombG.png","SnowPeaG.png"] #/images/Cards/
Plants_list = ["Sunflower.png", "Wallnut.png", "Peashooter1.png", "Cherrybomb.png", "Snowpeashooter.png", "Shovel.png"] #images/Plants/
Plants_value = { "Sunflower": 50, "Wallnut" : 50, "Peashooter": 100, "Cherrybomb": 150, "Snowpeashooter" : 150}
Plants_name = ["Sunflower", "Wallnut", "Peashooter", "Cherrybomb", "Snowpeashooter"]
Plants_Dim = [(73,74), (65, 73), (71,71), (112,81), (71,71), (71,77)] #dimension of different plants in the /images/Plants/ Folder
NUM_SLICES_PLANT = [18, 14, 13, 7, 15]  #Number of slices in each of the sprites in the order of Sunflower, wallnut, peashooter, cherryBomb, snowPea

Zombies_name = ['NormalZombies', 'ConeHeadZombies', 'NewspaperZombies', 'FlagZombies']

Zombies_walk_list = []
Zombies_attack_list = []
Zombies_heads_list = []
Zombies_noheadswalk_list = []
Zombies_noheadsattack_list = []
Zombies_die_list = []
Zombies_boom_list = []

for i in range(4):
    Zombies_walk_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'Walk.png')
    Zombies_attack_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'Bite.png')
    Zombies_heads_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'Heads.png')
    Zombies_noheadswalk_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'NoHeadsWalk.png')
    Zombies_noheadsattack_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'NoHeadsBite.png')
    Zombies_die_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'Die.png')
    Zombies_boom_list.append('/Zombies/' + Zombies_name[i] + '/' + Zombies_name[i] + 'Boom.png')
    
Zombies_attack_value = {'NormalZombies': 100, 'ConeHeadZombies': 100, 'NewspaperZombies': 100, 'FlagZombies': 100}
Zombies_health_value = {'NormalZombies': 270, 'ConeHeadZombies': 640, 'NewspaperZombies': 420, 'FlagZombies': 200}  

ZOMBIES_DIM = [166, 144]
NUM_SLICES_ZOMBIES_WALK = [22, 21, 19, 11]
NUM_SLICES_ZOMBIES_ATTACK = [21, 11, 8, 11]
NUM_SLICES_ZOMBIES_HEADS = [12, 12, 10, 12]
NUM_SLICES_ZOMBIES_NOHEADSWALK = [18, 18, 16, 12]
NUM_SLICES_ZOMBIES_NOHEADSATTACK = [11, 11, 7, 11]
NUM_SLICES_ZOMBIES_DIE = [10, 10, 11, 10]
NUM_SLICES_ZOMBIES_BOOM = [20, 20, 20, 20]

board = []
for row in range(NUM_ROWS):
    row_list = []
    for column in range(NUM_COLS):
        row_list.append(0)
    board.append(row_list)

class Stage():
    
    '''Create a beginning scene for the game, 
    once clicked, enter the real game'''
    
    def __init__(self, img, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/Background/" + img)
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)

     
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        # return "(" + str(self.x) + "," + str(self.y) + ")"  # (x,y)
        return "({0},{1})".format(self.x, self.y)

    def distance(self, other):   #in the future could be utilized to check collision
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
#plant Card need a cooling down time

class Sun:
    def __init__(self, p, w, h, num_slices, img):
        self.p = p     #add center point attribute to the Plant class
        self.w = w
        self.h = h
        self.num_slices = num_slices
        self.slice = 0
        self.img = loadImage(path + "/images/Plants/" + img)
        self.music = player.loadFile(path + "/sound/Sun.mp3")
        self.value = 25
        self.clicked = False
        self.vx = 0
        self.vy = 0
        self.collected = False
        
    def update(self):
        self.p.x = self.p.x - self.vx
        self.p.y = self.p.y - self.vy
        
        if self.slice <= self.num_slices:
            if frameCount%30 == 0:
                self.slice = self.slice + 1
        else:
            self.slice = self.slice
            
            
        if self.clicked == True:
            if self.p.x <= game.sun.x and self.p.y <= game.sun.y:
                self.collected = True
    

    
            
    def click(self):
        self.clicked = True
        self.music.play()
        game.score = game.score + 25
        self.vx = (self.p.x - game.sun.x)//2
        self.vy = (self.p.y - game.sun.y)//2
    
        
            
    def display(self):
        self.update()
        if self.collected == False:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
            
class FallingSun(Sun):
    def __init__(self, p, w, h, num_slices, img):
        Sun.__init__(self, p, w, h, num_slices, img)
        self.vy = -0.25
        self.vx = 0
        self.clicked = False
        self.timer = time.time()
    
    def update(self):
        self.p.y = self.p.y - self.vy
        self.p.x = self.p.x - self.vx
        
        if frameCount%60 == 0:
            self.slice = self.slice + 1
            
        if self.clicked == True:
            if self.p.x <= game.sun.x and self.p.y <= game.sun.y:
                self.collected = True
    
class Zombies():
    def __init__(self, row, img, num_slices, time):
        self.x = random.randint(1100, 1300)
        self.row = row
        self.y = Coordinates['UpperLeft'][1] + (self.row + 1) * CELL_HEIGHT - 0.5 * ZOMBIES_DIM[1]
        self.v = 0 
        self.health = 0
        self.attack = 0
        self.img = loadImage(path + "/images/" + img)
        self.img_w = ZOMBIES_DIM[0]
        self.img_h = ZOMBIES_DIM[1]
        self.num_slices = num_slices
        self.slice = random.randint(0, num_slices)
        self.groan = player.loadFile(path + "/sound/Groan.mp3")
        self.groan2= player.loadFile(path + "/sound/Groan4.mp3")
        self.hit_sound = player.loadFile(path + "/sound/Splat.mp3")
        self.eat_sound = player.loadFile(path + "/sound/ZombieBite.mp3")
        self.condition = 'Walk'
        self.delete = False
        self.type = 0
        self.framerate = 10 
        self.time = time
                                       
    def update(self):

        self.x = self.x + self.v
    
        if frameCount % self.framerate == 0:
            self.slice += 1
            
        if self.condition == 'Attack' or self.condition =='NoHeadsBite' and self.determine_position() != False:
            for plant in game.plants:
                if self.determine_position()[0] == plant.column and self.determine_position()[1] == plant.row:
                    plant.healthscore = plant.healthscore - self.attack / 60
                    # print(plant.healthscore)
        
        if not self.reach_plants() and self.health <= 80:
            if self.condition == 'Walk':
                game.heads.append(Heads(self.row, Zombies_heads_list[self.type], NUM_SLICES_ZOMBIES_HEADS[self.type], self.x + self.img_w // 2, self.y))
                self.img = loadImage(path + '/images/' + Zombies_noheadswalk_list[self.type])
                self.slice = 0
                self.num_slices = NUM_SLICES_ZOMBIES_NOHEADSWALK[self.type]
                self.condition = 'NoHeadsWalk'
                
            elif self.condition == 'NoHeadsBite':
                self.slice = 0
                self.img = loadImage(path + '/images/' + Zombies_noheadswalk_list[self.type])
                self.start()
                self.eat_sound.pause()
                self.num_slices = NUM_SLICES_ZOMBIES_NOHEADSWALK[self.type]
                self.condition = 'NoHeadsWalk'

        elif not self.reach_plants() and self.health > 80:
            if self.condition == 'Attack':
                self.slice = 0
                self.img = loadImage(path + '/images/' + Zombies_walk_list[self.type])
                self.start()
                self.eat_sound.pause()
                self.num_slices = NUM_SLICES_ZOMBIES_WALK[self.type]
                self.condition = 'Walk'
    
        if self.reach_plants() and self.health > 80:
            if self.condition == 'Walk':
                self.v = 0
                self.eat_sound.loop()
                self.img = loadImage(path + '/images/' + Zombies_attack_list[self.type])
                self.slice = 0
                self.num_slices = NUM_SLICES_ZOMBIES_ATTACK[self.type]
                self.condition = 'Attack'
        elif self.reach_plants() and self.health <= 80:
            if self.condition == 'Attack':
                game.heads.append(Heads(self.row, Zombies_heads_list[self.type], NUM_SLICES_ZOMBIES_HEADS[self.type], self.x + self.img_w // 2, self.y))
                self.slice = 0
                self.img = loadImage(path + '/images/' + Zombies_noheadsattack_list[self.type])
                self.num_slices = NUM_SLICES_ZOMBIES_NOHEADSATTACK[self.type]
                self.v = 0
                self.eat_sound.rewind()
                self.eat_sound.loop()
                self.condition = 'NoHeadsBite'
            
        if self.condition == 'NoHeadsWalk' and self.reach_plants():
            self.slice = 0
            self.img = loadImage(path + '/images/' + Zombies_noheadsattack_list[self.type])
            self.num_slices = NUM_SLICES_ZOMBIES_NOHEADSATTACK[self.type]
            self.v = 0
            self.eat_sound.rewind()
            self.eat_sound.loop()
            self.condition = 'NoHeadsBite'
            
        if self.condition != 'Die' and self.health <= 0:
            self.img = loadImage(path + '/images/' + Zombies_die_list[self.type])
            self.slice = 0
            self.framerate = 10
            self.num_slices = NUM_SLICES_ZOMBIES_DIE[self.type]
            self.hit_sound.pause()
            self.eat_sound.pause()
            self.condition = 'Die'
                
        if self.condition == 'Die' and self.slice == self.num_slices:
            self.delete = True
            
        self.slice = self.slice % self.num_slices
        
        # print(self.condition)
            
    
    def determine_position(self):
        if Coordinates['UpperLeft'][0] < self.x < Coordinates['UpperRight'][0]:
            return [int((self.x - Coordinates['UpperLeft'][0]) // CELL_WIDTH), self.row]
        return False
    
    def check_first_zombie(self, plant):
        if plant.row == self.row:
            row_list=[]
            for zombies in game.zombies:
                if zombies.determine_position() != False and zombies.row == self.row and zombies.determine_position()[0] >= plant.column:
                    row_list.append(zombies.x)
            if self.x in row_list and self.x == min(row_list):
                return True
            return False
        return False
        
    def reach_plants(self):
        if Coordinates['UpperLeft'][0] < self.x < Coordinates['UpperRight'][0] and \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)] != 0 and \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].p.x + \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].w // 2 > \
        self.x > \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].p.x - \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].w // 2:
            return True
        return False
    
    def start(self):
        if self.time + 0.1 >= game.time >= self.time - 0.1:
            self.v = 0
        
    def check_boom_die(self):
        if self.condition == 'BoomDie':
            self.slice = 0
            self.eat_sound.pause()
            self.hit_sound.pause()
            self.num_slices = NUM_SLICES_ZOMBIES_BOOM[self.type]
            self.img = loadImage(path + '/images/' + Zombies_boom_list[self.type])
            self.framerate = 10
            self.v = 0
            self.condition = 'BoomDead'
        if self.condition == 'BoomDead' and self.slice == self.num_slices - 1:
            self.delete = True
        
    def display(self):
        self.start()
        self.update()
        self.check_boom_die()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        

class NormalZombies(Zombies):
    
    def __init__(self, row, img, num_slices, time):
        Zombies.__init__(self, row, img, num_slices, time)
        self.type = 0
        self.attack = Zombies_attack_value[Zombies_name[self.type]]
        self.health = Zombies_health_value[Zombies_name[self.type]]
        
    
    def start(self):
        if self.time + 0.1 >= game.time >= self.time - 0.1:
            self.v = - 0.15

class FlagZombies(Zombies):
    def __init__(self, row, img, num_slices, time):
        Zombies.__init__(self, row, img, num_slices, time)
        self.type = 3
        self.attack = Zombies_attack_value[Zombies_name[self.type]]
        self.health = Zombies_health_value[Zombies_name[self.type]]
        
    
    def start(self):
        if self.time + 0.1 >= game.time >= self.time - 0.1:
            self.groan.play()
            self.v = - 0.2
        
class NewspaperZombies(Zombies):
    def __init__(self, row, img, num_slices,time):
        Zombies.__init__(self, row, img, num_slices, time)
        self.type = 2
        self.attack = Zombies_attack_value[Zombies_name[self.type]]
        self.health = Zombies_health_value[Zombies_name[self.type]]
        self.lost_newspaper = False
        
    def start(self):
        if not self.lost_newspaper and self.time + 0.1 >= game.time >= self.time - 0.1:
            self.v = - 0.15
        elif self.lost_newspaper:
            self.v = - 0.3
        
        
    def check_angry(self):
        if not self.lost_newspaper and 80 < self.health <= 270:
            self.v = 0
            self.groan2.play()
            self.img = loadImage(path + '/images/Zombies/' + Zombies_name[self.type] + '/' + Zombies_name[self.type] + 'LostNewspaper.png')
            self.slice = 0
            self.num_slices = 11
            self.lost_newspaper = True
            self.attack = self.attack * 5
            self.framerate = 5
            self.condition = 'Lost Newspaper'

        
        if self.lost_newspaper and self.health > 80:
            if self.condition == 'Lost Newspaper' and self.slice == self.num_slices - 1 and not self.reach_plants():
                self.slice = 0
                self.v = - 0.3
                self.num_slices = 14
                self.img = loadImage(path + '/images/' + Zombies_walk_list[self.type][:-4] + '_angry.png')
                self.condition = 'Walk'
            elif self.condition == 'Lost Newspaper' and self.slice == self.num_slices - 1 and self.reach_plants():
                self.slice = 0
                self.num_slices = 7
                self.img = loadImage(path + '/images/' + Zombies_attack_list[self.type][:-4] + '_angry.png')
                self.condition = 'Attack'
            elif self.condition == 'Walk':
                self.v = - 0.3
                self.num_slices = 14
                self.img = loadImage(path + '/images/' + Zombies_walk_list[self.type][:-4] + '_angry.png')
            elif self.condition == 'Attack':
                self.num_slices = 7
                self.img = loadImage(path + '/images/' + Zombies_attack_list[self.type][:-4] + '_angry.png')
                 
    def reach_plants(self):
        if Coordinates['UpperLeft'][0] < self.x < Coordinates['UpperRight'][0] and \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)] != 0 and \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].p.x + \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].w // 2 > \
        self.x - self.img_w // 2 > \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].p.x - \
        board[self.row][int((self.x - Coordinates["UpperLeft"][0])//CELL_WIDTH)].w // 2:
            return True
        return False
                
    def display(self):
        self.start()
        self.update()
        self.check_angry()
        self.check_boom_die()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)


class ConeHeadZombies(Zombies):
    def __init__(self, row, img, num_slices, time):
        Zombies.__init__(self, row, img, num_slices, time)
        self.type = 1
        self.attack = Zombies_attack_value[Zombies_name[self.type]]
        self.health = Zombies_health_value[Zombies_name[self.type]]
    
    def start(self):
        if self.time + 0.1 >= game.time >= self.time - 0.1:
            self.v = - 0.15
        
    def check_hat(self):
        if self.health <= 270:
            self.delete = True
            self.eat_sound.pause()
            self.hit_sound.pause()
            game.zombies.append(ConeHeadZombiesNoHat(self.row, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], self.x, game.time))
                    
    def display(self):
        self.start()
        self.check_hat()
        self.update()
        self.check_boom_die()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)


class ConeHeadZombiesNoHat(NormalZombies):
    def __init__(self, row, img, num_slices, x, time):
        NormalZombies.__init__(self, row, img, num_slices, time)
        self.x = x

class Heads(Zombies):
    def __init__(self, row, img, num_slices, x, y):
        Zombies.__init__(self, row, img, num_slices, time)
        self.x = x
        self.y = y
        self.slice = 0
        self.delete = False
        self.framerate = 5
        self.time = game.time
        
    def update(self):
        if frameCount % self.framerate == 0:
            self.slice += 1
        if self.slice == self.num_slices:
            self.delete = True


class Plant:

    def __init__(self, p, w, h, num_slices, img):   #p is the point, and point has attribute x
        self.p = p     #add center point attribute to the Plant class
        self.w = w
        self.h = h
        self.num_slices = num_slices
        self.slice = 0
        self.img = loadImage(path + "/images/Plants/" + img)
        self.row = 0
        self.column = 0
        self.fixed = False    #when the mouse click the card, but the plant has not been placed in the yard yet.
        #when self.fixed = False, the plant will automatically move with the mouse until next valid click
        
    def update(self, dx, dy):
        if self.fixed == False:
            self.p.x = dx
            self.p.y = dy
        elif self.fixed == True:
            self.p.x = self.p.x
            self.p.y = self.p.y
            self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
            self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
            
            if frameCount%10 == 0:
                self.slice = (self.slice + 1) % self.num_slices      
              
    def display(self):
        image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        
    
class Sunflower(Plant):
    
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.healthscore = 300
        self.value = 50
        self.fixed = False
        self.type = "Sunflower"
        self.suns = []
        self.start = frameCount
        
    def update(self, dx, dy):
        if self.fixed == False:
            self.p.x = dx
            self.p.y = dy
        elif self.fixed == True:
            self.p.x = self.p.x
            self.p.y = self.p.y
            self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
            self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT

            if frameCount % 10 == 0:
                self.slice = (self.slice + 1) % self.num_slices
                
            if len(self.suns)< 1:
                if (frameCount - self.start)% 600 == 0:
                    self.sun = Sun(Point(self.p.x - 20, self.p.y - 20), 78, 78, 22, "SunSpawn1.png" )
                    self.suns.append(self.sun)
            elif len(self.suns) >= 1:
                if (frameCount - (self.start + 1 * 600))% 1800 == 0:
                    self.sun = Sun(Point(self.p.x - 20, self.p.y - 20), 78, 78, 22, "SunSpawn1.png" )
                    self.suns.append(self.sun)
            
    def __str__(self):
        return "Sunflower"
    
    def display(self):
        if self.healthscore > 0:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        else:
            game.plants.remove(self)
            board[self.row][self.column] = 0
        
        if len(self.suns) != 0:
            for sun in self.suns:
                sun.display()
    

class Wallnut(Plant):
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.value = 50
        self.healthscore = 3600
        self.fixed = False
        self.type = "Wallnut"
        self.supercracked = loadImage(path + "/images/Plants/" + "SuperCrackedWallnut.png")
        self.cracked = loadImage(path + "/images/Plants/" + "CrackedWallnut1.png")
    
    def display(self):
        if self.healthscore >= 2400:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        elif 1200 <= self.healthscore <2400:
            image(self.cracked, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        elif 0 < self.healthscore < 1200:
            image(self.supercracked, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        else:
            game.plants.remove(self)
            board[self.row][self.column] = 0
            
        
        
    def __str__(self):
        return "Wallnut"    

    
class Peashooter(Plant):
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.value = 100
        self.healthscore = 300
        self.fixed = False
        self.type = "Peashooter"
        self.peas = []
        self.activated = False
        self.timer = 0
        
    def detect_same_row(self):
        if self.fixed == True:
            self.lst = []
            for zombie in game.zombies:
                if zombie.row == self.row:
                    self.lst.append(zombie)
            
            return self.lst
        
    def detect_approaching_zombies(self):
        if self.fixed == True:
            self.counter = 0
            self.targets = self.detect_same_row()
    
            for zombie in self.targets:
                if zombie.x <= Coordinates["LowerRight"][0] + 5:
                    self.counter = self.counter + 1

    

                
            if self.counter == 0:
                self.activated = False
                self.timer = 0
            elif self.counter != 0:
                self.activated = True
                
        
        
    def shoot_pea(self):
        self.pea = Pea(Point(self.p.x+15, self.p.y), 56,34, "PeaNormal_0.png", 20)
        self.timer = time.time()
        self.peas.append(self.pea)
        
    def let_pea_disappear(self, pea):
        if pea.disappear == True:
            self.peas.remove(pea)

    def update(self, dx, dy):
        if self.fixed == False:
            self.p.x = dx
            self.p.y = dy
        elif self.fixed == True:
            self.p.x = self.p.x
            self.p.y = self.p.y
            self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
            self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
            if frameCount%10 == 0:
                self.slice = (self.slice + 1) % self.num_slices
            
            self.detect_approaching_zombies()
            if self.activated == True and self.timer == 0:
                self.shoot_pea()
            elif self.activated == True and self.timer != 0:    #meaning it is not the first pea 
                if (time.time()-self.timer) >= 1.7:
                    self.shoot_pea()
            
    def __str__(self):
        return "Peashooter" 
    
    def display(self):
        if self.healthscore > 0:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
            # if len(self.peas) != 0:
            #     for pea in self.peas:
            #         pea.display()
            #         self.let_pea_disappear(pea)
        else:
            game.plants.remove(self)
            board[self.row][self.column] = 0
        
    
class Cherrybomb(Plant):
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.value = 150
        self.healthscore = 300
        self.fixed = False
        self.type = "Cherrybomb"
        self.img1 = loadImage(path + "/images/Plants/" + "Explosion.png")
        self.exploded = False
                
    def explode(self):
        self.exploded = True
        self.countdown = time.time()
        for zombie in game.zombies:
            if self.p.x - 1.5 * CELL_WIDTH <= zombie.x <= self.p.x + 1.5 * CELL_WIDTH and \
                self.row - 1 <= zombie.row <= self.row + 1:
                if zombie.condition != 'BoomDie' or zombie.condition != 'BoomDead':
                    zombie.condition = 'BoomDie'
        
    def update(self, dx, dy):
        if self.fixed == False:
            self.p.x = dx
            self.p.y = dy
        elif self.fixed == True:
            self.p.x = self.p.x
            self.p.y = self.p.y
            self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
            self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
            
            if self.exploded == False:
                if frameCount % 20 == 0:
                    self.slice = self.slice + 1
                if self.slice == self.num_slices:
                    self.explode()
                                    
    def __str__(self):
        return "Cherrybomb" 
    
    def display(self):
        if self.exploded == False:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
        elif self.exploded == True:
            if (time.time()-self.countdown) <= 3:
                image(self.img1, self.p.x, self.p.y, 246, 204)
            else:
                game.plants.remove(self)
                board[self.row][self.column] = 0
   
    
class Snowpeashooter(Plant):
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.value = 150
        self.healthscore = 300
        self.fixed = False
        self.peas = []
        self.type = "Snowpeashooter"
        self.activated = False
        self.timer = 0
        
    def detect_same_row(self):
        if self.fixed == True:
            self.lst = []
            for zombie in game.zombies:
                if zombie.row == self.row:
                    self.lst.append(zombie)
            
            return self.lst
        
    def detect_approaching_zombies(self):
        if self.fixed == True:
            self.counter = 0
            self.targets = self.detect_same_row()
    
            for zombie in self.targets:
                if zombie.x <= Coordinates["LowerRight"][0] + 5:
                    self.counter = self.counter + 1

    

                
            if self.counter == 0:
                self.activated = False
                self.timer = 0
            elif self.counter != 0:
                self.activated = True
                
                    
    def let_pea_disappear(self, pea):
        if pea.disappear == True:
            self.peas.remove(pea)        
    
    
    def shoot_pea(self):
        self.pea = Pea(Point(self.p.x+15, self.p.y), 56,34, "PeaIce_0.png", 30)
        self.timer = time.time()
        self.peas.append(self.pea)
    
    def update(self, dx, dy):
        if self.fixed == False:
            self.p.x = dx
            self.p.y = dy
        elif self.fixed == True:
            self.p.x = self.p.x
            self.p.y = self.p.y
            self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
            self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
            
            if frameCount%5 == 0:
                self.slice = (self.slice + 1) % self.num_slices
            
            self.detect_approaching_zombies()
            if self.activated == True and self.timer == 0:
                self.shoot_pea()
            elif self.activated == True and self.timer != 0:    #meaning it is not the first pea 
                if (time.time()-self.timer) >= 1.7:
                    self.shoot_pea() 
                    

    def display(self):
        if self.healthscore > 0:
            image(self.img, self.p.x, self.p.y, self.w, self.h, self.slice*self.w, 0, self.w*(self.slice + 1), self.h)
            # if len(self.peas) != 0:
            #     for pea in self.peas:
            #         pea.display()
            #         self.let_pea_disappear(pea)
        else:
            game.plants.remove(self)
            board[self.row][self.column] = 0
            
    
            
class Pea:
    def __init__(self, p, w, h, img, damage):
        self.p = p
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/Plants/Peas/" + img)
        self.splat = loadImage(path + "/images/Plants/Peas/" + "PeaNormalExplode_0.png")
        self.vx = 5.5
        self.damage = damage
        self.mid = Point(self.p.x +0.5*self.w, self.p.y + 0.5*self.h)
        self.column = (self.p.x - Coordinates["UpperLeft"][0])//CELL_WIDTH  
        self.row = (self.p.y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
        self.collision = False
        self.disappear = False
        
    def update(self):
   
        for zombie in game.zombies:
            self.check_collision(zombie)
                
        if self.collision == False:
            self.p.x = self.p.x + self.vx
        else:
            self.p.x = self.p.x
            
        
    
    def check_collision(self, Zombie):
        if self.row == Zombie.row:
            if self.p.x >= Zombie.x - 8.8 and Zombie.check_first_zombie(self):
                Zombie.health = Zombie.health - self.damage
                Zombie.hit_sound.rewind()
                Zombie.hit_sound.play()
                self.collision = True

    def __str__(self):
        return "Pea"
    
    def display(self):
        self.update()
        if self.collision == False:
            image(self.img, self.p.x, self.p.y, self.w, self.h, 0, 0, self.w, self.h)
        elif self.collision == True:
            image(self.splat, self.p.x, self.p.y, self.w, self.h, 0, 0, self.w, self.h)
            self.disappear = True

    
class Card():
    def __init__(self, x, y, w, h, value, img):
        self.x = x 
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/Cards/" + img)
        self.lock = loadImage(path + "/images/Cards/" + "Frozen.png")
        self.value = value        
        self.frozen = False
        
        
    def display_value(self):
        textSize(15)
        fill(5)
        text(self.value, self.x+ self.w - 38, self.y + self.h - 6)    
        
        
    def cooling_down(self):
        self.timer = time.time()
        self.frozen = True
        # print("Now the card is frozen")


#cherrybomb cooling time should be longer
    def update(self):
        self.current = time.time()
        if self.frozen == True:
            # print("Frozen")
            if (self.current - self.timer) >= 8:
                # print(self.current - self.timer)
                # print("Now the card is acticated")
                self.frozen = False
            elif (self.current - self.timer) <8:
                # print("Card is still unavailable")
                self.frozen = True
        
    
    def display(self):
        self.update()
        if self.frozen == False:
            image(self.img, self.x, self.y, self.w, self.h)
            self.display_value()
        elif self.frozen == True:
            image(self.img, self.x, self.y, self.w, self.h)
            self.display_value()
            image(self.lock, self.x, self.y, self.w, self.h)
            
class button:
    def __init__(self, x, y, w, h, img, txt):
        self.x = x 
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/Cards/" + img)
        self.txt = txt
        self.clicked = False
        
    def display_text(self):
        textSize(15)
        fill(5)
        text(self.txt, self.x, self.y)  
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
        self.display_txt()
        
            
class Menu():
    def __init__(self):
        self.cards = []
        self.SunflowerG = Card(10, 110,100, 60, 50, "SunFlowerG.png")
        self.WallnutG = Card(10, 180,100,60, 50, "WallNutG.png")
        self.PeashooterG = Card(10, 250,100, 60, 100, "PeashooterG.png")
        self.CherryBombG = Card(10, 320, 100, 60, 150, "CherryBombG.png")
        self.SnowPeashooterG = Card(10, 390, 100, 60, 150, "SnowPeaG.png")
        self.Shovel = Card(10,460, 71, 77, "", "Shovel.png")
        self.Sunflower = Card(10, 110,100, 60, 50, "SunFlower.png")
        self.Wallnut = Card(10, 180,100,60, 50, "WallNut.png")
        self.Peashooter = Card(10, 250,100, 60, 100,"Peashooter.png")
        self.CherryBomb = Card(10, 320, 100, 60, 150, "CherryBomb.png")
        self.SnowPeashooter = Card(10, 390, 100, 60, 150, "SnowPea.png")
        self.cards = [self.SunflowerG, self.WallnutG, self.PeashooterG, self.SnowPeashooterG,self.CherryBombG, self.Shovel]
        
                          
    def update(self):                
        if game.score < 50:
            self.cards[0] = self.SunflowerG
            self.cards[1] = self.WallnutG
            self.cards[2] = self.PeashooterG
            self.cards[3] = self.CherryBombG
            self.cards[4] = self.SnowPeashooterG
            
              #need to create a grey version      
        elif 50 <= game.score < 100 :
            self.cards[0] = self.Sunflower
            self.cards[1] = self.Wallnut
            self.cards[2] = self.PeashooterG
            self.cards[3] = self.CherryBombG
            self.cards[4] = self.SnowPeashooterG       
                       
        elif 100 <= game.score < 150:
            self.cards[0] = self.Sunflower
            self.cards[1] = self.Wallnut
            self.cards[2] = self.Peashooter
            self.cards[3] = self.CherryBombG
            self.cards[4] = self.SnowPeashooterG
            
                
        else:
            self.cards[0] = self.Sunflower
            self.cards[1] = self.Wallnut
            self.cards[2] = self.Peashooter
            self.cards[3] = self.CherryBomb
            self.cards[4] = self.SnowPeashooter
            
    def display(self):
        self.update()
        for card in self.cards:
            card.update()
            card.display()  



class Shovel(Plant):
    def __init__(self, p, w, h, num_slices, img):
        Plant.__init__(self, p, w, h, num_slices, img)
        self.active = False
        self.img = loadImage(path + "/images/Cards/" + img)

    def update(self, dx, dy):
        if self.active == True:
            self.p.x = dx
            self.p.y = dy
        elif self.active == False:
            self.p.x = self.p.x
            self.p.y = self.p.y
            
            
            
    def display(self):
        if self.active == True:
            image(self.img, self.p.x, self.p.y, self.w, self.h)
        

#create a blue version of all zombies in case they are hit by the snowpea.         
#add shovel to the menu    
class Game():
    def __init__(self):
        self.w = 1300
        self.h = 600
        self.score = 50
        self.menu = Menu()
        self.sun = Card(10,20,78,78, "", "Sun.png")
        self.stage = Stage("PVZBackground_3.jpeg", 0,0, 1400,600)
        self.bg_music = player.loadFile(path + "/sound/maintheme.mp3")
        self.bg_music.loop()
        self.win_picture = loadImage(path + "/images/Background/Win.png")
        self.win_sound = player.loadFile(path + "/sound/winmusic.mp3")
        self.lose_picture = loadImage(path + "/images/Background/Lose.png")
        self.lose_sound = player.loadFile(path + "/sound/lose.mp3")
        self.button = loadImage(path + "/images/Background/Restart.png")
        self.plants = []
        self.zombies = []
        self.heads = []
        self.mouse = False
        self.over = False
        self.timer = time.time()
        self.timer2 = time.time()
        self.time = 0
        self.fallingsuns = []
        self.lawnmower = []
        self.shovel = Shovel(Point(10,30), 71,77, 0, "Shovel.png")
        self.zombies_initialisation()

        
    def time_elapsed(self):
        self.time = time.time() - self.timer2
        # print(self.time)

    def display_score(self):
        textSize(20)
        fill(10)
        text(str(self.score), 90, 59)        
        #add a rectangle to surround the score!!!!!!!!!!!!

    def display_rectangle(self):
        noStroke()
        fill(205,133,63,200)
        rect(50,35,100,35,7)
        
    def add_plant(self, index):
        self.index = index 
        self.score = self.score - Plants_value[Plants_name[self.index]]
        self.mouse = True   #after clicking the card, the plant is moving with the mouse, and waiting for next click
        if self.index == 0:
            self.plant = Sunflower(Point(10,30), 73, 74, 16, "Sunflower.png")
            # self.sunflowers.append(self.plant)
        elif self.index == 1:
            self.plant = Wallnut(Point(10,30), 65, 73, 11, "Wallnut.png")
            # self.wallnuts.append(self.plant)
        elif self.index == 2:
            self.plant = Peashooter(Point(10,30), 71, 71, 13, "Peashooter1.png")
            # self.peashooters.append(self.plant)
        elif self.index == 3:
            self.plant = Cherrybomb(Point(10,30), 112, 81, 7, "Cherrybomb.png")
            # self.cherrybombs.append(self.plant)
        else:
            self.plant = Snowpeashooter(Point(10,30), 71, 71, 15,"Snowpeashooter.png")
            # self.snowpeashooters.append(self.plant)
            
        self.plants.append(self.plant)
        
        
    def shovel_activated(self):
        self.mouse = True
        self.shovel.active = True
        
    def shovel_disabled(self):
        self.mouse = False
        self.shovel.active = False

    def place_plant(self, x, y):
    
           #the plant is fixed at certain position, I have created a boundary or cell to place the plant
        if board[(y - Coordinates["UpperLeft"][1])//CELL_HEIGHT][(x - Coordinates["UpperLeft"][0])//CELL_WIDTH] == 0:
            board[(y - Coordinates["UpperLeft"][1])//CELL_HEIGHT][(x - Coordinates["UpperLeft"][0])//CELL_WIDTH] = self.plant
            self.plant.fixed = True 
            self.plant.p.x = x
            self.plant.p.y = y
            self.mouse = False  
            
        else:
            self.fixed = False    #change the naming !!!!!!!!!!
            
    def add_falling_sun(self):
        self.fallingsun = FallingSun(Point(random.randint(252, 900), 0), 78, 78, 22, "Sun.png")
        self.fallingsuns.append(self.fallingsun)        

    def update(self):
        self.menu.update()
        if (time.time() - self.timer) >= 10:
                self.add_falling_sun()
                self.timer = time.time() 
                
    def check_win(self):
        if self.start == True:
            if len(self.zombies)== 1:    #there is a normal zombie won't go into the yard, and we did not figure out why
                self.over = True
                self.win = True
                self.bg_music.pause()
                
    def check_lose(self):
        if self.start == True:
            for zombie in self.zombies:
                if zombie.x < Coordinates["UpperLeft"][0]:
                    self.over = True
                    self.win = False
                    self.bg_music.pause()
    
            

    def display_win(self):
        image(self.win_picture, 0, 0, 1000, 600, 0, 0, 960, 540)
        self.win_sound.play()
        
    def display_lose(self):
        image(self.lose_picture, 220, 100, 600, 360, 0, 0, 250, 207)
        self.lose_sound.play()
        
    def display_button(self):
        self.button_x = 450
        self.button_y = 450
        self.button_w = 201
        self.button_h = 81
        image(self.button, self.button_x, self.button_y)
        
    def restart(self):
        global board
        board = []
        for row in range(NUM_ROWS):
            row_list = []
            for column in range(NUM_COLS):
                row_list.append(0)
            board.append(row_list)
        self.__init__()

    
        
    def zombies_initialisation(self):
        my_list_1 = []
        for t in range(5):
            my_list_1.append((t + 1) * 15)
        random.shuffle(my_list_1)
        
        for r in range(5):
            self.zombies.append(NormalZombies(r, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], my_list_1[r]))
        
        my_list_2 = []
        for t in range(5):
            my_list_2.append((t + 6) * 15)
        random.shuffle(my_list_2)
        
        for r in range(5):
            self.zombies.append(NormalZombies(r, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], my_list_2[r]))
            self.zombies.append(ConeHeadZombies(r, Zombies_walk_list[1], NUM_SLICES_ZOMBIES_WALK[1], my_list_2[r]))
        
        my_list_3 = []
        for t in range(5):
            my_list_3.append((t + 11) * 15)
        random.shuffle(my_list_3)
        
        for r in range(5):
            self.zombies.append(NormalZombies(r, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], my_list_3[r]))
            self.zombies.append(NewspaperZombies(r, Zombies_walk_list[2], NUM_SLICES_ZOMBIES_WALK[2], my_list_3[r]))

        self.zombies.append(FlagZombies(random.randint(0, 4), Zombies_walk_list[3], NUM_SLICES_ZOMBIES_WALK[3], 16 * 15))
        my_list_4 = []
        for t in range(5):
            my_list_4.append(240 + t * 10)
        random.shuffle(my_list_4)
        
        for r in range(5):
            self.zombies.append(NormalZombies(r, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], my_list_4[r]))
            self.zombies.append(NormalZombies(r, Zombies_walk_list[0], NUM_SLICES_ZOMBIES_WALK[0], my_list_4[r]))
            self.zombies.append(ConeHeadZombies(r, Zombies_walk_list[1], NUM_SLICES_ZOMBIES_WALK[1], my_list_4[r]))
            self.zombies.append(NewspaperZombies(r, Zombies_walk_list[2], NUM_SLICES_ZOMBIES_WALK[2], my_list_4[r]))
            
        self.start = True
        
    def zombies_update(self):
        
        for zombie in self.zombies:
            if zombie.delete:
                self.zombies.remove(zombie)
                
        for head in self.heads:
            if head.delete:
                self.heads.remove(head)
        
            
    def display(self):
        if self.over == False:
            self.time_elapsed()
            self.update()
            self.stage.display()
            self.menu.display()   
            self.zombies_update()
        
  
            
            for plant in self.plants:
                plant.update(mouseX - 0.5*plant.w, mouseY - 0.5*plant.h)
                plant.display()

            for zombie in self.zombies:
                zombie.display()
            
            for head in self.heads:
                head.display()
            
            for plant in self.plants:
                if plant.type == "Peashooter" or plant.type == "Snowpeashooter":
                    if len(plant.peas) != 0:
                        for pea in plant.peas:
                            pea.display()
                            plant.let_pea_disappear(pea)
                

            if len(self.fallingsuns)!= 0:
                for sun in self.fallingsuns:
                    sun.update()
                    sun.display()
            self.display_rectangle()    
            self.sun.display()
            self.display_score()
            self.shovel.update(mouseX - 0.5*self.shovel.w, mouseY - 0.5*self.shovel.h)
            self.shovel.display()
            self.check_win()
            self.check_lose()
            
            
        elif self.over == True:
            self.stage.display()
            self.menu.display()
            self.display_rectangle()    
            self.sun.display()
            self.display_score()
            self.shovel.display()
            
            if self.win == True:
                self.display_win()
                self.display_button()
            elif self.win == False:
                self.display_lose()
                self.display_button()
                
                ###new modification made here
                    
        
stage_1 = Stage("Instruction_1.jpg", 0, 0, 1000, 600)   
game = Game()
        
def setup():
    size(1000, 600)   #995,575    995, 90 is the above line
    background(255, 255, 255)
    
def draw():
    background(255, 255, 255)
    if frameCount <= 300:
        stage_1.display()
    elif frameCount > 300:
        game.display()
    

def mouseReleased():
    x = mouseX
    y = mouseY
    if game.over == False and game.mouse == False:  #first click
        if len(game.plants) != 0:
            for plant in game.plants:
                if plant.type == "Sunflower":
                    if len(plant.suns) != 0:
                        for sun in plant.suns:
                            if sun.p.x <= x <= sun.p.x + sun.w and sun.p.y <= y <= sun.p.y + sun.h and sun.clicked != True:
                                sun.click() 
                        
        if len(game.fallingsuns)!= 0:
            for sun in game.fallingsuns:
                if sun.p.x <= x <= sun.p.x + sun.w and sun.p.y <= y <= sun.p.y + sun.h and sun.clicked != True:
                    sun.click()  
                
                            
           
             
        for card in game.menu.cards:
            if card.x <= x <= card.x + card.w and card.y <= y <= card.y + card.h:
                if game.score >= card.value and game.menu.cards.index(card) < 5:
                    if card.frozen == False:
                        game.add_plant(game.menu.cards.index(card))
                        # print("you sucessfully add the plant into the game!")
                        card.cooling_down()
                elif game.menu.cards.index(card) == 5:
                    game.shovel_activated()
                
    
    if game.over == False and game.mouse == True and game.shovel.active == False:#game.mouse True means that the plant is moving with the mouse, exclude the condition where the shovel is activated
        if Coordinates["UpperLeft"][0] <= x <= Coordinates["LowerRight"][0] and Coordinates["UpperLeft"][1] <= y <= Coordinates["LowerRight"][1]:
            # row = (x - Coordinates["UpperLeft"][0])//CELL_WIDTH 
            # column = (y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
            x_desired = ((x - Coordinates["UpperLeft"][0])//CELL_WIDTH)* CELL_WIDTH + Coordinates["UpperLeft"][0]  #left most is 252, 
            y_desired = ((y - Coordinates["UpperLeft"][1])//CELL_HEIGHT)*CELL_HEIGHT + Coordinates["UpperLeft"][1]   #x_desired and y_desired the desired position for placing the plants
            game.place_plant(x_desired,y_desired)
            

            
    elif game.over == False and game.mouse == True and game.shovel.active == True:
        if Coordinates["UpperLeft"][0] <= x <= Coordinates["LowerRight"][0] and Coordinates["UpperLeft"][1] <= y <= Coordinates["LowerRight"][1]:
            if board[(y - Coordinates["UpperLeft"][1])//CELL_HEIGHT][(x - Coordinates["UpperLeft"][0])//CELL_WIDTH] != 0:
                r = (y - Coordinates["UpperLeft"][1])//CELL_HEIGHT
                c = (x - Coordinates["UpperLeft"][0])//CELL_WIDTH
                for plant in game.plants:
                    if plant.row == r and plant.column == c:
                        
                        game.score = game.score + 0.5*plant.value
                        game.plants.remove(plant)
                        board[r][c] = 0
                        game.shovel_disabled()
                        # print(board)
                    
                
            elif board[(y - Coordinates["UpperLeft"][1])//CELL_HEIGHT][(x - Coordinates["UpperLeft"][0])//CELL_WIDTH] == 0:
                game.shovel_disabled()
                
    elif game.over == True:
       if (game.button_x <= x <= game.button_x + game.button_w) and (game.button_y <= y <= game.button_y + game.button_h):
           game.restart()
       
       
           #write the button range here
           #then click the button will invoke the restart button
                    
                
                
    
