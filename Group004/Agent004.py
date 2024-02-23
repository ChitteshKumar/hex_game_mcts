# make colour of game state
# add boardsize to self of mcts
from copy import deepcopy
import socket
from random import choice
from time import time as clock
import random 
import math
import sys
import time
from union import UnionFind
class GameState():
    def __init__(self,board_size = None,colour=None,board = None):
        self.board=board
        self.white_groups = UnionFind()
        self.black_groups = UnionFind()
        self.white_groups.set_ignored_elements([1, 2])
        self.black_groups.set_ignored_elements([1, 2])
        self.board_size = board_size
        self.colour =  colour
        self._winner = None
        self.visited=[]
        self.I_DISPLACEMENTS = [-1, -1, 0, 1, 1, 0]
        self.J_DISPLACEMENTS = [0, 1, 1, 0, -1, -1]
    
    def no_move(self):
        for i in range(self.board_size):
            if 0 in self.board[i]:
                return False
        return True

    def winner(self) -> int:
        """
        Return a number corresponding to the winning player,
        or none if the game is not over.
        """
        if self.white_groups.connected(1, 2):
            return "R"
        elif self.black_groups.connected(1, 2):
            return "B"
        else:
            return 0
    
    def movePossible(self):
        possible_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] ==0:
                    possible_moves.append((i, j))
        # #print(possible_moves,3456787654567898765567898765456789876)
        return possible_moves
    
    
    def getbgroup(self) -> dict:
        """
        Returns (dict): group of white groups for unionfind check
        """
        return self.white_groups.get_groups()

    def getbgroup(self) -> dict:
        """

        Returns (dict): group of white groups for unionfind check

        """
        return self.black_groups.get_groups()
    def place_white(self, cell: tuple) -> None:
        """
        Place a white stone regardless of whose turn it is.

        Args:
            cell (tuple): row and column of the cell
        """
        if self.board[cell[0]][cell[1]] == 0:
            self.board[cell[0]][cell[1]] = 'R'
        else:
            raise ValueError("Cell occupied")
        # if the placed cell touches a white edge connect it appropriately
        if cell[0] == 0:
            self.white_groups.join(1, cell)
        if cell[0] == self.board_size - 1:
            self.white_groups.join(2, cell)
        # join any groups connected by the new white stone
        for n in self.neighbors(cell):
            if self.board[n[0]][n[1]] == "R":
                self.white_groups.join(n, cell)
    
    def place_black(self, cell: tuple) -> None:
        """
        Place a white stone regardless of whose turn it is.

        Args:
            cell (tuple): row and column of the cell
        """
        if self.board[cell[0]][cell[1]] == 0:
            self.board[cell[0]][cell[1]] = 'B'
        else:
            raise ValueError("Cell occupied")
        # if the placed cell touches a white edge connect it appropriately
        if cell[0] == 0:
            self.black_groups.join(1, cell)
        if cell[0] == self.board_size - 1:
            self.black_groups.join(2, cell)
        # join any groups connected by the new white stone
        for n in self.neighbors(cell):
            if self.board[n[0]][n[1]]== "B":
                self.black_groups.join(n, cell)
    
    def play(self, cell: tuple) -> None:
        """
        Play a stone of the player that owns the current turn in input cell.
        Args:
            cell (tuple): row and column of the cell
        """
        if self.colour == 'R':
            self.place_white(cell)
            self.colour = 'B'
        elif self.colour == 'B':
            self.place_black(cell)
            self.colour = 'R'
    
    def neighbors(self, cell: tuple) -> list:
        """
        Return list of neighbors of the passed cell.

        Args:
            cell tuple):
        """
        x = cell[0]
        y = cell[1]
        return [(n[0] + x, n[1] + y) for n in [(-1, 0), (0, -1), (-1, 1), (0, 1), (1, 0), (1, -1)]
                if (0 <= n[0] + x < self.board_size and 0 <= n[1] + y < self.board_size)]

    def has_ended(self):
        """Checks if the game has ended. It will attempt to find a red chain
        from top to bottom or a blue chain from left to right of the board.
        """

        # Red
        # for all top tiles, check if they connect to bottom
        for idx in range(self.board_size):
            tile = self.board[0][idx]
            if (not (0,idx) in self.visited and
                tile == "R" and
                    self._winner is None):
                self.DFS_colour(0, idx, "R")
        # Blue
        # for all left tiles, check if they connect to right
        for idx in range(self.board_size):
            tile = self.board[idx][0]
            if (not (idx,0) in self.visited and
                tile == "B" and
                    self._winner is None):
                self.DFS_colour(idx, 0, "B")

        # un-visit tiles
        self.visited.clear()

        return self._winner is not None
    
    def DFS_colour(self, x, y, colour):
        """A recursive DFS method that iterates through connected same-colour
        tiles until it finds a bottom tile (Red) or a right tile (Blue).
        """
        
        self.visited.append((x,y))
        # win conditions
        if (colour == "R"):
            if (x == self.board_size-1):
                self._winner = colour
        elif (colour == "B"):
            if (y == self.board_size-1):
                self._winner = colour
        else:
            return

        # end condition
        if (self._winner is not None):
            
            return
        
        # visit neighbours
        for idx in range(6):
            x_n = x + self.I_DISPLACEMENTS[idx]
            y_n = y + self.J_DISPLACEMENTS[idx]
            if (x_n >= 0 and x_n < self.board_size and
                    y_n >= 0 and y_n < self.board_size):
                neighbour = self.board[x_n][y_n]
                if (not (x_n,y_n) in self.visited and
                        self.board[x_n][y_n] == colour):
                    self.DFS_colour(x_n, y_n, colour)
        
