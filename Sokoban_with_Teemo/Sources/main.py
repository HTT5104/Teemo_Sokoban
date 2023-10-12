import numpy as np
import os
import time
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar
import bestfs
from memory_profiler import profile


''' TIME OUT FOR ALL ALGORITHM'''
TIME_OUT = 1800
''' GET THE TESTCASES AND CHECKPOINTS PATH FOLDERS '''
path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'

''' TRAVERSE TESTCASE FILES AND RETURN A SET OF BOARD '''
def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}\{file}"
            board = get_board(file_path)
            # print(file)
            list_boards.append(board)
    return list_boards

''' TRAVERSE CHECKPOINT FILES AND RETURN A SET OF CHECKPOINT '''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}\{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

''' FORMAT THE INPUT TESTCASE TXT FILE '''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

''' FORMAT THE INPUT CHECKPOINT TXT FILE '''
def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

''' READ A SINGLE TESTCASE TXT FILE '''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

''' READ A SINGLE CHECKPOINT TXT FILE '''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

'''DECLARE MAPS AND CHECK POINTS'''
maps = get_boards()
check_points = get_check_points()


'''UI'''
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
'''
GET SOME ASSETS
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')
'''
RENDER THE MAP FOR GAMEPLAY
'''
def renderMap(board):
	width = len(board[0])
	height = len(board)
	indent = (800 - width * 50) / 2.0
	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 50 + indent, i * 50 + 250))
			if board[i][j] == '#':
				screen.blit(wall, (j * 50 + indent, i * 50 + 250))
			if board[i][j] == '$':
				screen.blit(box, (j * 50 + indent, i * 50 + 250))
			if board[i][j] == '%':
				screen.blit(point, (j * 50 + indent, i * 50 + 250))
			if board[i][j] == '@':
				screen.blit(player, (j * 50 + indent, i * 50 + 250))
'''
VARIABLES INITIALIZATIONS
'''
#Map level
mapNumber = 0
#Algorithm to solve the game
algorithm = "Breadth First Search"
#Your scene states, including: 
#init for choosing your map and algorithm
#loading for displaying "loading scene"
#executing for solving problem
#playing for displaying the game
sceneState = "init"
loading = False

''' SOKOBAN FUNCTION '''
def sokoban():
	running = True
	global sceneState
	global loading
	global algorithm
	global list_board
	global mapNumber
	stateLenght = 0
	currentState = 0
	found = True

	while running:
		screen.blit(init_background, (0, 0))
		if sceneState == "init":
			#Choose map and display
			initGame(maps[mapNumber])

		if sceneState == "executing":
			#Choose map
			list_check_point = check_points[mapNumber]

			#Choose between BFS or Hill Climbing
			if algorithm == "Breadth First Search":
				print("BFS")
				list_board = bfs.BFS_search(maps[mapNumber], list_check_point)
			elif algorithm == "A Star Search":
				print("AStar")
				list_board = astar.AStart_Search(maps[mapNumber], list_check_point)
			else:
				print("BestFS")
				list_board = bestfs.BestFS_Search(maps[mapNumber], list_check_point)
			if len(list_board) > 0:
				sceneState = "playing"
				stateLenght = len(list_board[0])
				currentState = 0
			else:
				sceneState = "end"
				found = False
		if sceneState == "loading":
			loadingGame()
			sceneState = "executing"
		if sceneState == "end":
			if found:
				foundGame(list_board[0][stateLenght - 1])
			else:
				notfoundGame()
		if sceneState == "playing":
			clock.tick(2)
			renderMap(list_board[0][currentState])
			currentState = currentState + 1
			if currentState == stateLenght:
				sceneState = "end"
				found = True
		#Check event when you press key board
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				
				#Press arrow key board to change level map
				if event.key == pygame.K_RIGHT and sceneState == "init":
					if mapNumber < len(maps) - 1:
						mapNumber = mapNumber + 1
				if event.key == pygame.K_LEFT and sceneState == "init":
					if mapNumber > 0:
						mapNumber = mapNumber - 1
				#Press ENTER key board to select level map and algorithm
				if event.key == pygame.K_RETURN:
					if sceneState == "init":
						sceneState = "loading"
					if sceneState == "end":
						sceneState = "init"
				#Press SPACE key board to switch algorithm
				if event.key == pygame.K_SPACE and sceneState == "init":
					if algorithm == "Breadth First Search":
						algorithm = "A Star Search"
					elif algorithm == "A Star Search":
						algorithm = "Best First Search"
					else:
						algorithm = "Breadth First Search"
		pygame.display.flip()
	pygame.quit()

''' DISPLAY MAIN SCENE '''
#DISPLAY INITIAL SCENE
def initGame(map):
	titleSize = pygame.font.Font('gameFont.ttf', 60)
	titleText = titleSize.render('Sokoban with Teemo', True, WHITE)
	titleRect = titleText.get_rect(center=(400, 80))
	screen.blit(titleText, titleRect)

	desSize = pygame.font.Font('gameFont.ttf', 20)
	desText = desSize.render('Now, select your map!!!', True, WHITE)
	desRect = desText.get_rect(center=(400, 140))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font('gameFont.ttf', 30)
	mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
	mapRect = mapText.get_rect(center=(400, 200))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (246, 188))
	screen.blit(arrow_right, (520, 188))

	algorithmSize = pygame.font.Font('gameFont.ttf', 30)
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(400, 750))
	screen.blit(algorithmText, algorithmRect)
	renderMap(map)

''' LOADING SCENE '''
#DISPLAY LOADING SCENE
def loadingGame():
	screen.blit(loading_background, (0, 0))

	fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = fontLoading_1.render('SHHHHHHH!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(400, 700))
	screen.blit(text_1, text_rect_1)

	fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = fontLoading_2.render('Stay right here, Captain Teemo on duty!', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(400, 750))
	screen.blit(text_2, text_rect_2)

def foundGame(map):
	screen.blit(found_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Ace! You have cleared all your enemies!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(400, 200))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(400, 750))
	screen.blit(text_2, text_rect_2)

	renderMap(map)

def notfoundGame():
	screen.blit(notfound_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = font_1.render('Oh no, Teemo was lost in jungle', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(400, 50))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(400, 750))
	screen.blit(text_2, text_rect_2)

	
@profile
def main():
	sokoban()

if __name__ == "__main__":
	main()
