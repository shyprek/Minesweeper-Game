import pygame
import math
import random
import time
#Minesweeper
#Outline: 
"""1. Initialize/set up window.
   2. Create grid/cells (using 2D List to randomly initialize the mines).
   3. Draw grid.
   4. Code a way to take in mouse clicks for input.
   5. Create timer, print it when game starts.
   6. The first cell left clicked reveals a large area of the grid with numbers showing neighboring mines.
   7. Afterwards, check if the cell left-clicked is a mine; if so, terminate game. If not, reveal the cell's number of mines surrounding it.
   8. If cell is right-clicked, draw a "flag" to show possible mine location.
   9. When all possible non-mine cells are revealed, end the game and print a message for losing or winning."""

pygame.init()
screen = pygame.display.set_mode((800, 800))
screen.fill((255, 250, 255))

class Tile:
  def __init__(self, x, y, type, side, number):
    self.x = x
    self.y = y
    self.type = type
    self.side = side
    self.number = number
    self.selected = False
    self.flag = False
  def get_X(self):
    return self.x

  def set_X(self, x):
    self.x = x

  def get_Y(self):
    return self.y

  def set_Y(self, y):
    self.y = y

  def get_type(self):
    return self.type

  def set_type(self, type):
    self.type = type

  def get_side(self):
    return self.side

  def set_side(self, side):
    self.side = side

  def get_number(self):
    return self.number

  def set_number(self, number):
    self.number = number
    
# bomb tile:
BOMB = "bomb"
# tile adjacent to >= 1 mine:
SPEC = "special"
# tile not adjacent to any mines:
NONSPEC = "nonspecial"
board = []
for i in range(0, 10):
  row = []
  for j in range(0, 10):
    tile = Tile(i, j, NONSPEC, 15, 0)
    row.append(tile)
  board.append(row)

# placing the bombs:
bombs = 10
def randomize(list):
  global bombs
  b_create = 0
  uni_numbers = set()
  while b_create < bombs:
    cell = random.randint(0, 99)
    if cell in uni_numbers:
      continue
    else:
      uni_numbers.add(cell)
      left_dig = cell // 10
      right_dig = cell % 10
      list[left_dig][right_dig].type = BOMB
      b_create += 1


def out_bounds(x, y):
  return x < 0 or x > 9 or y < 0 or y > 9

# organizing and classifying remaining tiles
def identity(list):
  for i in range(0, 10):
    for j in range(0, 10):
      for k in range(-1, 2):
        for l in range(-1, 2):
          if out_bounds(i + k, j + l) or list[i][j].type == BOMB:
            continue
          elif list[k + i][l + j].type == BOMB:
            list[i][j].number += 1
      if list[i][j].number > 0 and list[i][j].type != BOMB:
        list[i][j].type = SPEC
      elif list[i][j].type != BOMB:
        list[i][j].type = NONSPEC

# for revealing multiple tiles when a NONSPEC tile is hit
def reveal(list, ind1, ind2):
  for i in range(-1, 2):
    for j in range(-1, 2):
      if out_bounds(ind1 + i, ind2 + j):
        continue
      elif list[ind1 + i][ind2 + j].type != BOMB:
        list[ind1 + i][ind2 + j].selected = True

#drawing function
def draw():
  color = (23, 155, 67)
  for i in range(0, 10):
    for j in range(0, 10):
      pygame.draw.rect(screen, color, pygame.Rect(30 + 20 * j , 30 + 20 * i, board[i][j].side, board[i][j].side))
      if board[i][j].selected and board[i][j].type != BOMB:
        draw_text(str(board[i][j].number), 35 + 20 * j, 30 + 20 * i)
      elif board[i][j].selected and board[i][j].type == BOMB:
        ocolor1 = (255, 0, 0)
        pygame.draw.rect(screen, ocolor1, pygame.Rect(30 + 20 * j , 30 + 20 * i, board[i][j].side, board[i][j].side))
      if board[i][j].flag:
        ocolor = (0, 0, 255)
        pygame.draw.rect(screen, ocolor, pygame.Rect(30 + 20 * j , 30 + 20 * i, board[i][j].side, board[i][j].side))
      pygame.display.flip()

# for mapping coordinates of mouseclick to the right tile
def findTile(x, y):
  ind1 = (x - 30) // 20
  ind2 = (y - 30) // 20
  return (ind1, ind2)

def winGame(list):
  global bombs
  count = 0
  for i in range(10):
    for j in range(10):
      if list[i][j].selected:
        count += 1
  if count == 100 - bombs:
    draw_text("You Won!", 10, 10)
    time.sleep(60)
    quit_game()

run = True

#quit function
def quit_game():
  global run
  run = False

#render text
def draw_text(txt, x, y):
  font = pygame.font.SysFont("FreeSans.ttf", 20)
  text = font.render(txt, True, (0, 0, 0))
  screen.blit(text, (x, y))
  pygame.display.flip()

randomize(board)
identity(board)

clock = pygame.time.Clock()
while run:
  draw()
  winGame(board)
  ev = pygame.event.get()
  for event in ev:
    if event.type == pygame.MOUSEBUTTONUP:
      x, y = pygame.mouse.get_pos()
      j , i = findTile(x, y)
      print(x, y, j, i)
      print(board[i][j].x, board[i][j].y)
      if event.button == 1:
        if (board[i][j].type == BOMB):
          draw_text("X", j * 20 + 35, i * 20 + 30)
          draw_text("You Lost", 10, 10)
          time.sleep(60)
          quit_game()
        elif (board[i][j].type == SPEC):
          board[i][j].selected = True
        elif (board[i][j].type == NONSPEC):
          board[i][j].selected = True
          reveal(board, i, j)
      elif event.button == 3:
        board[i][j].flag = True
  clock.tick(30)

