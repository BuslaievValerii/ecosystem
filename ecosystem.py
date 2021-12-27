import numpy as np
import os
import time
from termcolor import colored

SIZE = 25

PLANT_MASS  = 1800
RABBIT_MASS = 5000


def move(field_alive, field_dead, position, position_to_move, type_org):
	field_dead[position[0]][position[1]] += 0.1 * type_org
	field_alive[position[0]][position[1]][1] -= 0.1 * type_org
	field_alive[position_to_move[0]][position_to_move[1]] = field_alive[position[0]][position[1]]
	field_alive[position[0]][position[1]] = [None, 0]
	return field_alive, field_dead


def show_field(field):
	os.system('cls')
	for i in range(SIZE):
		creatures = ""
		for j in range(SIZE):
			if field[i][j][0] == None:
				creatures += "   "
			else:
				if field[i][j][0] == 'P':
					color = 'green'
				elif field[i][j][0] == 'R':
					color = 'red'
				creatures += " "
				creatures += colored(field[i][j][0], color)
				creatures += " "
		print(creatures)


def stay(field_alive, field_dead, position):
	i, j = position[0], position[1]
	if field_alive[i][j][0] == 'P':
		field_alive[i][j][1] -= 0.01 * PLANT_MASS
		field_dead[i][j] += 0.01 * PLANT_MASS
	elif field_alive[i][j][0] == 'R':
		field_alive[i][j][1] -= 0.01 * RABBIT_MASS
		field_dead[i][j] += 0.01 * RABBIT_MASS
	elif field_alive[i][j][0] == 'F':
		field_alive[i][j][1] -= 0.01 * FOX_MASS
		field_dead[i][j] += 0.01 * FOX_MASS
	return field_alive, field_dead


def eat_dead(field_alive, field_dead, position, type_org):
	i, j = position[0], position[1]
	if type_org - field_alive[i][j][1] <= field_dead[i][j]:
		field_alive[i][j][1] = type_org
		field_dead[i][j] -= type_org - field_alive[i][j][1]
	else:
		field_alive[i][j][1] += field_dead[i][j]
		field_dead[i][j] -= field_dead[i][j]
	return field_alive, field_dead


def eat_alive(field_alive, position, position_to_eat, type_org):
	i, j = position[0], position[1]
	k, p = position_to_eat[0], position_to_eat[1]
	if type_org - field_alive[i][j][1] <= field_alive[k][p][1]:
		field_alive[i][j][1] = type_org
	else:
		field_alive[i][j][1] += field_alive[k][p][1]
	field_alive[k][p] = [None, 0]
	return field_alive


def die(field_alive, field_dead, position):
	i, j = position[0], position[1]
	field_dead[i][j] += field_alive[i][j][1]
	field_alive[i][j] = [None, 0]
	return field_alive, field_dead


def copy(field_alive, field_dead, position, position_to_copy):
	i, j = position[0], position[1]
	field_dead[i][j] += 0.1 * field_alive[i][j][1]
	field_alive[i][j][1] = (field_alive[i][j][1] - 0.1 * field_alive[i][j][1])/2
	field_alive[position_to_copy[0]][position_to_copy[1]] = field_alive[i][j]
	return field_alive, field_dead


def rabbit_sees_plant(field_alive, position):
	plant_position = None
	position_to_move = None
	for i in range(position[0]-2, position[0]+3):
		for j in range(position[1]-2, position[1]+3):
			if i >= SIZE:
				ii = i - SIZE
			else:
				ii = i
			if j >= SIZE:
				jj = j - SIZE
			else:
				jj = j
			if field_alive[ii][jj][0] == 'P':
				plant_position = (ii,jj)
	if plant_position:
		for i in range(plant_position[0]-1, plant_position[0]+2):
			for j in range(plant_position[1]-1, plant_position[1]+2):
				if i >= SIZE:
					ii = i - SIZE
				else:
					ii = i
				if j >= SIZE:
					jj = j - SIZE
				else:
					jj = j
				if field_alive[ii][jj][0] == None:
					position_to_move = (ii,jj)
	return plant_position, position_to_move


