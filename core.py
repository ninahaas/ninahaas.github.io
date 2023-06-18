import itertools
from collections import namedtuple

N = 19
NN = N ** 2
BLACK = 'B'
WHITE = 'W'
EMPTY = '_'

def flatten(p):
	return N * p[0] + p[1]

def unflatten(fp):
	return divmod(fp, N)

def switch_color(color):
	if color == BLACK:
		return WHITE
	elif color == WHITE:
		return BLACK
	else:
		return EMPTY

def get_neighbors(fp):
	x, y = unflatten(fp)
	neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
	neighbors_in_bounds = []

	#only keep neighbors in bounds
	for p in neighbors:
		if 0 <= p[0] < N and 0 <= p[1] < N:
			neighbors_in_bounds.append(flatten(p))
	return neighbors_in_bounds

def place_stone(board, fp, color):
	board[fp] = color
	return board

def bulk_place_stones(board, fps, color):
	for fp in fps:
		board[fp] = color
		#print(fp)
	return board

NEIGHBORS = [get_neighbors(fp) for fp in range(NN)]

def check_ko_color(board, fp):
	color = board[NEIGHBORS[fp][0]]
	for np in NEIGHBORS[fp]:
		if board[np] != color:
			return None
	return color


def find_reached(board, fp):
	color = board[fp]
	frontier = [fp]
	reached = []
	chain = []
	while frontier:
		current_fp = frontier.pop()
		chain.append(current_fp)
		for np in NEIGHBORS[current_fp]:
			if board[np] == color and np not in chain:
				frontier.append(np)
			elif board[np] != color:
				reached.append(np)
	return reached, chain

def check_if_captured(board, fp):
	reached, chain = find_reached(board, fp)
	print(reached, chain)
	if not any(board[rp] == EMPTY for rp in reached):
		board = bulk_place_stones(board, chain, EMPTY)
		return board, chain
	else:
		return board, []


class Board():
 	def __init__(self):
 		self.board = [EMPTY] * NN
 		self.ko = None

 	def print_board(self):
 		for i in range(N):
 			print(self.board[0 + (i*N) : (N-1) + (i*N)])
 		print('')

 	def play_move(self, p, color):
 		fp = flatten(p)
 		# check if position is empty
 		if self.board[fp] != EMPTY:
 			print(p, 'ILLEGAL: POSITION TAKEN')
 			return
 		# check if ko
 		if self.ko == fp:
 			print(p, 'ILLEGAL: KO')
 			return

 		# get possible ko color
 		possible_ko_color = check_ko_color(self.board, fp)

 		# place stone
 		new_board = self.board
 		new_board = place_stone(new_board, fp, color)

 		# find neighbors
 		my_neighbors = []
 		enemy_neighbors = []
 		enemy_color = switch_color(color)
 		for np in NEIGHBORS[fp]:
 			if new_board[np] == color:
 				my_neighbors.append(np)
 			elif new_board[np] == enemy_color:
 				enemy_neighbors.append(np)
 		# check enemy captures
 		number_enemies_captured = 0
 		enemies_captured = []
 		for ep in enemy_neighbors:
 			new_board, captured = check_if_captured(new_board, ep)
 			number_enemies_captured += len(captured)
 			enemies_captured += captured

 		# check for suicide
 		new_board, captured = check_if_captured(new_board, fp)
 		if captured:
 			print(p, 'ILLEGAL: SUICIDE')
 			return

 		# set new ko
 		if number_enemies_captured == 1 and possible_ko_color == enemy_color:
 			self.ko = enemies_captured[0]
 		else:
 			self.ko = None

 		self.board = new_board




#main
board = Board()
board.play_move([0,2], WHITE)
board.play_move([1,1], WHITE)
board.play_move([1,3], WHITE)
board.play_move([1,4], WHITE)
board.play_move([2,2], WHITE)
board.print_board()
board.play_move([0,3], BLACK)
board.play_move([1,5], BLACK)
board.play_move([2,3], BLACK)
board.play_move([0,4], BLACK)
board.play_move([2,4], BLACK)
board.play_move([1,2], BLACK)
board.print_board()

