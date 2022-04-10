import curses
import random
import os
global screen
def clear():
  os.system('clear')
screen = curses.initscr()
screen.keypad(True)
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, -1, curses.COLOR_BLACK)
curses.init_pair(2, -1, curses.COLOR_WHITE)
curses.init_pair(3, -1, curses.COLOR_RED)
curses.init_pair(4, -1, curses.COLOR_BLUE)
white = curses.color_pair(2)
black = curses.color_pair(1)
red = curses.color_pair(3)
blue = curses.color_pair(4)
def placeWallAndPassage(y, x, direction):
  newy = y
  newx = x
  passage = list()
  if direction == 'vertical':
    while True:
      screen.addstr(newy, newx, '  ', black)
      newy += 1
      attrs = screen.inch(newy, newx)
      isBlack = bool(attrs & black)
      if isBlack:
        break
    passage.append(random.randint(y, newy-1))
    if passage[0] % 2 == 0:
      passage[0] -= 1
    screen.addstr(passage[0], newx, '  ', white)
    if random.randint(0, 1) == 0:
      passage.append(random.randint(y, newy-1))
      if passage[1] % 2 == 0:
        passage[1] -= 1
      screen.addstr(passage[1], newx, '  ', white)
  else:
    while True:
      screen.addstr(newy, newx, '  ', black)
      newx += 2
      attrs = screen.inch(newy, newx)
      isBlack = bool(attrs & black)
      if isBlack:
        break
    passage.append(random.randint(x, newx-2))
    while True:
      if passage[0] % 2 == 0 and passage[0] % 4 != 0:
        break
      passage[0] -= 1
    screen.addstr(newy, passage[0], '  ', white)
    if random.randint(0, 1) == 0:
      passage.append(random.randint(x, newx-2))
      while True:
        if passage[1] % 2 == 0 and passage[1] % 4 != 0:
          break
        passage[1] -= 1
  return passage
def choose_orientation(width, height):
  if width < height:
    return 'horizontal'
  elif width > height:
    return 'vertical'
  else:
    if random.randint(0, 1) == 0:
      return 'vertical'
    else:
      return 'horizontal'
maxy, maxx = screen.getmaxyx()
if maxy % 2 == 0:
  maxy -= 1
while True:
  if maxx % 2 == 0 and maxx % 4 != 0:
    break
  maxx -= 1
width = maxx-4
height = maxy-2
unusablex = [5000]
unusabley = [5000]
def reset():
  for line in range(0, maxy):
    if line == 0 or line == maxy-1:
      try:
        screen.addstr(line, 0, ' '*maxx, black)
      except:
        idk = 0
    else:
      screen.addstr(line, 0, '  ', black)
      screen.addstr(line, maxx-2, '  ', black)
  for line in range(1, maxy-1):
    for char in range(2, maxx-2, 2):
      screen.addstr(line, char, '  ', white)
def divide(x, y, width, height, orientation, unusablex, unusabley):
  if width < 4 or height < 2:
    return 0
  wallx = x
  wally = y
  while True:
    if orientation == 'horizontal':
      wally = random.randint(y+1, height+y-1)
      if wally % 2 != 0:
        wally -= 1
      if not wally in unusabley:
        break
    else:
      wallx = random.randint(x+2, width+x-2)
      while True:
        if wallx % 4 == 0 and not wallx in unusablex and wallx > 0:
          break
        else:
          wallx = random.randint(x+2, width+x-2)
      break
  if orientation == 'vertical':
    unusablex = [wallx]
    unusabley = placeWallAndPassage(wally, wallx, orientation)
    newx = wallx+2
    newy = wally
    nextx = x
    nexty = wally
    newwidth = width + x - 2 - wallx
    newheight = height
    nextwidth = width - newwidth - 2
    nextheight = height
  else:
    unusabley = [wally]
    unusablex = placeWallAndPassage(wally, wallx, orientation)
    newx = wallx
    newy = wally+1
    nextx = wallx
    nexty = y
    newwidth = width
    newheight = height + y - 1 - wally
    nextwidth = width
    nextheight = height - newheight - 1
  divide(newx, newy, newwidth, newheight, choose_orientation(width, height), unusablex, unusabley)
  divide(nextx, nexty, nextwidth, nextheight, choose_orientation(nextwidth, nextheight), unusablex, unusabley)
def maze():
  divide(2, 1, width, height, choose_orientation(width, height), unusablex, unusabley)
  starty = 1
  startx = 2
  endy = maxy - 2
  endx = maxx - 4
  screen.addstr(starty, startx, '  ', white)
  screen.addstr(endy, endx, '  ', blue)
  playerx = startx
  playery = starty
  prevy, prevx = 3, 2
  curses.noecho()
  while True:
    if playerx == endx and playery == endy:
      break
    screen.addstr(playery, playerx, '  ', red)
    screen.addstr(prevy, prevx, '  ', white)
    screen.refresh()
    curses.napms(100)
    char = screen.getch()
    if char in [ord('w'), ord('a'), ord('s'), ord('d'), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
      if char in [ord('w'), curses.KEY_UP]:
        try:
          attrs = screen.inch(playery-1, playerx)
          isBlack = bool(attrs & black)
          if isBlack:
            raise ValueError
          if playery == 0:
            raise ValueError
          prevy = playery
          prevx = playerx
          playery -= 1
        except:
          bruh = 0
      elif char in [ord('a'), curses.KEY_LEFT]:
        try:
          attrs = screen.inch(playery, playerx-2)
          isBlack = bool(attrs & black)
          if isBlack:
            raise ValueError
          if playerx == 0:
            raise ValueError
          prevy = playery
          prevx = playerx
          playerx -= 2
        except:
          bruh = 0
      elif char in [ord('s'), curses.KEY_DOWN]:
        try:
          attrs = screen.inch(playery+1, playerx)
          isBlack = bool(attrs & black)
          if isBlack:
            raise ValueError
          if playery == maxy-1:
            raise ValueError
          prevy = playery
          prevx = playerx
          playery += 1
        except:
          bruh = 0
      elif char in [ord('d'), curses.KEY_RIGHT]:
        try:
          attrs = screen.inch(playery, playerx+2)
          isBlack = bool(attrs & black)
          if isBlack:
            raise ValueError
          if playerx == maxx-2:
            raise ValueError
          prevy = playery
          prevx = playerx
          playerx += 2
        except:
          bruh = 0
while True:
  reset()
  maze()