def plant_near(field_alive, position):
	plant_position = None
	for i in range(position[0]-1, position[0]+2):
		for j in range(position[1]-1, position[1]+2):
			if i >= SIZE:
				ii = i - SIZE
			else:
				ii = i
			if j >= SIZE:
				jj = j - SIZE
			else:
				jj = j
			if field_alive[ii][jj][0] == 'P':
				plant_position = (ii,jj)
	return plant_position


def clear_position_near(field_alive, position):
	clear_position = None
	for i in range(position[0]-1, position[0]+2):
		for j in range(position[1]-1, position[1]+2):
			if i >= SIZE:
				ii = i - SIZE
			else:
				ii = i
			if j >= SIZE:
				jj = j - SIZE
			else:
				jj = j
			if field_alive[ii][jj][0] == None:
				clear_position = (ii,jj)
	return clear_position


field_alive = []
field_dead = []

for i in range(SIZE):
	field_alive.append([])
	field_dead.append([])
	for j in range(SIZE):
		field_alive[i].append([None, 0])
		field_dead[i].append(2000)


field_alive[6][5] = ["R", RABBIT_MASS]
field_alive[6][7] = ["R", RABBIT_MASS]
field_alive[7][16] = ["R", RABBIT_MASS]
field_alive[13][14] = ["R", RABBIT_MASS]
field_alive[16][6] = ["R", RABBIT_MASS]

field_alive[7][10] = ["P", PLANT_MASS]
field_alive[8][10] = ["P", PLANT_MASS]
field_alive[8][11] = ["P", PLANT_MASS]
field_alive[9][9] = ["P", PLANT_MASS]
field_alive[9][10] = ["P", PLANT_MASS]
field_alive[9][11] = ["P", PLANT_MASS]
field_alive[9][12] = ["P", PLANT_MASS]
field_alive[9][13] = ["P", PLANT_MASS]
field_alive[10][9] = ["P", PLANT_MASS]
field_alive[10][10] = ["P", PLANT_MASS]
field_alive[10][11] = ["P", PLANT_MASS]
field_alive[10][12] = ["P", PLANT_MASS]
field_alive[10][13] = ["P", PLANT_MASS]
field_alive[11][9] = ["P", PLANT_MASS]
field_alive[11][10] = ["P", PLANT_MASS]
field_alive[11][11] = ["P", PLANT_MASS]
field_alive[11][12] = ["P", PLANT_MASS]
field_alive[12][12] = ["P", PLANT_MASS]

num_of_orgs = 23
iteration = 0
while (num_of_orgs > 0):
	time.sleep(1)

	show_field(field_alive)
	num_of_orgs = 0
	iteration += 1
	print(f'\n\nIteration {iteration}')

	for i in range(SIZE):
		for j in range(SIZE):
			if field_alive[i][j][0] == "R":
				num_of_orgs += 1
				if field_alive[i][j][1] >= 0.6 * RABBIT_MASS and clear_position_near(field_alive, (i,j)):
					field_alive, field_dead = copy(field_alive, field_dead, (i,j), clear_position_near(field_alive, (i,j)))
				else:
					plant_position = plant_near(field_alive, (i,j))
					if plant_position:
						field_alive = eat_alive(field_alive, (i,j), plant_position, RABBIT_MASS)
					else:
						plant_position, position_to_move = rabbit_sees_plant(field_alive, (i,j))
						if position_to_move:
							field_alive, field_dead = move(field_alive, field_dead, (i,j), position_to_move, RABBIT_MASS)
						else:
							field_alive, field_dead = stay(field_alive, field_dead, (i,j))
				if field_alive[i][j][1] < 0.1 * RABBIT_MASS:
					field_alive, field_dead = die(field_alive, field_dead, (i,j))

	for i in range(SIZE):
		for j in range(SIZE):
			if field_alive[i][j][0] == "P":
				num_of_orgs += 1
				if field_alive[i][j][1] >= 0.6 * PLANT_MASS and clear_position_near(field_alive, (i,j)):
					field_alive, field_dead = copy(field_alive, field_dead, (i,j), clear_position_near(field_alive, (i,j)))
				else:
					field_alive, field_dead = eat_dead(field_alive, field_dead, (i,j), PLANT_MASS)
				if field_alive[i][j][1] < 0.1 * PLANT_MASS:
					field_alive, field_dead = die(field_alive, field_dead, (i,j))
