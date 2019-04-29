# Erich Johnson
# Com Sci 471
# This project is to find the best move for a player to make using a heuristic
# Assumes lookahead means if I look ahead 0 then I look at just x and do the heuristic
# 1 would look at x and then y
# 2 would look at x and then y and then x
# 3 would look at x and then y and then x and then y
# and so on and so forth
# FUNCTION AND CLASSES

import sys
import copy
import math


class GameMap:
    state_of_game = None

    def _init__(self):
        self.state_of_game = [[0 for x in range(7)] for y in range(6)]

    def drop_connect(self, column, player):
        if self.state_of_game[0][column] is '_':  # checks to see if can move in column
            row = 0
            while row is not 5 and self.state_of_game[row + 1][column] is '_':  # will find the next move in the column
                row += 1
            # player will be either x or o need to keep track
            if player is 'x':  # changes the '_' space to the player that moved there
                self.state_of_game[row][column] = 'x'
            else:
                self.state_of_game[row][column] = 'o'

            return True
        else:
            return False


class GraphNode:
    score = None  # the heuristic score
    children_nodes = []  # list of children nodes
    game_map = None  # is the game map of the state
    player = None  # is the player
    finished = False  # gives if state is finished
    best_next_move = None  # will tell the best_next move in the graph by column move

    def __init__(self, Node, xoro):  # initialises the node
        self.nodes_name = Node  # give the name which is the column of the move
        self.player = xoro  # can be x or o
        self.game_map = GameMap
        self.children_nodes = []  # Is a list of the adjacent nodes by their nodes_name


class Graph:

    nodes_list = {}  # nodes_list is in a graph format where (reference, object)
    terminal_list = []  # is the list of the terminals which are not finished

    def __init__(self, name, start_map, player):  # initialises the graph and also adds the first node
        self.nodes_list = []  # gives a list of nodes which might be used very much
        node = GraphNode(name, player)  # creates the initial state
        node.game_map = GameMap()
        node.game_map.state_of_game = copy.deepcopy(start_map)  # does a deep copy
        self.nodes_list.append(node)
        self.terminal_list.append(self.nodes_list[0])

    def look_moves_ahead(self, moves_into_the_future):
        best_move = 0
        for moves in range(0, moves_into_the_future + 1):  # will do x + 1 amount of moves into the future
            new_terminal_list = []
            for state in self.terminal_list:  # goes through every node in list
                for x in range(0, 7):  # goes through every column on the list
                    new_state = GameMap()  # copies the last state of the game
                    new_state.state_of_game = copy.deepcopy(state.game_map.state_of_game)
                    change = new_state.drop_connect(x, state.player)  # drops down a move and returns if it is possible
                    if change is True:  # checks to see if a change was possible
                        new_player = change_player(state.player)  # changes the player
                        # checks to see if game is over
                        game_over_check = is_game_over(new_state.state_of_game, x, state.player)
                        name = x  # row equals the name for the time
                        new_node = GraphNode(name, new_player)  # makes a new node
                        new_node.game_map = copy.deepcopy(new_state)
                        if game_over_check is True:  # if game is done change score
                            new_node.finished = True
                            if state.player is 'x':
                                new_node.score = math.inf
                            else:
                                new_node.score = -math.inf
                        state.children_nodes.append(new_node)

                        if game_over_check is False:  # if false it gets added to the list where the next moves continue
                            new_terminal_list.append(new_node)
            self.terminal_list = new_terminal_list  # sets up for the next moves to be made
        best_move = minimax(self.nodes_list[0], self.nodes_list[0].player)  # get the best column move
        return self.nodes_list[0].best_next_move


def change_player(player):  # changes the player
    new_player = None
    if player is 'x':
        new_player = 'o'
    else:
        new_player = 'x'
    return new_player


