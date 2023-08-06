# encoding: utf-8
# module pyscratch
#

import sys, os, pygame, threading, time, math, random, inspect, functools

from pygame.locals import *

game_running = True


backdrop_color = (255, 255, 255)
fps = 35
time_piece = 1/fps
cur_fragment = {}
func_stack = {}

screen = None
events = {}
backdrop = None
lines = []
sprites = {}

#
pygame.init()
screen = pygame.display.set_mode((480, 360))
screen.fill(backdrop_color)
#pygame.display.update()


def refresh_events(start_time):
    global events
    new_events = {}
    for event_name, time_list in events.items():
        new_time_list = []
        for event_time in time_list:
            if event_time > start_time - time_piece:  # not too old
                new_time_list.append(event_time)
        if len(new_time_list) > 0:
            new_events[event_name] = new_time_list
    events = new_events


def update_screen():
    if not game_running:
        return
    # draw back ground
    if backdrop and backdrop.get_locked() is not True:
        screen.blit(backdrop, (0, 0))
    else:
        screen.fill(backdrop_color)
    # draw all lines
    for line in lines:
        #
        start_x = line['start_pos'][0] + 240
        start_y = 180 - line['start_pos'][1]
        end_x = line['end_pos'][0] + 240
        end_y = 180 - line['end_pos'][1]

        pygame.draw.line(screen, line['color'], [start_x, start_y], [end_x, end_y], line['width'])
    # draw all sprite
    #print(list(scratch.sprites.values())[0].rect)
    for s in list(sprites.values()):
        if not s.sprite.get_locked():
            #
            rect = s.rect.copy()
            rect.x = rect.x + 240 - rect.width//2
            rect.y = 180 - rect.y - rect.height//2
            screen.blit(s.sprite, rect)
            #print("a rect",rect)
            #print("s rect",s.sprite.get_rect())
    pygame.display.update()


def frame_loop():
    while game_running:

        # time fragment
        start_time = time.perf_counter()
        cur_fragment['start_time'] = start_time
        cur_fragment['end_time'] = start_time + time_piece

        func_stack.clear()
        # event
        refresh_events(time.perf_counter())
        # events.clear()

        update_screen()
        elapsed = time.perf_counter() - start_time

        if time_piece > elapsed:
            time.sleep(time_piece - elapsed)


threading.Thread(target=frame_loop).start()


def frame_control(func):

    def wrapper(*args, **kwargs):

        get_events()

        stack = inspect.stack()
        stack_str = ""
        for s in stack:
            stack_str = stack_str + s[1] + str(s[2])
        hash_str = hash(str(stack_str))

        if hash_str in func_stack:
            # pause the function call if duplicate call in one fragment
            if func_stack[hash_str] > cur_fragment['start_time']:
                time.sleep(cur_fragment['end_time'] - func_stack[hash_str])

        func_stack[hash_str] = time.perf_counter()
        result = func(*args, **kwargs)
        #update_screen()
        functools.update_wrapper(wrapper, func)
        return result
    return wrapper


def global_event(event_name, event_time=None):
    if event_time is None:
        event_time = time.perf_counter()
    # append event to global events
    if event_name in events:
        events[event_name].append(event_time)
    else:
        events[event_name] = [event_time]

    for s in list(sprites.values()):
        s.event(event_name)


def erase_all():
    lines.clear()


def key_pressed(key):
    if key in events:
        return True
    else:
        return False


def add_line(color, start_pos, end_pos, width):
    line = {'color': color, 'start_pos': start_pos, 'end_pos': end_pos, 'width': width}
    lines.append(line)


def get_events():
    global game_running
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False;
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            global_event(event.key)


def start():
    global game_running
    game_running = True
    global_event("start")

    while game_running:
        get_events()
        time.sleep(0.01)


