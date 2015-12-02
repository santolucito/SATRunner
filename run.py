
from threading import Thread

import os
import subprocess
import time
import re
import pygame

##
## collect the test suite
##
programs = []
programs += [each for each in os.listdir("executables")]

# each program has a list of ints
performance = [[] for each in programs]

tests = []
tests += [each for each in os.listdir("tests")]

current_test = ""

##
## start the graphics
##

def displaying():
  t_to_d = lambda xs : map(lambda x : font.render(x, True, BLACK), xs)

  # Initialize the game engine
  pygame.init()
 
  # Define some colors
  BLACK = (0, 0, 0)
  WHITE = (255, 255, 255)
  GREEN = (0, 255, 0)
  RED = (255, 0, 0)

  # Select the font to use, size, bold, italics
  font = pygame.font.SysFont('Times New Roman', 25, True, False)
 
  # Set the height and width of the screen
  size = (800, 500)
  screen = pygame.display.set_mode(size)
 
  pygame.display.set_caption("SAT Competetion")
 
  # Loop until the user clicks the close button.
  done = False
  clock = pygame.time.Clock()
 
  # Loop as long as done == False
  while not done:
 
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
 
    # Clear the screen and set the screen background
    screen.fill(WHITE)
 
    screen.blit(font.render("Running test: "+str(current_test), True, BLACK), [50, 20])
    # Render the text
    programs_text = t_to_d(programs) 
    # Put the image of the text on the screen at 250x250
    for i in range(0,len( programs_text)):
      screen.blit(programs_text[i], [25, 50+(i*25)])
      
      offset = 0
      for j in range(0,len(performance[i])):
        if performance[i][j] == -1:
          c = RED
          size = 5
        else:
          c = GREEN 
          size = 1/performance[i][j]
        offset+=size
        pygame.draw.line(screen, c, [175+offset, 50+(i*25)+15], [175+offset+size, 50+(i*25)+15], 15)

    
    # Draw a rectangle
    #pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
 
    pygame.display.flip()
    clock.tick(60)
  pygame.quit()

Thread( target=displaying, args=()).start()

##
## run the tests
##
for t in tests:
  current_test = t
  for x in range(0,len(programs)):
    start = time.time()
    res = subprocess.check_output("executables/"+programs[x]+" "+t,shell=True)
    if (res == "sat"): 
      performance[x] += [time.time()-start]
    else:
      performance[x] += [-1]
    print res
    time.sleep (1)

