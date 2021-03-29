"""
8-puzzle problem with A* alorithum search
"""
import sys, copy
import math
goal_state =  [[0,1,2],
               [3,4,5],
               [6,7,8]]

def main():
     """
        Main function for input and start of the program.
        Default value for the problem search matrix is 325687014
     """
     puzzle = EightPuzzle()
     print("""
      ___           .______    __    __   ________   ________   __       _______
     / _ \          |   _  \  |  |  |  | |       /  |       /  |  |     |   ____|
    | (_) |  ______ |  |_)  | |  |  |  | `---/  /   `---/  /   |  |     |  |__
     > _ <  |______||   ___/  |  |  |  |    /  /       /  /    |  |     |   __|
    | (_) |         |  |      |  `--'  |   /  /----.  /  /----.|  `----.|  |____
     \___/          | _|       \______/   /________| /________||_______||_______|
     """)

     print("Input 1 or 2 for Manhattan/Misplace tile distance")
     while True:
        h = input("1/2:: ")
        try:
            h = int(h)
        except:
            print("Enter a number")
            continue
        if h == 1:
            break
        elif h == 2:
            break

        print('Please enter a valid number')
        continue

     """ Set puzzle by commenting the other line out with # """

     #puzzle.set("123045678") # 13 moves
     #puzzle.set("123405678") # 14 moves
     puzzle.set("325687014") # 16 moves
     #puzzle.set("072456831") # 26 moves (a difficult position)
     #puzzle.set("724506831") # 26 moves

     print("initial:: \n")
     puzzle.show()
     print("Goal State ::\n ")
     show(goal_state)
     print("solving:: \n")
     puzzle.solve(h)


def show(puzzle):
    """
    Prints a puzzle matrix to the terminal
    """
    print('')
    print("  ", puzzle[0][0],puzzle[0][1],puzzle[0][2])
    print("  ", puzzle[1][0],puzzle[1][1],puzzle[1][2])
    print("  ", puzzle[2][0],puzzle[2][1],puzzle[2][2])
    print('')

def checkSolved(path_node):
    """
    Check the goal state has been found
    """
    return path_node.matrix == goal_state

def manhattanDistance(search, goal):
    """
    Calcualte the heuristic h(n) as manhattan distance
    """
    man_dist = 0
    # search through the numbers in the puzzle
    for index in range(9):
        #rows
        for i in range(3):
            #colomns
            for j in range(3):
                # get where the number should be
                if (index == goal[i][j]):
                    goal_row = i
                    goal_col = j
                # get where the number is now
                if (index == search[i][j]):
                    puzzle_row = i
                    puzzle_col = j
        # calculate the Manhattan Distance based on the points
        man_dist += (abs(goal_row - puzzle_row) + abs(goal_col - puzzle_col))
    return man_dist

def misplaced_tiles(search, goal):
    """
    Calcualte the heuristic h(n) as misplaced distance
    """
    mis_dist = 0
    #rows
    for i in range(0,3):
        #colomns
        for j in range(0,3):
            if (search[i][j] != goal[i][j]):
                    mis_dist += 1

    return mis_dist

def distanceFunction(h, search, goal):
    """
    Gets the h value for the heristic to perform
    """
    hval = h
    val = 0
    if hval == 1:
        val = manhattanDistance(search, goal)
    if hval == 2:
        val = misplaced_tiles(search, goal)
    return val

def possibleMoves(matrix_search):
    """
    Finds the possible moves where the index is 0 in the puzzle
    The possible moves are saved for the rows and colomns which can be swapped
    The current index of the 0 is also located
    """
    possible_m = []
    matrix = matrix_search
    index = []
    row_c = 0
    col_c = 0

    for rows in matrix:
        col_c = 0
        for col in rows:
            if col == 0:
                row_index, col_index = row_c, col_c
                index.append(row_index)
                index.append(col_index)
                break
            else:
                col_c +=1
        row_c+=1

    for rowww in range(row_index-1, row_index+2):
        for colll in range(col_index-1, col_index+2):
            if (-1 < rowww < 3) and (-1 < colll < 3):
                if rowww != row_index:
                    if colll == col_index:
                        possible_m.append([rowww, colll])
                if rowww == row_index:
                    possible_m.append([rowww, colll])

    for i in possible_m:
        if i == index:
            possible_m.remove(i)

    return possible_m, index

def heuristic(node):
    """
    For the sort of the queue by the f(n) values for the nodes in the queue
    """
    return node.fn


def in_list(node, closed_nodes):
    """
    If the node puzzle state has been vistited before, it will be skipped
    """
    for c_nodes in closed_nodes:
        if node == c_nodes.matrix:
            return True

def add_queue(new_path, Queue):
    """
    If the node already exits in the queue and the f(n) value is greater then
    new node then the node will be skipped.
    """
    for node in Queue:
        if new_path.matrix == node.matrix and node.fn >= new_path.fn:
            return False
    return True

