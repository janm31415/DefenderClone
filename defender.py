import pgzrun
import random
import math

pixel_size = 3

WIDTH = 640 - (640%pixel_size)
HEIGHT = 400 - (400%pixel_size)

TITLE = "Defender"

screen_x = 0

wave = 1

max_planet_x = WIDTH*10
max_planet_y = 100

planet_x = []
planet_y = []

speed_x = 0
score = 0

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
gameover = 0
space_is_pressed = 0

mantis_speed = 0.5
mutant_speed = 1
bullet_speed = 2

humans = []
mantis = []
lasers = []
mutants = []
bullets = []

explosions = []

lives = 3

class Sprite:
  x = 0
  y = 0
  w = 0
  h = 0
  dir = 1
  alive = 0
  state = 0
  vx = 0
  vy = 0
  
  
class Explosion:
  x = 0
  y = 0
  t = 0
  
spacecraft = Sprite()

def init_spacecraft():
  global spacecraft
  spacecraft.x = WIDTH//(2*pixel_size)
  spacecraft.y = HEIGHT//(2*pixel_size)
  spacecraft.w = 16
  spacecraft.h = 6
  spacecraft.dir = -1
  spacecraft.alive = 1
  spacecraft.state = 0
  
def init_humans(nr):
  global humans
  humans = []
  for i in range(0, nr):
    h = Sprite()
    h.x = random.randint(0, max_planet_x/pixel_size)
    h.y = HEIGHT/pixel_size - 5 - random.randint(0, 5)
    h.w = 4
    h.h = 8
    h.dir = random.randint(0, 1)*2-1
    h.alive = 1
    h.state = 0
    humans.append(h)