def minimax(state, player):  # goes through the tree using a min max algorithm
    # is recursive so it will prop up and will move the moves while done so in like a dfs way

    # if there is no score and is a terminal then find score
    if len(state.children_nodes) is 0 and state.finished is False:
        state.score = heuristic(state.game_map.state_of_game)

    # for the x player which is assumed they are max and not finished or a terminal then it will decided best score
    # by the next possible moves which the max score is
    if player is 'x' and len(state.children_nodes) is not 0 and state.finished is False:  # goes for max
        score = -math.inf
        for child in state.children_nodes:  # goes through every node
            if child.score is None:  # if the child doesn't have a score it also does a min max search on the node
                minimax(child, child.player)
            if child.score > score:  # checks to see if the score is the best
                score = child.score
                state.best_next_move = child.nodes_name
        state.score = score

        return score

    # for the y player which is assumed they are min and not finished or a terminal then it will decided best score
    # by the next possible moves which the min score is
    if player is 'o' and len(state.children_nodes) is not 0 and state.finished is False:  # goes for min
        score = math.inf
        for child in state.children_nodes:  # goes through every node
            if child.score is None:  # if the child doesn't have a score it also does a min max search on the node
                minimax(child, child.player)
            if child.score < score:  # checks to see if the score is the best
                score = child.score
                state.best_next_move = child.nodes_name
        state.score = score
        return score


def heuristic(game_map):  # number of 3 in a row blocks of x's - number of 3 in a row blocks of o's
    score = 0
    for y in range(6):
        for x in range(7):
            if game_map[y][x] is 'x':
                score += check_in_a_row(game_map, x, y, 'x')
            elif game_map[y][x] is 'o':
                score -= check_in_a_row(game_map, x, y, 'y')
    return score


def check_in_a_row(game_map, x, y, x_or_o):  # I think this is done
    number_in_row = 0
    if x + 2 <= 6:  # check if you can go right
        if game_map[y][x] is x_or_o and game_map[y][x+1] is x_or_o and game_map[y][x+2] is x_or_o:
            number_in_row += 1
        if y + 2 <= 5:  # check if you can go down and right
            if game_map[y][x] is x_or_o and game_map[y+1][x + 1] is x_or_o and game_map[y+2][x + 2] is x_or_o:
                number_in_row += 1
        if -1 <= y - 2:  # check if can go up and right
            if game_map[y][x] is x_or_o and game_map[y-1][x + 1] is x_or_o and game_map[y-2][x + 2] is x_or_o:
                number_in_row += 1
    if y + 2 <= 5:  # check if go just down
        if game_map[y][x] is x_or_o and game_map[y+1][x] is x_or_o and game_map[y+2][x] is x_or_o:
            number_in_row += 1
    return number_in_row