class Node:
    """
    Node class object
    """
    def __init__(self):
        """
        Initial setup of the class
        """
        self.gn = 0
        self.hn = 0
        self.moves = 0
        self.matrix = []
        self.fn = 0
        self.path = []

    def setPuzzle(self, puzzle):
        """
        Set the puzzle state of the object
        """
        self.matrix = puzzle

    def set_fn(self):
        """
        Calculate the value of the f(n) value
        """
        self.fn = self.gn + self.hn


class EightPuzzle:
    """
    Puzzle class
    """
    def __init__(self):
        """
        Setup of the puzzle program
        """
        self.search_matrix = [[0,0,0],[0,0,0],[0,0,0]]
        self.goal_matrix = goal_state

    def set(self, other):
        """
        Setup of the initial search matrix
        """
        i=0;
        for row in range(3):
            for col in range(3):
                self.search_matrix[row][col] = int(other[i])
                i=i+1

    def show(self):
        """
        Show the puzzle to the terminal
        """
        print('')
        print(self.search_matrix[0][0], self.search_matrix[0][1], self.search_matrix[0][2])
        print(self.search_matrix[1][0], self.search_matrix[1][1], self.search_matrix[1][2])
        print(self.search_matrix[2][0], self.search_matrix[2][1], self.search_matrix[2][2])
        print("\n")

    def expandMoves(self, possible_moves, index_0, parent_node):
        """
        Expanded puzzle states for the possoble moves
        """
        new_puzzle_state = []
        temp_puzzle = []
        temp_index_swap = 0
        for i in possible_moves:
            temp_puzzle = copy.deepcopy(parent_node)
            temp_index_swap = temp_puzzle[i[0]][i[1]]
            temp_puzzle[i[0]][i[1]] = 0
            temp_puzzle[index_0[0]][index_0[1]] = temp_index_swap
            new_puzzle_state.append(temp_puzzle)
        return new_puzzle_state

    def solve(self, h):
        """
        Main solve function where the puzzle will loop through until a solution
        if found or the queue is exhausted
        """
        self.hval = h
        self.parent = 0
        self.gn = 0
        self.hn = distanceFunction(self.hval,self.search_matrix, self.goal_matrix)
        nodesExpanded = 0
        #______________
        priority_queue = []
        closed_nodes = []
        #_____________
        initial_node = Node()
        initial_node.setPuzzle(self.search_matrix)
        initial_node.hn = self.hn
        initial_node.gn = -1
        priority_queue.append(initial_node)

        while 1:
            self.hval = h
            if (len(priority_queue) == 0):
                print("Puzzle search exhausted")
                sys.exit(0)
            elif(len(closed_nodes) > nodesExpanded):
                print("Puzzle search exhausted")
                sys.exit(0)
            #set path node for first in queue
            path_node = Node()
            path_node.setPuzzle(priority_queue[0].matrix)
            path_node.hn = priority_queue[0].hn
            path_node.gn = priority_queue[0].gn
            path_node.moves = priority_queue[0].moves
            path_node.path = priority_queue[0].path
            path_node.set_fn()

            print("Going with path node: \n")
            print("fn:: ",priority_queue[0].fn)
            print("Heuristic value:: ", priority_queue[0].hn)
            print("Depth:: ", priority_queue[0].gn)
            show(path_node.matrix)

            current_node = priority_queue[0]
            closed_nodes.append(current_node)
            priority_queue.pop(0)

            #check state is solved
            if checkSolved(path_node):
                print(":: Solved :: \n")
                print("In moves: ",path_node.moves)
                print("Depth: ", path_node.gn)
                path_node.path.append(self.goal_matrix)
                print("Nodes visited:", len(closed_nodes))
                print("Total nodes generated: ", nodesExpanded)
                print("Move list: ")
                for path_parent in path_node.path:
                    show(path_parent)
                sys.exit(0)

            possible_moves, index_0 = possibleMoves(path_node.matrix)
            possible_matrixes = EightPuzzle.expandMoves(self, possible_moves, index_0, path_node.matrix)

            for node in possible_matrixes:
                if in_list(node, closed_nodes):
                    continue

                new_path = Node()
                new_path.setPuzzle(node)
                new_path.hn = distanceFunction(h, new_path.matrix, self.goal_matrix)
                new_path.gn = path_node.gn + 1
                new_path.moves = path_node.moves + 1
                new_path.path = copy.deepcopy(path_node.path)
                new_path.path.append(path_node.matrix)
                new_path.set_fn()
                if add_queue(new_path, priority_queue):
                    priority_queue.append(new_path)
                    nodesExpanded += 1

            priority_queue.sort(key=heuristic)




if __name__ == "__main__":
    main()
