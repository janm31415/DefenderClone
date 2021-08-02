import pgzrun
import random

pixel_size = 5

#x = 64
#y = 40

WIDTH = 640
HEIGHT = 400
TITLE = "Defender"

screen_x = 0

max_planet_x = WIDTH*10
max_planet_y = 100

planet_x = []
planet_y = []

gray = (80,80,80)
red = (255,0,0)
green=(0,200,0)
yellow=(255,200,0)
pink=(252,3,211)
white=(255,255,255)
blue = (0,0,255)
brown=(150, 75, 0)
black=(0,0,0)

timer = 0

humans = []

class Sprite:
  x = 0
  y = 0
  w = 0
  h = 0
  dir = 1
  
spacecraft = Sprite()

def init_spacecraft():
  spacecraft.x = 64
  spacecraft.y = 40
  spacecraft.w = 16
  spacecraft.h = 6
  spacecraft.dir = -1
  
def init_humans():
  global humans
  humans = []
  for i in range(0, 6):
    h = Sprite()
    h.x = random.randint(0, max_planet_x/pixel_size)
    h.y = HEIGHT/pixel_size - 5 - random.randint(0, 10)
    h.w = 4
    h.h = 8
    h.dir = random.randint(0, 1)*2-1
    humans.append(h)

def build_planet():
  print("Building a planet...", flush=True)
  planet_x.append(0)
  planet_y.append(random.randint(0, max_planet_y))
  last_x = 0
  while last_x < max_planet_x:
    last_x += random.randint(1, 100)
    if last_x < max_planet_x:
      planet_x.append(last_x)
      planet_y.append(random.randint(0, max_planet_y))
  planet_x.append(max_planet_x)
  planet_y.append(planet_y[0])
      
def draw_planet():
  l = len(planet_x)
  for i in range(0, l):
    s=(planet_x[i]-screen_x, HEIGHT-1-planet_y[i])
    e=(planet_x[(i+1)%l]-screen_x, HEIGHT-1-planet_y[(i+1)%l])
    if e[0] < 0:
      s=(planet_x[i]-screen_x+max_planet_x, HEIGHT-1-planet_y[i])
      e=(planet_x[(i+1)%l]-screen_x+max_planet_x, HEIGHT-1-planet_y[(i+1)%l])
    if s[0] < e[0]:
      screen.draw.line(start=s, end=e, color=brown)

def fill_pixel(x, y, clr):
  pixel = Rect((x*pixel_size, y*pixel_size), (pixel_size, pixel_size))
  screen.draw.filled_rect(pixel, clr)

def random_burst_color():
  r = random.randint(0, 4)
  if r == 0:
    return green
  if r == 1:
    return blue
  if r == 2:
    return red
  if r == 3:
    return gray
  return yellow
  
