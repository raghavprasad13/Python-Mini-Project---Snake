import SimpleGUICS2Pygame.simpleguics2pygame as sg 
import SimpleGUICS2Pygame.simplegui_lib_draw as draw
import SimpleGUICS2Pygame.simplegui_lib_loader as Loader
import pygame
import random
import time
import sys

LENGTH = 500  # length of playing space
HEIGHT = 500  # height of playing space

X_VELOCITY = 20 # the x and y velocities must be 20/-20 because of the size of the segments of the snake chosen i.e. 20*20 squares
Y_VELOCITY = 0

global snake_speed,score
score=0

displayed = True
timer_interval = 500

start_button_disabled = False	# initially we will want start button to be enabled
restart_button_disabled = True	# initially we will want the restart button to be disabled
								# since "restarting" the game for the first time is illogical

class Segment(object):
	def __init__(self, x_pos, y_pos, x_vel = 0, y_vel = 0):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.x_vel = x_vel
		self.y_vel = y_vel

		''' prev_x_pos and prev_y_pos are going to store te coordinates of
			the last occupied position of a segment before it moves ahead.
			This will be used by the segment behind it to enable it to follow
			the segment in front of it '''

		self.prev_x_pos = x_pos 
		self.prev_y_pos = y_pos

		''' ahead is an instance variable which will be used to refer 
			to the segment of the snake directly in front of the segment
			in question '''

		self.ahead = None	



class Snake(object):
	def __init__(self):
		RANDOM_POS_X = random.randint(10, 15)*20   # initial x-coordinate of head of the snake
		RANDOM_POS_Y = random.randint(10, 15)*20   # initial y-coordinate of head of the snake

		self.head = self.tail = Segment(RANDOM_POS_X, RANDOM_POS_Y, X_VELOCITY, Y_VELOCITY)
		self.segments = []	# will store all the segments of the snake
		self.head.ahead = self.tail.ahead = None

	def addSegment(self):
		segment = Segment(self.tail.x_pos-20, self.tail.y_pos)	# currently adds a segment of the snake assuming its moving rightward
																# will need to be modified

		if self.head == self.tail:
			self.tail = segment
			self.tail.ahead = self.head

		else:
			temp = self.tail
			self.tail = segment
			self.tail.ahead = temp

		self.segments.append(self.tail)		# note use of .append() :P
		self.tail.x_vel = self.tail.ahead.x_vel 	# new segment added is initialized with velocity equal
		self.tail.y_vel = self.tail.ahead.y_vel 	# to that of the segment directly in front of it
	
	def collision(self):
		global start_button_disabled,wall_check
		if(wall_check==0):
			if(self.head.x_pos==-20 or self.head.y_pos==500 or self.head.x_pos==500 or self.head.y_pos==-20):
				time.sleep(0.2)
				frame.set_draw_handler(game_over)
				start_button_disabled = False			#Used to disable the Start button but doesn't affect the Restart button
				restart_button_disabled = False
				collision_sound_effect.play()
				read_highscores()        #Creates scores_list
				CheckHighscore(score)    #Compares score with scores_list
	
				return
		else:
			if(self.head.x_pos==500):         	#Looping back conditions for the boundary
				self.head.x_pos=20	
			if(self.head.x_pos==0):
				self.head.x_pos=500
			if(self.head.y_pos==500):
				self.head.y_pos=20	
			if(self.head.y_pos==0):
				self.head.y_pos=500													
		

		# condition to check for self collision
		for segment in self.segments:
			if (self.head.x_pos == segment.x_pos) and (self.head.y_pos == segment.y_pos):
				frame.set_draw_handler(game_over)
				start_button_disabled = False
				restart_button_disabled = False
				collision_sound_effect.play()				
				read_highscores()			#Creates scores_list
				CheckHighscore(score)		#Compares score with scores_list
				return

snake = Snake()

class Fruit(object):
	def __init__(self,x_pos=20,y_pos=20):
		self.x_pos=x_pos
		self.y_pos=y_pos

	def update_pos(self,x,y):                   # this updates the position of the fruit each time something wierd happens
		self.x_pos=x
		self.y_pos=y

	

fruit=Fruit()


clock = pygame.time.Clock()		
''' clock will be used to control the frame rate of the game
	i.e. the speed of the snake (and in fact the entire game) '''