def is_game_over(game_map, x, player):
    game_over = False

    y = 0
    while player != game_map[y][x]:
        y += 1

    # checks for all in horizontal

    # look for xxxz
    if 0 < x - 3 and game_map[y][x-1] is player and game_map[y][x-2] is player and game_map[y][x-3] is player:
        game_over = True
    # look for xxzx
    if 0 <= x - 2 and x + 1 <= 6 and game_map[y][x+1] is player and game_map[y][x-1] is player and game_map[y][x-2] is player:
        game_over = True
    # look for xzxx
    if 0 <= x - 1 and x + 2 <= 6 and game_map[y][x+2] is player and game_map[y][x+1] is player and game_map[y][x-1] is player:
        game_over = True
    # look for zxxx
    if x + 3 <= 6 and game_map[y][x+3] is player and game_map[y][x+2] is player and game_map[y][x+1] is player:
        game_over = True

    # checks for all in vertical

    # look for zyyy
    if y + 3 <= 5 and game_map[y+3][x] is player and game_map[y+2][x] is player and game_map[y+1][x] is player:
        game_over = True
    # look for yzyy
    if 0 <= y - 1 and y + 2 <= 5 and game_map[y+2][x] is player and game_map[y+1][x] is player and game_map[y-1][x] is player:
        game_over = True
    # look for yyzy
    if 0 <= y - 2 and y + 1 <= 5 and game_map[y+1][x] is player and game_map[y-1][x] is player and game_map[y-2][x] is player:
        game_over = True
    # look for yyyz
    if 0 <= y - 3 and game_map[y-1][x] is player and game_map[y-2][x] is player and game_map[y-3][x] is player:
        game_over = True

    # checks for all in diagonal in the 10:30 and 4:30 o clock
    # [xy][xy][xy][z]
    if 0 <= x - 3 and 0 <= y - 3 and game_map[y-3][x-3] is player and game_map[y-2][x-2] is player and game_map[y-1][x-1] is player:
        game_over = True
    # [xy][xy][z][xy]
    if 0 <= x - 2 and x + 1 <= 6 and 0 <= y - 2 and y + 1 <= 5 and game_map[y-2][x-2] is player and game_map[y-1][x-1] is player and game_map[y+1][x+1] is player:
        game_over = True
    # [z][xy][xy][xy]
    if 0 <= x - 1 and x + 2 <= 6 and 0 <= y - 1 and y + 2 <= 5 and game_map[y-1][x-1] is player and game_map[y+1][x+1] is player and game_map[y+2][x+2] is player:
        game_over = True
    # [xy][xy][xy][z]
    if x + 3 <= 6 and y + 3 <= 5 and game_map[y+1][x+1] is player and game_map[y+2][x+2] is player and game_map[y+3][x+3] is player:
        game_over = True

    # checks for all in diagonal in the 1:30 and 7:30 o clock
    # [xy][xy][xy][z]
    if x + 3 <= 6 and 0 <= y - 3 and game_map[y-3][x+3] is player and game_map[y-2][x+2] is player and game_map[y-1][x+1] is player:
        game_over = True
    # [xy][xy][z][xy]
    if 0 <= x - 1 and x + 2 <= 6 and 0 <= y - 2 and y + 1 <= 5 and game_map[y-2][x+2] is player and game_map[y-1][x+1] is player and game_map[y+1][x-1] is player:
        game_over = True
    # [xy][z][xy][xy]
    if 0 <= x - 2 and x + 1 <= 1 and 0 <= y - 1 and y + 2 <= 5 and game_map[y-1][x+1] is player and game_map[y+1][x-1] is player and game_map[y+2][x-2] is player:
        game_over = True
    # [z][xy][xy][xy]
    if 0 <= x - 3 and y + 3 <= 5 and game_map[y+1][x-1] is player and game_map[y+2][x-2] is player and game_map[y+3][x-3] is player:
        game_over = True

    return game_over


def which_row_did_i_move(state, column):  # checks for the best move row
    # goes from initial state to find the next move in the column
    row = 0
    while row is not 5 and state.game_map.state_of_game[row + 1][column] is '_':
        row += 1
        # player will be either x or o need to keep track

    return row

# main code

# used to parse command line

# sys argument is python Play.py input_file.txt <-- 1 lookahead <-- 2


input_file = str(sys.argv[1])
look_ahead = int(sys.argv[2])

# for  line in FileTemp:

initial_state = [[0 for x in range(7)] for y in range(6)]
with open(input_file) as FileTemp: # parses the data to make a 6 by 7 graph
    iterator = 0
    for line in FileTemp:
        Col_1, Col_2, Col_3, Col_4, Col_5, Col_6, Col_7 = line.split()  # parses the line
        # map lay out is [y][x]
        initial_state[iterator][0] = Col_1
        initial_state[iterator][1] = Col_2
        initial_state[iterator][2] = Col_3
        initial_state[iterator][3] = Col_4
        initial_state[iterator][4] = Col_5
        initial_state[iterator][5] = Col_6
        initial_state[iterator][6] = Col_7
        iterator += 1
Game = Graph(None, initial_state, 'x')

best_move_column = Game.look_moves_ahead(look_ahead)
best_move_row = which_row_did_i_move(Game.nodes_list[0], best_move_column)


print("[" + str(best_move_row) + ", " + str(best_move_column) + "] " + str(Game.nodes_list[0].score))