def draw_defender(px, py, dir):
  fill_pixel(px-dir*8, py, green)
  fill_pixel(px-dir*7, py, white)
  fill_pixel(px-dir*6, py, gray)
  fill_pixel(px-dir*5, py, gray)
  fill_pixel(px-dir*4, py, gray)
  fill_pixel(px-dir*3, py, gray)
  fill_pixel(px-dir*2, py, gray)
  fill_pixel(px-dir, py, gray)
  fill_pixel(px, py, gray)
  fill_pixel(px+dir, py, pink)
  fill_pixel(px+dir*2, py, pink)
  fill_pixel(px+dir*3, py, pink)
  fill_pixel(px+dir*4, py, pink)
  fill_pixel(px+dir*5, py, gray)
  fill_pixel(px+dir*6, py, green)
  
  fill_pixel(px-dir*5, py-1, red)
  fill_pixel(px-dir*4, py-1, blue)
  fill_pixel(px-dir*3, py-1, yellow)
  fill_pixel(px-dir*2, py-1, gray)
  fill_pixel(px-dir, py-1, gray)
  fill_pixel(px, py-1, gray)
  fill_pixel(px+dir, py-1, gray)
  fill_pixel(px+dir*2, py-1, gray)
  fill_pixel(px+dir*3, py-1, pink)
  fill_pixel(px+dir*4, py-1, pink)
  fill_pixel(px+dir*5, py-1, green)
  
  fill_pixel(px-dir, py+1, green)
  fill_pixel(px, py+1, white)
  fill_pixel(px+dir, py+1, gray)
  fill_pixel(px+dir*2, py+1, pink)
  fill_pixel(px+dir*3, py+1, pink)
  fill_pixel(px+dir*4, py+1, pink)  

  fill_pixel(px+dir, py-2, gray)
  fill_pixel(px+dir*2, py-2, gray)
  fill_pixel(px+dir*3, py-2, gray)
  fill_pixel(px+dir*4, py-2, gray)
  fill_pixel(px+dir*5, py-2, gray)
  fill_pixel(px+dir*6, py-2, green)

  fill_pixel(px+dir*2, py-3, gray)
  fill_pixel(px+dir*3, py-3, gray)
  fill_pixel(px+dir*4, py-3, gray)
  fill_pixel(px+dir*5, py-3, gray)
  
  fill_pixel(px+dir*3, py-4, gray)
  fill_pixel(px+dir*4, py-4, gray)

  
  fill_pixel(px+dir*8, py-3, random_burst_color())
  fill_pixel(px+dir*9, py-3, random_burst_color())
  fill_pixel(px+dir*8, py-2, random_burst_color())
  fill_pixel(px+dir*9, py-2, random_burst_color())
  fill_pixel(px+dir*8, py-1, random_burst_color())
  fill_pixel(px+dir*9, py-1, random_burst_color())
  fill_pixel(px+dir*8, py-0, random_burst_color())
  fill_pixel(px+dir*9, py-0, random_burst_color())
  fill_pixel(px+dir*8, py+1, random_burst_color())
  fill_pixel(px+dir*9, py+1, random_burst_color())