def keydown_handler(key):
	
	global snake
	activate_updown = True		# by default up/down controls should be active since initial direction of snake is rightward
	activate_leftright = False	# by default left/right should be deactivated because of reason stated above

	x_vel = snake.head.x_vel
	y_vel = snake.head.y_vel


	if x_vel == 0:
		activate_updown = False
		activate_leftright = True
		

	if y_vel == 0:
		activate_leftright = False
		activate_updown = True
		
	allowed_keystrokes = ["left", "right", "up", "down"]

	accepted_keys = [sg.KEY_MAP[x] for x in allowed_keystrokes]

	if key not in accepted_keys:
		return


	if activate_updown:
		if key == sg.KEY_MAP["up"]:
			snake.head.y_vel = -abs(snake.head.x_vel)


		if key == sg.KEY_MAP["down"]:
			snake.head.y_vel = abs(snake.head.x_vel)

		if key == sg.KEY_MAP["left"]:
			return

		if key == sg.KEY_MAP["right"]:
			return

		snake.head.x_vel = 0
		return

	if activate_leftright:
		if key == sg.KEY_MAP["left"]:
			snake.head.x_vel = -abs(snake.head.y_vel)

		if key == sg.KEY_MAP["right"]:
			snake.head.x_vel = abs(snake.head.y_vel)

		if key == sg.KEY_MAP["up"]:
			return

		if key == sg.KEY_MAP["down"]:
			return

		snake.head.y_vel = 0
		return 




def draw_play_space(canvas):

	global snake
	global snake_speed

	for i in range(25):		# merely draws the red grid. Temporary and for visual ref of dev only. 
							#Not to be included in finalized project

		canvas.draw_line((((i+1)*LENGTH)/25, 0), (((i+1)*LENGTH)/25, HEIGHT), 1, "Red")
		canvas.draw_line((0, ((i+1)*HEIGHT)/25), (LENGTH, ((i+1)*HEIGHT)/25), 1, "Red")

	snake.head.prev_x_pos = snake.head.x_pos
	snake.head.prev_y_pos = snake.head.y_pos

	snake.head.x_pos += snake.head.x_vel
	snake.head.y_pos += snake.head.y_vel

	draw.draw_rect(canvas, [snake.head.x_pos, snake.head.y_pos], [20, 20], 1, "Red", "Green")
	if displayed:
		draw.draw_rect(canvas,[fruit.x_pos,fruit.y_pos],[20,20],1,"Red","Red")
	
	for segment in snake.segments:

		if segment is snake.tail:
			segment.x_pos = segment.ahead.prev_x_pos
			segment.y_pos = segment.ahead.prev_y_pos

			draw.draw_rect(canvas, [segment.x_pos, segment.y_pos], [20, 20], 1, "Red", "Yellow")

		else:
			segment.prev_x_pos = segment.x_pos
			segment.prev_y_pos = segment.y_pos

			segment.x_pos = segment.ahead.prev_x_pos
			segment.y_pos = segment.ahead.prev_y_pos

			draw.draw_rect(canvas, [segment.x_pos, segment.y_pos], [20, 20], 1, "Red", "Blue")

		

	clock.tick(snake_speed)	# this is where the frame rate of the game is being controlled


	def check(x_pos, y_pos, segments): # ensures that the fruit does not appear on the snake

	    for segment in segments:
	        if (x_pos == segment.x_pos) and (y_pos == segment.y_pos):
	            return False

	    return True

	x_pos = random.randint(0, 24)*20
	y_pos = random.randint(0, 24)*20

	while not check(x_pos, y_pos, snake.segments):
	    x_pos = random.randint(0, 24)*20
	    y_pos = random.randint(0, 24)*20

	if fruit.x_pos==snake.head.x_pos and fruit.y_pos==snake.head.y_pos:
	    global score
	    score=score+10*(int(snake_speed/3))		#Updates score based on snake speed (Each difficulty corresponds to 10 points)
	    eating_sound_effect.play()    # adds sound 
	    fruit.update_pos(x_pos,y_pos) #updates the position of the fruit each time the snake eats it
	    snake.addSegment()

			
	snake.collision()                  # WallCollision calls game_over when the condition is satisfied


def button_Start():
	global start_button_disabled, snake_speed, restart_button_disabled,score
	score=0

	if not start_button_disabled:
		snake.__init__()                             	# Resets the object snake 
		snake.addSegment()				# Starts off with the initial conditions
		snake.addSegment()
		snake.addSegment()
		# snake.head.x_pos=random.randint(0, 25)*20
		# snake.head.y_pos=random.randint(0, 25)*20

		try:
			snake_speed = int(inp.get_text())*3
		except ValueError:
			inp.set_text("NaN")
			return

		if (int(inp.get_text()) < 1) or (int(inp.get_text()) > 10):
			inp.set_text("Invalid")
			return

		restart_button_disabled = False
		start_button_disabled = True

		frame.set_draw_handler(draw_play_space)	

