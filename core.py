import copy

N = 19
NN = N ** 2
BLACK = 'B'
WHITE = 'W'
EMPTY = '_'

class Board:
    def __init__(self):
        self.board = [EMPTY] * NN
        self.ko = None

    # flattens 2D position into 1 number
    def flatten(self, p):
        return N * p[0] + p[1]

    def unflatten(self, fp):
        return divmod(fp, N)

    def switch_color(self, color):
        if color == BLACK:
            return WHITE
        elif color == WHITE:
            return BLACK
        else:
            return EMPTY

    # returns list of list of neighbors in order of flattened positions
    def get_all_neighbors(self):
        def get_neighbors(fp):
            x, y = self.unflatten(fp)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            neighbors_in_bounds = []

            # only keep neighbors in bounds
            for p in neighbors:
                if 0 <= p[0] < N and 0 <= p[1] < N:
                    neighbors_in_bounds.append(self.flatten(p))
            return neighbors_in_bounds

        return [get_neighbors(fp) for fp in range(NN)]

    def place_stone(self, fp, color):
        self.board[fp] = color

    def bulk_place_stones(self, fps, color):
        for fp in fps:
            self.board[fp] = color

    def check_ko_color(self, fp, neighbors):
        color = self.board[neighbors[0]]
        for np in neighbors:
            if self.board[np] != color:
                return None
        return color

    def find_reached(self, fp, all_neighbors):
        color = self.board[fp]
        frontier = [fp]
        reached = []
        chain = []
        while frontier:
            current_fp = frontier.pop()
            chain.append(current_fp)
            for np in all_neighbors[current_fp]:
                if self.board[np] == color and np not in chain:
                    frontier.append(np)
                elif self.board[np] != color:
                    reached.append(np)
        return reached, chain

    def check_if_captured(self, fp, all_neighbors):
        reached, chain = self.find_reached(fp, all_neighbors)
        print(reached, chain)
        if not any(self.board[rp] == EMPTY for rp in reached):
            self.bulk_place_stones(chain, EMPTY)
            return chain
        else:
            return []


class Game:
    def __init__(self):
        self.board = Board()
        self.all_neighbors = self.board.get_all_neighbors()
        self.ko = None

    def print_board(self):
        for i in range(N):
            print(self.board.board[0 + (i * N): (N - 1) + (i * N)])
        print('')

    def play_move(self, p, color):
        fp = self.board.flatten(p)
        # check if position is empty
        if self.board.board[fp] != EMPTY:
            print(p, 'ILLEGAL: POSITION TAKEN')
            return
        # check if ko
        if self.ko == fp:
            print(p, 'ILLEGAL: KO')
            return

        # get possible ko color
        possible_ko_color = self.board.check_ko_color(fp, self.all_neighbors[fp])

        # place stone
        new_board = copy.deepcopy(self.board)
        new_board.place_stone(fp, color)

        # find neighbors
        my_neighbors = []
        enemy_neighbors = []
        enemy_color = self.board.switch_color(color)
        for np in self.all_neighbors[fp]:
            if new_board.board[np] == color:
                my_neighbors.append(np)
            elif new_board.board[np] == enemy_color:
                enemy_neighbors.append(np)

        # check enemy captures
        number_enemies_captured = 0
        enemies_captured = []
        for ep in enemy_neighbors:
            captured = new_board.check_if_captured(ep, self.all_neighbors)
            number_enemies_captured += len(captured)
            enemies_captured += captured

        # check for suicide
        captured = new_board.check_if_captured(fp, self.all_neighbors)
        if captured:
            print(p, 'ILLEGAL: SUICIDE')
            return

        # set new ko
        if number_enemies_captured == 1 and possible_ko_color == enemy_color:
            self.ko = enemies_captured[0]
        else:
            self.ko = None

        self.board = new_board

    def get_score(self):
        score_board = copy.deepcopy(self.board)
        while EMPTY in score_board.board:
            ep = score_board.board.index(EMPTY)
            reached, chain = score_board.find_reached(ep, self.all_neighbors)
            # check if reached are all one color
            color = score_board.board[reached[0]]
            if any(score_board.board[rp] != color for rp in reached):
                score_board.bulk_place_stones(chain, '?')
            else:
                score_board.bulk_place_stones(chain, color)

        self.board = score_board
        # return positive number = black wins
        return score_board.board.count(BLACK) - score_board.board.count(WHITE)


def test_place_stone():
    game = Game()
    fp = game.board.flatten([0,0])
    assert game.board.board[fp] == EMPTY
    game.board.place_stone(fp, WHITE)
    assert game.board.board[fp] == WHITE


# main
game = Game()
game.play_move([0, 2], WHITE)
game.play_move([1, 1], WHITE)
game.play_move([1, 3], WHITE)
game.play_move([1, 4], WHITE)
game.play_move([2, 2], WHITE)
game.print_board()
game.play_move([0, 3], BLACK)
game.play_move([1, 5], BLACK)
game.play_move([2, 3], BLACK)
game.play_move([0, 4], BLACK)
game.play_move([2, 4], BLACK)
game.play_move([1, 2], BLACK)
print(game.get_score())
game.print_board()
