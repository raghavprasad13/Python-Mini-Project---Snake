import SimpleGUICS2Pygame.simpleguics2pygame as sg 
import SimpleGUICS2Pygame.simplegui_lib_draw as draw
import pygame
import random

LENGTH = 500  # length of playing space
HEIGHT = 500  # height of playing space
RANDOM_POS_X = random.randint(0, 25)*20   # initial x-coordinate of head of the snake
RANDOM_POS_Y = random.randint(0, 25)*20   # initial y-coordinate of head of the snake
X_VELOCITY = 20 # the x and y velocities must be 20/-20 because of the size of the segments of the snake chosen i.e. 20*20 squares
Y_VELOCITY = 0
global snake_speed
global input_given  #Variable to check if the difficulty is specified(enable's /disable's the start button)
input_given=False
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
	
	def wall_collision(self):
		global input_given
		if(self.head.x_pos==0 or self.head.y_pos==500 or self.head.x_pos==500 or self.head.y_pos==0):
			frame.set_draw_handler(game_over)
			input_given=False			#Used to disable the Start button but doesn't affect the Restart button
		'''
		if(self.head.x_pos==500):         	Incomplete looping back conditions
			self.head.x_pos=20	
		if(self.head.x_pos==0):
			self.head.x_pos=500
		if(self.head.y_pos==500):
			self.head.y_pos=20	
		if(self.head.y_pos==0):
			self.head.y_pos=500													
		'''

snake = Snake()



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

	# lines 89-94: deactivates all other keys except arrow keys

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

		snake.wall_collision()                  #WallCollision calls game_over when the condition is satisfied

def button_Start():
	global input_given					#Only works if the user inputs a difficulty
	if(input_given):
		snake.__init__()                             	#Reset's the object snake 
		snake.addSegment()				#Starts off with the initial conditions
		snake.addSegment()
		snake.addSegment()
		snake.head.x_pos=random.randint(0, 25)*20
		snake.head.y_pos=random.randint(0, 25)*20
		frame.set_draw_handler(draw_play_space)	
def button_Restart():
	snake.__init__()                             	#Use's the difficulty previously given 
	snake.addSegment()				
	snake.addSegment()
	snake.addSegment()
	snake.head.x_pos=random.randint(0, 25)*20
	snake.head.y_pos=random.randint(0, 25)*20
	frame.set_draw_handler(draw_play_space)
		
def canvas_Menu(canvas):				#Temporary GameOver screen
	canvas.draw_text('Snake Game', (140, 40), 46, 'Red')
	canvas.draw_text('Instructions', (40, 140), 36, 'Green')		

def input_handler(int_input):                         #Function to input difficulty
	global snake_speed
	global input_given
	snake_speed=int(int_input)*10
	input_given=True			#Since input is given Start button is enabled

def game_over(canvas):						#Temporary GameOver screen
	canvas.draw_text('Game Over', (140, 40), 46, 'Red')
	canvas.draw_text('Score', (140, 140), 26, 'Blue')

frame = sg.create_frame("Snake", LENGTH, HEIGHT)
frame.set_keydown_handler(keydown_handler)
StartGame = frame.add_button("Start", button_Start)
RestartGame = frame.add_button("Restart", button_Restart)
frame.set_draw_handler(canvas_Menu)		
inp = frame.add_input("Difficulty from 1-10", input_handler,50)       #Changes the framerate and hence the speed of the snake
frame.start()