def button_Restart():
	global score
	score=0
	if not restart_button_disabled:
		snake.__init__()                             	# Uses the difficulty previously given 
		snake.addSegment()				
		snake.addSegment()
		snake.addSegment()
		# snake.head.x_pos=random.randint(0, 25)*20			<-- was causing the teleportation error
		# snake.head.y_pos=random.randint(0, 25)*20			<-- was causing the teleportation error
		frame.set_draw_handler(draw_play_space)
		
def canvas_Menu(canvas):			#HomeScreen
	canvas.draw_text('Snake Game', (140, 40), 46, 'Red')
	canvas.draw_text('Instructions', (40, 140), 36, 'Green')
	canvas.draw_text(" Don't run the snake into the wall, or his own tail: you die.",(40,200),19,'Blue') #Instructions
	canvas.draw_text(" Eat the red apples to gain points.  ",(40,240),19,'Blue')
	canvas.draw_text(" Your score depends on the Difficulty  ",(40,280),19,'Blue')
def input_handler(int_input):                         #Function to input difficulty
	pass


def button_HighScoreScreen():		#Highscore screen
	read_highscores()
	frame.set_draw_handler(canvas_HighScoreScreen)
	
def read_highscores():   #Reads the highscore file
	global scores_list        #Stores the previous highscores
	scores_list=[]
	highscore_text=open("Highscores.txt","r")
	with highscore_text as file:
	    scores_list = [line.strip() for line in file]  #Reads the first 10 lines

def canvas_HighScoreScreen(canvas):                #Prints Highscore.txt
	global scores_list
	i=1
	j=80
	canvas.draw_text("ScoreBoard",(40,40),29,'Red')
	for elements in scores_list:             #Prints the scores
		canvas.draw_text(str(i)+")   "+str(elements),(40,j),19,'Green')
		i=i+1
		j=j+40
def CheckHighscore(score):
	global scores_list
	highscore_text=open("Highscores.txt","w+")
	for element in scores_list:
		if int(score)>int(element):                 # Checks if final score is greater than current highscores
			                 		                    
			highscore_text.write(str(score)+'\n')		#Shift's each element down by one
			score=element		                        #if the User's score is greater than the previous high scores
		else:
			highscore_text.write(str(element)+'\n')

      
def timer_handler():
    global displayed
    displayed = not displayed


frame = sg.create_frame("Snake", LENGTH, HEIGHT)
frame.set_keydown_handler(keydown_handler)

eating_sound_effect = sg.load_sound('http://rpg.hamsterrepublic.com/wiki-images/7/73/Powerup.ogg')    #To be called when snake collides with an apple
collision_sound_effect = sg.load_sound('http://rpg.hamsterrepublic.com/wiki-images/3/3b/EnemyDeath.ogg') #To be called when snake collides with walls/itself

inp = frame.add_input("Difficulty from 1-10", input_handler,60)       #Changes the framerate and hence the speed of the snake

def game_over(canvas):						#GameOver screen
	global score
	
	canvas.draw_text('Game Over', (140, 40), 46, 'Red')
	canvas.draw_text('Score :'+str(score), (140, 140), 26, 'Blue')	
def button_quit():
	timer.stop()			#Ends the timer thread(Was causing the exit issue)
	exit()					#Exits from the script
def button_walls():
	global wall_check
	if(Walls_State.get_text()=="Walls: Enabled"):
		Walls_State.set_text("Walls: Disabled")
		wall_check=1                          #Wall_Check is used in collision() to either eneable/disable snake-wall collision
	else:
		Walls_State.set_text("Walls: Enabled")
		wall_check=0
StartGame = frame.add_button("Start", button_Start)
RestartGame = frame.add_button("Restart", button_Restart)

frame.set_draw_handler(canvas_Menu)
read_highscores()        #Initially reads the highscore file

global wall_check
wall_check=0
Walls_State = frame.add_button("Walls: Enabled", button_walls)      #Walls enabled initially
HighScore = frame.add_button("Highscores",button_HighScoreScreen)


Quit = frame.add_button("Quit",button_quit)


frame.set_draw_handler(canvas_Menu)		

timer = sg.create_timer(timer_interval, timer_handler)

timer.start()

frame.start()