class Sprite(object):

    def __init__(self, sprite_name, name=None, x=0, y=0):
        #name = str(name, 'utf-8')
        if name is None:
            name = sprite_name
        self.sprite_size = 100
        self.x = x
        self.y = y
        self.direction = 90
        self.timer_start = time.perf_counter()
        self.pen_down_flag = False
        self.pen_size = 1
        self.pen_color = (0, 150, 0)
        self.event_watcher = {}
        self.costumeDict = {}
        if not os.path.exists(name):
            name = os.path.join(os.path.split(__file__)[0], "sprite", name)

        for file_name in os.listdir(name):
            file_name_key = os.path.splitext(file_name)[0]
            self.costumeDict[file_name_key] = os.path.join(name, file_name) #open(os.path.join(name,file_name), 'r')

        current_costume = list(self.costumeDict.items())[0]
        self.current_costume_key = current_costume[0]
        self.current_costume_value = current_costume[1]

        self.sprite = pygame.image.load(self.current_costume_value).convert_alpha()
        self.rect = self.sprite.get_rect() #rect(1,2,3,4) #  self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites[sprite_name] = self

    @frame_control
    def set_x_to(self, new_x):
        self.x = new_x
        self.rect.x = new_x

    @frame_control
    def set_y_to(self, new_y):
        self.y = new_y
        self.rect.y = new_y

    @frame_control
    def change_x_by(self, change_x):
        self.x = self.x + change_x
        self.rect.x = self.rect.x + change_x

    @frame_control
    def change_y_by(self, change_y):#
        self.y = self.y + change_y
        self.rect.y = self.rect.y + change_y

    def flip(self):
        self.sprite = pygame.transform.flip(self.sprite, True, False);

    def size(self, num):
        width = self.rect.width
        height = self.rect.height
        new_width = int(width * (num/self.sprite_size))
        new_height = int(height * (num / self.sprite_size))
        self.sprite = pygame.transform.smoothscale(self.sprite, (new_width, new_height))
        self.rect.width = new_width
        self.rect.height = new_height
        self.sprite_size = num

    def switch_costume_to(self, name):
        if name != self.current_costume_key:
            self.current_costume_key = name
            self.current_costume_value = self.costumeDict.get(name)
            new_sprite = pygame.image.load(self.current_costume_value).convert_alpha()
            new_sprite = pygame.transform.smoothscale(new_sprite, (self.rect.width, self.rect.height))
            self.sprite = new_sprite

    @frame_control
    def move(self, steps):
        direction = 90 - self.direction
        direction_pi = math.pi * (direction/180) # to π

        steps_x = steps * round(math.cos(direction_pi), 15)
        steps_y = steps * round(math.sin(direction_pi), 15)

        self.go_to(self.rect.x + steps_x, self.rect.y + steps_y)

    @frame_control
    def go_to(self, new_x, new_y):
        if self.pen_down_flag:
            add_line(self.pen_color, [self.rect.x, self.rect.y], [new_x, new_y], self.pen_size)
        self.set_x_to(new_x)
        self.set_y_to(new_y)

    @frame_control
    def turn(self, degrees):
        self.sprite = pygame.transform.rotate(self.sprite, degrees) #-degree
        self.direction = self.direction + degrees

    @frame_control
    def glide_secs_to_x_y(self, sec, x, y):
        interval = fps
        step_x = (x - self.rect.x)//interval
        step_y = (y - self.rect.y)//interval
        for i in range(interval):
            self.set_x_to(self.rect.x + step_x)
            self.set_y_to(self.rect.y + step_y)
            time.sleep(sec/interval)

    def bounce_if_on_edge(self):
        if self.rect.x > 240:
            self.direction = -self.direction
            self.flip()
        elif self.rect.x < -240:
            self.direction = -self.direction
            self.flip()
        elif self.rect.y > 180:
            self.direction = 180 - self.direction
        elif self.rect.y < -180:
            self.direction = 180 - self.direction

    #scratch coordinate to pygame coordinate
    def pygame_rect(self, target_rect):
        new_rect = target_rect.copy()
        new_rect.x = new_rect.x + 240 - new_rect.width // 2
        new_rect.y = 180 - new_rect.y - new_rect.height // 2
        return new_rect

    # Events
    def regist_event(self, event_name, func):
        if event_name in self.event_watcher:
            functions = self.event_watcher.get(event_name)
            functions.append(func)
        else:
            self.event_watcher[event_name] = [func]

    def when_start(self, func):
        self.regist_event("start", func)

    def when_key_pressed(self, key_name, func):
        self.regist_event(key_name, func)

    def when_receive(self,event_name, func):
        self.regist_event(event_name, func)

    #Control
    def wait(self, seconds):
        time.sleep(seconds)

    # Sensing
    def touching(self, sprite_name):
        sprite_2 = sprites.get(sprite_name)
        if sprite_2 is None:
            return False
        return pygame.Rect.colliderect(self.pygame_rect(self.rect), self.pygame_rect(sprite_2.rect))

    def reset_timer(self):
        self.timer_start = time.perf_counter()

    def timer(self):
        return time.perf_counter() - self.timer_start

    #Operators
    def random(self,from_num, to_num):
        return random.randrange(from_num, to_num)

    #Pen
    @frame_control
    def pen_down(self):
        self.pen_down_flag = True

    @frame_control
    def pen_up(self):
        self.pen_down_flag = False

    def event(self, event_name):
        if event_name in self.event_watcher:
            functions = self.event_watcher.get(event_name)
            for f in functions:
                t = threading.Thread(target=f)#name='LoopThread'
                t.start()


def switch_backdrop(name):
    global backdrop

    if os.path.exists(name):
        backdrop = pygame.image.load(name).convert_alpha()
    else:
        if not name.endswith(".jpg"):
            name = name + ".jpg"
            name = os.path.join(os.path.split(__file__)[0], "backdrop", name)
            backdrop = pygame.image.load(name).convert_alpha()