def draw_manti(px, py, t):
  t = (t//10) % 3
  a = green
  b = green
  c = black
  d = green
  e = black
  if t == 1:
    a = green
    b = black
    c = green
    d = black
    e = green
  if t == 2:
    a = black
    b = green
    c = black
    d = green
    e = green

  fill_pixel(px-3, py, green)
  fill_pixel(px-3, py-1, green)
  fill_pixel(px, py, c)
  fill_pixel(px, py-1, c)
  fill_pixel(px-1, py, b)
  fill_pixel(px-1, py-1, b)
  fill_pixel(px-2, py, a)
  fill_pixel(px-2, py-1, a)
  fill_pixel(px+1, py, d)
  fill_pixel(px+1, py-1, d)
  fill_pixel(px+2, py, e)
  fill_pixel(px+2, py-1, e)
  fill_pixel(px+3, py, green)
  fill_pixel(px+3, py-1, green)

  fill_pixel(px, py-2, yellow)
  fill_pixel(px, py-3, yellow)
  fill_pixel(px-1, py-2, yellow)
  fill_pixel(px-1, py-3, yellow)
  fill_pixel(px+1, py-2, yellow)
  fill_pixel(px+1, py-3, yellow)
  fill_pixel(px-2, py-2, green)
  fill_pixel(px+2, py-2, green)
  fill_pixel(px-2, py+1, green)
  fill_pixel(px+2, py+1, green)
  fill_pixel(px-1, py+1, yellow)
  fill_pixel(px+1, py+1, yellow)
  fill_pixel(px, py+1, green)
  fill_pixel(px, py+2, green)
  fill_pixel(px, py+3, green)
  fill_pixel(px, py+4, green)
  fill_pixel(px-2, py+2, green)
  fill_pixel(px-3, py+3, green)
  fill_pixel(px-4, py+4, green)
  fill_pixel(px+2, py+2, green)
  fill_pixel(px+3, py+3, green)
  fill_pixel(px+4, py+4, green)  

def draw_human(px, py, dir):
  fill_pixel(px, py, brown)
  fill_pixel(px, py+1, brown)
  fill_pixel(px+1, py, pink)
  fill_pixel(px+1, py+1, pink)
  fill_pixel(px-1, py, pink)
  fill_pixel(px-1, py+1, pink)
  fill_pixel(px, py+2, brown)
  fill_pixel(px, py+3, brown)
  fill_pixel(px, py+4, brown)
  fill_pixel(px-dir, py-1, pink)
  fill_pixel(px+dir, py-1, yellow)
  fill_pixel(px, py-1, green)
  fill_pixel(px+dir, py-2, yellow)
  fill_pixel(px, py-2, green)
  fill_pixel(px+dir, py-3, green)
  fill_pixel(px, py-3, green)  

def draw_mutant(px, py, t):
  d = (t//10 % 2)*2 - 1

  fill_pixel(px+3, py, green)
  fill_pixel(px+3, py-1, green)
  fill_pixel(px-3, py, green)
  fill_pixel(px-3, py-1, green)


  fill_pixel(px-2, py-2, green)
  fill_pixel(px+2, py-2, green)
  fill_pixel(px-2, py+1, green)
  fill_pixel(px+2, py+1, green)
  fill_pixel(px-1, py+1, yellow)
  fill_pixel(px+1, py+1, yellow)
  fill_pixel(px-2, py+2, green)
  fill_pixel(px-3, py+3, green)
  fill_pixel(px-4, py+4, green)
  fill_pixel(px+2, py+2, green)
  fill_pixel(px+3, py+3, green)
  fill_pixel(px+4, py+4, green)  

  fill_pixel(px, py, brown)
  fill_pixel(px, py+1, brown)
  fill_pixel(px+1, py, pink)
  fill_pixel(px+1, py+1, pink)
  fill_pixel(px-1, py, pink)
  fill_pixel(px-1, py+1, pink)
  fill_pixel(px, py+2, brown)
  fill_pixel(px, py+3, brown)
  fill_pixel(px, py+4, brown)
  fill_pixel(px-d, py-1, pink)
  fill_pixel(px+d, py-1, blue)
  fill_pixel(px, py-1, blue)
  fill_pixel(px+d, py-2, blue)
  fill_pixel(px, py-2, blue)
  fill_pixel(px+d, py-3, blue)
  fill_pixel(px, py-3, blue)  
  
def random_bullet_color():
  r = random.randint(0, 3)
  if r == 0:
    return white
  if r == 1:
    return red
  if r == 2:
    return yellow
  if r == 3:
    return gray
  return white
  

def draw_bullet(px, py):
  fill_pixel(px, py, random_bullet_color())
  fill_pixel(px, py-1, random_bullet_color())
  fill_pixel(px-1, py, random_bullet_color())
  fill_pixel(px, py+1, random_bullet_color())
  fill_pixel(px+1, py, random_bullet_color())


def update():
  global screen_x
  global spacecraft
  global timer
  if keyboard.left:
    screen_x = (screen_x - 10)%max_planet_x
    spacecraft.dir = 1
  if keyboard.right:
    screen_x = (screen_x + 10)%max_planet_x
    spacecraft.dir = -1
  if keyboard.up:
    spacecraft.y = spacecraft.y - 1
    if spacecraft.y < 4:
      spacecraft.y = 4
  if keyboard.down:
    spacecraft.y = spacecraft.y + 1
    if spacecraft.y > HEIGHT/pixel_size-4:
      spacecraft.y = HEIGHT/pixel_size-4
  timer = timer + 1

def draw_humans():
  for i in range(0, len(humans)):
    x = humans[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    draw_human(x, humans[i].y, humans[i].dir)

def draw():
  screen.fill('black')
  screen.draw.text("Hello", topleft=(10,10))
  draw_planet()
  draw_defender(spacecraft.x, spacecraft.y, spacecraft.dir)
  draw_humans()
  #draw_manti(40, 40, timer)
  #draw_human(80, 40, -1)
  #draw_mutant(100, 40, timer)
  #draw_bullet(120, 40)
  
def init_game():
  build_planet()
  init_spacecraft()
  init_humans()

init_game()
pgzrun.go()