def init_mantis(nr):
  global mantis
  mantis = []
  for i in range(0, nr):
    h = Sprite()
    h.x = random.randint(WIDTH//pixel_size, max_planet_x/pixel_size)
    h.y = random.randint(5, HEIGHT/pixel_size-5)
    h.w = 8
    h.h = 8
    h.dir = random.randint(0, 1)*2-1
    h.alive = 1
    h.state = 0
    mantis.append(h)

def reset_mantis():
  global mantis
  for i in range(0, len(mantis)):    
    mantis[i].x = random.randint(WIDTH//pixel_size, max_planet_x/pixel_size)
    #mantis[i].y = random.randint(5, HEIGHT/pixel_size-5)  

def reset_mutants():
  global mutants
  for i in range(0, len(mutants)):    
    mutants[i].x = random.randint(WIDTH//pixel_size, max_planet_x/pixel_size)


def init_wave(w):
  global screen_x
  global lasers
  global explosions
  global bullets
  init_humans(4+w*2)
  init_mantis(4+w*2)
  init_spacecraft()
  lasers = []
  explosions = []
  bullets = []
  screen_x = 0

def debug(s):
  print(s, flush=True)

def build_planet():  
  global planet_x
  global planet_y
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
  global planet_x
  global planet_y
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

def draw_explosion(px, py, t):
  fill_pixel(px-t, py, random_burst_color())
  fill_pixel(px+t, py, random_burst_color())
  fill_pixel(px, py-t, random_burst_color())
  fill_pixel(px, py+t, random_burst_color())
  fill_pixel(px-t, py-t, random_burst_color())
  fill_pixel(px+t, py-t, random_burst_color())
  fill_pixel(px-t, py+t, random_burst_color())
  fill_pixel(px+t, py+t, random_burst_color())

def draw_laser(px, py, w):
  for i in range(0, w):
    fill_pixel(px+i-w//2, py, random_bullet_color())
  

def add_explosion(x,y):
  global explosions
  e = Explosion()
  e.x = x
  e.y = y
  e.t = 0
  explosions.append(e)
  

def collide(a, b):
  ax = a.x - a.w/2
  ay = a.y - a.h/2
  ax2 = a.x + a.w/2
  ay2 = a.y + a.h/2
  bx = b.x - b.w/2
  by = b.y - b.h/2
  bx2 = b.x + b.w/2
  by2 = b.y + b.h/2
  if (ax <= bx2) and (ax2 >= bx) and (ay <= by2) and (ay2 >= by):
    return True
  return False

def spacecraft_dead():
  global lives
  global gameover
  global spacecraft
  spacecraft.alive = 0
  add_explosion(spacecraft.x, spacecraft.y)
  lives = lives - 1

def check_human_spacecraft_collisions():
  global humans
  global spacecraft
  for i in range(0, len(humans)):
    if (humans[i].alive != 0) and (spacecraft.alive != 0):
      if collide(humans[i], spacecraft):
        if humans[i].state == 2:
          humans[i].state = 3
        

def check_mantis_spacecraft_collisions():  
  global mantis
  global spacecraft
  for i in range(0, len(mantis)):
    if (mantis[i].alive != 0) and (spacecraft.alive != 0):
      if collide(mantis[i], spacecraft):
        spacecraft_dead()
        
def check_mutants_spacecraft_collisions():  
  global mutants
  global spacecraft
  for i in range(0, len(mutants)):
    if (mutants[i].alive != 0) and (spacecraft.alive != 0):
      if collide(mutants[i], spacecraft):
        spacecraft_dead()
        
def check_bullet_spacecraft_collisions():
  global bullets
  global spacecraft
  for i in range(0, len(bullets)):
    if (spacecraft.alive != 0) and collide(bullets[i], spacecraft):
      spacecraft_dead()

def check_mantis_laser_collisions():
  global score
  global mantis
  global lasers
  for i in range(0, len(mantis)):
    if (mantis[i].alive != 0):
      for j in reversed(range(0, len(lasers))):
        if collide(mantis[i], lasers[j]):
          mantis[i].alive = 0
          add_explosion(mantis[i].x, mantis[i].y)
          score = score + 100
          if (mantis[i].state == 1):
            humans[i].state = 2
          lasers.pop(j)
          
def check_mutants_laser_collisions():
  global score
  global mutants
  global lasers
  for i in range(0, len(mutants)):
    if (mutants[i].alive != 0):
      for j in reversed(range(0, len(lasers))):
        if collide(mutants[i], lasers[j]):
          mutants[i].alive = 0
          add_explosion(mutants[i].x, mutants[i].y)
          score = score + 200
          lasers.pop(j)
          
def check_bullet_laser_collisions():
  global bullets
  global lasers
  for i in reversed(range(0, len(bullets))):
    for j in reversed(range(0, len(lasers))):
      if collide(bullets[i], lasers[j]):
        add_explosion(bullets[i].x, bullets[i].y)
        bullets.pop(i)
        lasers.pop(j)        


def check_human_laser_collisions():
  global score
  global humans
  global lasers
  for i in range(0, len(humans)):
    if (humans[i].alive != 0) and (humans[i].state == 0):
      for j in reversed(range(0, len(lasers))):
        if collide(humans[i], lasers[j]):
          humans[i].alive = 0
          add_explosion(humans[i].x, humans[i].y)    
          lasers.pop(j)      

def check_mantis_humans_collisions():
  global mantis
  global humans
  for i in range(0, len(mantis)):
    if (mantis[i].alive != 0) and (mantis[i].state == 0):
      if (humans[i].alive != 0) and (humans[i].state == 0):
        if collide(humans[i], mantis[i]):
          humans[i].state = 1
          mantis[i].state = 1

  
def check_collisions():
  check_bullet_laser_collisions()
  check_human_laser_collisions()
  check_mantis_laser_collisions()  
  check_mutants_laser_collisions()  
  check_human_spacecraft_collisions()
  check_mantis_spacecraft_collisions()
  check_mutants_spacecraft_collisions()
  check_mantis_humans_collisions()
  check_bullet_spacecraft_collisions()

def update_explosions():
  global explosions
  for i in range(0, len(explosions)):
    explosions[i].t = explosions[i].t + 1
  for i in reversed(range(0, len(explosions))):
    if explosions[i].t > 100:
      explosions.pop(i)
      
def update_lasers():
  global lasers
  for i in range(0, len(lasers)):
    lasers[i].t = lasers[i].t + 1
    lasers[i].x -= lasers[i].dir * lasers[i].w
  for i in reversed(range(0, len(lasers))):
    if lasers[i].t > ((((WIDTH//pixel_size)//lasers[i].w)//2)+1):
      lasers.pop(i)
          
      
def get_number_of_mantis():
  global mantis
  nr = 0
  for i in range(0, len(mantis)):
    if mantis[i].alive != 0:
      nr = nr + 1
  return nr      
      
def get_number_of_mutants():
  global mutants
  nr = 0
  for i in range(0, len(mutants)):
    if mutants[i].alive != 0:
      nr = nr + 1
  return nr        
      
def reset_spacecraft():
  global screen_x
  global bullets
  global explosions
  global lasers
  init_spacecraft()
  screen_x = 0
  reset_mantis()
  reset_mutants()
  bullets = []
  explosions = []
  lasers = []
  
  
def spacecraft_shoots_laser():
  global lasers
  global spacecraft
  laser = Sprite()
  laser.w = 20
  laser.t = 0
  laser.x = spacecraft.x - spacecraft.dir*(8 + laser.w//2)
  if laser.x > max_planet_x/pixel_size:
    laser.x -= max_planet_x/pixel_size
  if laser.x < 0:
    laser.x += max_planet_x/pixel_size
  laser.dir = spacecraft.dir
  laser.y = spacecraft.y  
  laser.h = 2
  lasers.append(laser)
  
def get_distance(a, b):
  diff_x = abs(a.x - b.x)
  if diff_x > (max_planet_x/pixel_size)/2:
    diff_x = max_planet_x/pixel_size - diff_x
  diff_y = abs(a.y - b.y)
  return diff_x + diff_y
  
def move_from_to_x(a, b):
  diff_x_1 = b.x - a.x
  diff_x_2 = b.x - a.x + max_planet_x/pixel_size
  if abs(diff_x_1) < abs(diff_x_2):
    return diff_x_1
  return diff_x_2
  
def move_from_to_y(a, b):
  return b.y - a.y
    
def clamp(x, a, b):
  if x < a:
    return a
  if x > b:
    return b
  return x    
  
def make_bullet(x, y):
  global bullets
  global bullet_speed
  bullet = Sprite()
  bullet.x = x
  bullet.y = y
  bullet.w = 3
  bullet.h = 3
  bullet.vx = random.randint(-100,100)
  bullet.vy = random.randint(-100,100)
  le = math.sqrt(bullet.vx*bullet.vx + bullet.vy*bullet.vy)
  bullet.vx *= bullet_speed/le
  bullet.vy *= bullet_speed/le
  bullets.append(bullet)
    
def update_mantis():
  global mantis
  global mutants
  global humans
  global mantis_speed
  for i in range(0, len(mantis)):
    if mantis[i].alive != 0:
      if mantis[i].state == 0:
        if random.randint(0, 100) == 0:
          make_bullet(mantis[i].x, mantis[i].y)
        j = -1
        if (humans[i].alive!=0) and (humans[i].state == 0):
          j = i
        if j == -1:
          px = move_from_to_x(mantis[i], spacecraft)
          py = move_from_to_y(mantis[i], spacecraft)
          if abs(px)>abs(py):
            py = 0
          else:
            px = 0           
          mantis[i].x += clamp(px,-mantis_speed,mantis_speed)
          mantis[i].y += clamp(py,-mantis_speed,mantis_speed)
        else:
          px = move_from_to_x(mantis[i], humans[j])
          py = move_from_to_y(mantis[i], humans[j])
          if abs(px)>abs(py):
            py = 0
          else:
            px = 0          
          mantis[i].x += clamp(px, -mantis_speed, mantis_speed)
          mantis[i].y += clamp(py, -mantis_speed, mantis_speed)
        if mantis[i].x > max_planet_x/pixel_size:
          mantis[i].x -= max_planet_x/pixel_size
        if mantis[i].x < 0:
          mantis[i].x += max_planet_x/pixel_size
      else:
        mantis[i].y -= 0.1
        if mantis[i].y < 8:
          mantis[i].alive = 0
          mutant = Sprite()
          mutant.x = mantis[i].x
          mutant.y = mantis[i].y
          mutant.w = mantis[i].w
          mutant.h = mantis[i].h
          mutant.alive = 1
          mutant.state = 0
          mutants.append(mutant)
          humans[i].alive = 0
  
def update_mutants():
  global mutants
  global mutant_speed
  for i in range(0, len(mutants)):
    if mutants[i].alive != 0:
      if random.randint(0, 75) == 0:
        make_bullet(mutants[i].x, mutants[i].y)
      px = move_from_to_x(mutants[i], spacecraft)
      py = move_from_to_y(mutants[i], spacecraft)
      if abs(px)>abs(py):
        py = 0
      else:
        px = 0           
      mutants[i].x += clamp(px,-mutant_speed,mutant_speed)
      mutants[i].y += clamp(py,-mutant_speed,mutant_speed)

  
  
def update_humans():
  global humans
  global mantis
  global spacecraft
  global score
  for i in range(0, len(humans)):
    if humans[i].state==1:    
      humans[i].x = mantis[i].x
      humans[i].y = mantis[i].y+4
    if humans[i].state==2:
      humans[i].y += 0.3
      if (humans[i].y > HEIGHT/pixel_size-8):
        humans[i].alive = 0
        humans[i].state = 0
        add_explosion(humans[i].x, humans[i].y)
    if humans[i].state==3:    
      humans[i].x = spacecraft.x
      humans[i].y = spacecraft.y+4
      if (humans[i].y > HEIGHT/pixel_size-8):
        humans[i].state = 0
        score += 500
        
def update_bullets():
  global bullets
  for i in reversed(range(0, len(bullets))):
    bullets[i].state = bullets[i].state+1    
    bullets[i].x += bullets[i].vx
    bullets[i].y += bullets[i].vy
    if bullets[i].x > max_planet_x/pixel_size:
      bullets[i].x -= max_planet_x/pixel_size
    if bullets[i].x < 0:
      bullets[i].x += max_planet_x/pixel_size
    if bullets[i].state > 200:
      bullets.pop(i)
            
def get_number_of_enemies():
  nr = get_number_of_mantis()
  nr += get_number_of_mutants()
  return nr
  
def update():
  global screen_x
  global spacecraft
  global timer
  global speed_x
  global gameover
  global space_is_pressed
  global wave
  if gameover != 0:
    return
  update_lasers()
  if keyboard.left and (spacecraft.alive!=0):
    speed_x -= 0.4
    if speed_x < -20:
      speed_x = -20
    spacecraft.dir = 1
  if keyboard.right and (spacecraft.alive!=0):
    speed_x += 0.4
    if speed_x > 20:
      speed_x = 20
    spacecraft.dir = -1
  if keyboard.up and (spacecraft.alive!=0):
    spacecraft.y = spacecraft.y - 1
    if spacecraft.y < 4:
      spacecraft.y = 4
  if keyboard.down and (spacecraft.alive!=0):
    spacecraft.y = spacecraft.y + 1
    if spacecraft.y > HEIGHT/pixel_size-4:
      spacecraft.y = HEIGHT/pixel_size-4
  if keyboard.space:    
    if space_is_pressed == 0 and spacecraft.alive != 0:
      spacecraft_shoots_laser()
    space_is_pressed = 1
  else:
    space_is_pressed = 0
  screen_x = (screen_x + speed_x)%max_planet_x   
  spacecraft.x = ((spacecraft.x*pixel_size + speed_x)%max_planet_x)/pixel_size
  if speed_x < 0:
    speed_x += min(0.1, -speed_x)
    if spacecraft.alive == 0:
      speed_x = 0
  elif speed_x > 0:    
    speed_x -= min(0.1, speed_x)
    if spacecraft.alive == 0:
      speed_x = 0
  update_mantis()
  update_mutants()
  update_humans()
  update_bullets()
  update_explosions()    
  check_collisions()
  if (spacecraft.alive == 0) and not explosions:
    if lives < 0:
      gameover = 1
    else:
      reset_spacecraft()
  timer = timer + 1      
  if (spacecraft.alive != 0) and (get_number_of_enemies() == 0):
      wave = wave + 1
      init_wave(wave)
      timer = 0     
  

def draw_humans():
  global humans
  for i in range(0, len(humans)):
    x = humans[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    if humans[i].alive != 0:
      draw_human(x, humans[i].y, humans[i].dir)
    
def draw_mantis():
  global mantis
  for i in range(0, len(mantis)):
    x = mantis[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    if mantis[i].alive != 0:
      draw_manti(x, mantis[i].y, timer)
      
def draw_mutants():
  global mutants
  for i in range(0, len(mutants)):
    x = mutants[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    if mutants[i].alive != 0:
      draw_mutant(x, mutants[i].y, timer)
         
def draw_explosions():
  global explosions
  for i in range(0, len(explosions)):
    x = explosions[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    draw_explosion(x, explosions[i].y, explosions[i].t)

def draw_lasers():
  global lasers
  for i in range(0, len(lasers)):
    x = lasers[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    draw_laser(x, lasers[i].y, lasers[i].w)

def draw_bullets():
  global bullets
  for i in range(0, len(bullets)):
    x = bullets[i].x - screen_x/pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    draw_bullet(x, bullets[i].y)



def draw():
  screen.fill('black')
  if gameover!=0:
    screen.draw.text("Game Over", center=(WIDTH//2,HEIGHT//2))
    screen.draw.text("Score: "+str(score), center=(WIDTH//2,HEIGHT//2+20))
    return    
  if timer < 100:
    screen.draw.text("Wave "+str(wave), center=(WIDTH//2,HEIGHT//2))
    return 
  screen.draw.text("Lives: "+str(max(lives, 0)), topleft=(10,10))
  screen.draw.text("Score: "+str(score), topright = (WIDTH-10,10))
  
  draw_planet()
  if spacecraft.alive != 0:
    x = spacecraft.x - screen_x / pixel_size
    if x < 0:
      x += max_planet_x/pixel_size
    draw_defender(x, spacecraft.y, spacecraft.dir)
  draw_humans()
  draw_mantis()
  draw_explosions()
  draw_lasers()
  draw_bullets()
  draw_mutants()
    
def init_game():
  build_planet()
  init_wave(wave)
  
init_game()
pgzrun.go()