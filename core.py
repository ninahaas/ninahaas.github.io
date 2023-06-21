import copy

BLACK = 'B'
WHITE = 'W'
EMPTY = '_'


class Board:
    def __init__(self, N):
        self.N = N
        self.NN = N ** 2
        self.board = [EMPTY] * self.NN
        self.ko = None
        self.all_neighbors = self.get_all_neighbors()

    # flattens 2D position into 1 number
    def flatten(self, p):
        return self.N * p[0] + p[1]

    def unflatten(self, fp):
        return divmod(fp, self.N)

    def switch_color(self, color):
        if color == BLACK:
            return WHITE
        elif color == WHITE:
            return BLACK
        else:
            return EMPTY

    def pos_is_empty(self, p):
        return self.board[self.flatten(p)] == EMPTY

    # returns list of list of neighbors in order of flattened positions
    def get_all_neighbors(self):
        def get_neighbors(fp):
            x, y = self.unflatten(fp)
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            neighbors_in_bounds = []

            # only keep neighbors in bounds
            for p in neighbors:
                if 0 <= p[0] < self.N and 0 <= p[1] < self.N:
                    neighbors_in_bounds.append(self.flatten(p))
            return neighbors_in_bounds

        return [get_neighbors(fp) for fp in range(self.NN)]

    def place_stone(self, p, color):
        fp = self.flatten(p)
        self.board[fp] = color

    def bulk_place_stones(self, fps, color):
        for fp in fps:
            self.board[fp] = color

    def check_ko_color(self, p):
        fp = self.flatten(p)
        color = self.board[self.all_neighbors[fp][0]]
        for np in self.all_neighbors[fp]:
            if self.board[np] != color:
                return None
        return color

    def set_ko(self, number_enemies_captured, possible_ko_color, color):
        enemy_color = self.switch_color(color)
        if number_enemies_captured == 1 and possible_ko_color == enemy_color:
            return self.unflatten(enemies_captured[0])
        else:
            return None

    def find_reached(self, fp):
        color = self.board[fp]
        frontier = [fp]
        reached = []
        chain = []
        while frontier:
            current_fp = frontier.pop()
            chain.append(current_fp)
            for np in self.all_neighbors[current_fp]:
                if self.board[np] == color and np not in chain:
                    frontier.append(np)
                elif self.board[np] != color:
                    reached.append(np)
        return reached, chain

    def check_if_captured(self, fp):
        reached, chain = self.find_reached(fp)
        if not any(self.board[rp] == EMPTY for rp in reached):
            self.bulk_place_stones(chain, EMPTY)
            return chain
        else:
            return []

    def get_enemy_neighbors(self, p, color):
        fp = self.flatten(p)
        enemy_neighbors = []
        enemy_color = self.switch_color(color)
        for np in self.all_neighbors[fp]:
            if self.board[np] == enemy_color:
                enemy_neighbors.append(np)
        return enemy_neighbors

    def capture_enemies(self, p, color):
        enemy_neighbors = self.get_enemy_neighbors(p, color)
        number_enemies_captured = 0
        enemies_captured = []
        for fp in enemy_neighbors:
            captured = self.check_if_captured(fp)
            number_enemies_captured += len(captured)
            enemies_captured += captured
        return number_enemies_captured, enemies_captured

    def check_suicide(self, p):
        return self.check_if_captured(self.flatten(p))

    def get_score(self):
        while EMPTY in self.board:
            ep = self.board.index(EMPTY)
            reached, chain = self.find_reached(ep)
            # check if reached are all one color
            color = self.board[reached[0]]
            if any(self.board[rp] != color for rp in reached):
                self.bulk_place_stones(chain, '?')
            else:
                self.bulk_place_stones(chain, color)
        # return positive number = black wins
        return self.board.count(BLACK) - self.board.count(WHITE)


class Game:
    def __init__(self):
        self.board = Board(19)
        self.ko = None

    def print_board(self):
        for i in range(self.board.N):
            print(self.board.board[0 + (i * self.board.N): (self.board.N - 1) + (i * self.board.N)])
        print('')

    def play_move(self, p, color):
        # check if position is empty
        if not self.board.pos_is_empty(p):
            print(p, 'ILLEGAL: POSITION TAKEN')
            return

        # check if ko
        if self.ko == p:
            print(p, 'ILLEGAL: KO')
            return

        # get possible ko color
        possible_ko_color = self.board.check_ko_color(p)

        # place stone
        new_board = copy.deepcopy(self.board)
        new_board.place_stone(p, color)

        # check enemy captures
        number_enemies_captured, enemies_captured = new_board.capture_enemies(p, color)

        # check for suicide
        if new_board.check_suicide(p):
            print(p, 'ILLEGAL: SUICIDE')
            return

        # set new ko
        self.ko = new_board.set_ko(number_enemies_captured, possible_ko_color, color)

        self.board = new_board

    def end_game(self):
        score = self.board.get_score()
        if score > 0:
            print("BLACK WINS WITH", score, "POINTS")
        elif score < 0:
            print("WHITE WINS WITH", score, "POINTS")
        else:
            print("DRAW")


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
print(game.end_game())
game.print_board()