class MCTSNode():
    def __init__(self, move=None, parent=None):
        self.parent = parent # Parent node
        self.move = move
         # Child nodes
        self.visits = 0 # Number of times this node has been visited
        self.value = 0  # average reward
        self.rave_value = 0
        self.rave_visits = 0
        self.children = []
        self.N = 0  # times this position was visited
        self.Q = 0  # average reward (wins-losses) from this position
        self.Q_RAVE = 0  # times this move has been critical in a rollout
        self.N_RAVE = 0  # times this move has appeared in a rollout
        
    def add_children(self, children: list):
        for child in children:
            self.children.append(child)
    def nodeValue(self, use_rave=True):
        C = 0.5
        rave_exploration = 500
        explore = 0.5

        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else:
            # rave valuation:
            alpha = max(0, (rave_exploration - self.N) / rave_exploration)
            UCT = self.Q / self.N + explore * math.sqrt(2 * math.log(self.parent.N) / self.N)
            AMAF = self.Q_RAVE / self.N_RAVE if self.N_RAVE != 0 else 0
            return (1 - alpha) * UCT + alpha * AMAF
            



    
    
    
class MCTS():
    
    """This class describes the MCTS Hex agent. It will apply Monte-Carlo Tree Search algorithm which 
    explores possible moves in a tree-like structure, simulates random plays to evaluate potential outcomes, 
    and selects the most promising moves based on accumulated statistical information. 
    """

    HOST = "127.0.0.1"
    PORT = 1234

    def __init__(self):
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.s.connect((self.HOST, self.PORT))
        self.root = MCTSNode()
        self.state = GameState()
        self.board_size = None
        self.board = None
        self.colour = None
        self._winner=None
        
    
    

    def run(self):
        """Reads data until it receives an END message or the socket closes."""
        # print("self")
        while True:
            data = self.s.recv(1024)
            #print("hi")
            #print(data)
            if not data:
                break
            if (self.interpret_data(data)):
                break


    def interpret_data(self, data):
        """Checks the type of message and responds accordingly. Returns True
        if the game ended, False otherwise.
        """
        self.root = MCTSNode()
        # self.state = GameState()
        messages = data.decode("utf-8").strip().split("\n")
        messages = [x.split(";") for x in messages]
        # print(messages)
        for s in messages:
            if s[0] == "START":
                self.board_size = int(s[1])
                self.colour = s[2]
                self.state.board=[[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
                self.state.board_size = self.board_size

                if self.colour == "R":
                    self.make_move()

            elif s[0] == "END":
                return True

            elif s[0] == "CHANGE":
                if s[3] == "END":
                    return True

                elif s[1] == "SWAP":
                    self.colour = self.opp_colour()
                    if s[3] == self.colour:
                        self.make_move()

                elif s[3] == self.colour:

                    # print("6378287474774883748487488748847")
                    x=s[1].split(',')
                    print(x)
                    if self.state.colour is not None:
                        self.state.play((int(x[0]),int(x[1])))
                    else:
                        print(self.state.board_size,int(x[0]))
                        self.state.board[int(x[0])][int(x[1])] = s[2][self.state.board_size*int(x[0])+int(x[1])+int(x[0])]
                        print(s[2][self.board_size*int(x[0])+int(x[1])+int(x[0])])
                    print(self.state.board)
                    self.make_move()

        return False
    

    
    


    

    def make_move(self):
        """Selects and sends the best move to the game server using MCTS."""
        best_move =self.best_move1()
        #print(best_move,4567887656787656776545678765456)
        self.state.play(best_move)
        print(best_move)
        move_str = f"{best_move[0]},{best_move[1]}\n"
        self.s.sendall(bytes(move_str, "utf-8"))
        # print("************************************************************************************")




    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """
        if self.colour == "R":
            return "B"
        elif self.colour == "B":
            return "R"
        else:
            return "None"
        
    # My code from here
    
    def best_move1(self):
        self.state.colour = self.colour
        start_time = clock()
        a=0
        while clock() - start_time < 8:
        # for _ in range(1000):
            a+=1
            node,state=self.Select_node()
            colour=state.colour

            # print(colour)
            winner,blue_r,red_r=self.simulate_game(state)
            self.back_propogate(node,colour,winner,blue_r,red_r)
        # print(a)
        max_nodes=[]
        max=sys.maxsize
        max = -max
        # print(self.ff)
        for i in self.root.children:
            # print(i.nodeValue())
            if i.nodeValue()!=float("inf"):
                if i.nodeValue() >max:
                    max=i.nodeValue()
                    max_nodes.clear()
                    max_nodes.append(i)
                elif i.nodeValue()==max:
                    max_nodes.append(i)
        best_move = choice(max_nodes)
        return best_move.move
    
    
    def Select_node(self):
        state = deepcopy(self.state)
        node = self.root
        a=0
        while len(node.children)!=0:
            max=node.children[0].nodeValue()
            max_nodes=[]
            node.visits+=1
            for i in node.children:
                if i.nodeValue() >max:
                    max=i.nodeValue()
            max_nodes = [n for n in node.children if
                         n.nodeValue() == max]
            node = choice(max_nodes)
            state.play(node.move)
            if node.N == 0:
                return node, state
        
        # print("sss")
        self.expandTree(node,state)
        
        if len(node.children):
            node = choice(node.children)
            state.play(node.move)
        return node, state
    
    def expandTree(self, parent: MCTSNode,state):
         # Expand the tree by adding a child node for an unexplored move
        children = []
        poss_move = state.movePossible()
        for move in poss_move:    
            children.append(MCTSNode(move=move, parent=parent))
        parent.add_children(children)
        return True
    
    def simulate_game(self,state:GameState):
        poss_moves = state.movePossible()
        while len(poss_moves) != 0:
            # print(poss_moves)
            move = choice(poss_moves)
            state.play(move)
            poss_moves.remove(move)
        state._winner=None
        state.has_ended()

    
        blue_r = []
        red_r = []
    
        for x in range(state.board_size):
            for y in range(state.board_size):
                if state.board[x][y] == "B":
                    blue_r.append((x, y))
                elif state.board[x][y] == "R":
                    red_r.append((x, y))
        return state._winner, blue_r, red_r
    
    
    def back_propogate(self,node:MCTSNode,colour,winner,blue_r,red_r):
        final = -1 if winner == colour else 1
        moves=[]
        #print(node.children)
        for w in node.children:
            moves.append(w.move)
        # print(moves)
        while node is not None:
            moves=[]
            #print(node.children)
            for w in node.children:
                moves.append(w.move)
            if colour == "R":
                for point in red_r:
                    if point in moves:
                        node.children[moves.index(point)].Q_RAVE += -final
                        node.children[moves.index(point)].N_RAVE += 1
            else:
                for point in blue_r:
                    if point in moves:
                        node.children[moves.index(point)].Q_RAVE += -final
                        node.children[moves.index(point)].N_RAVE += 1
    
            node.N += 1
            node.Q += final
            colour = "R" if colour =="B" else "B"
            final = -final
            node = node.parent
                    
        

if (__name__ == "__main__"):
    agent = MCTS()
    # print("run")
    agent.run()
