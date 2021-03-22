import sys, copy
from queue import PriorityQueue

goal_state =  [[0,1,2],
               [3,4,5],
               [6,7,8]]

def main():
    p = EightPuzzle()
    p.set("724506831")
    #p.set("142375680")
    print("initial:: \n")
    print(p)
    print("solving:: \n")
    p.solve()

class Node:
    def __init__(self):
        self.heuristic = 0
        self.f = 0
        self.depth = 0
        self.parent_matrix = []
        self.moves = 0

    def printPuzzle(self):
        print('')
        print(self.parent_matrix[0][0], self.parent_matrix[0][1], self.parent_matrix[0][2])
        print(self.parent_matrix[1][0], self.parent_matrix[1][1], self.parent_matrix[1][2])
        print(self.parent_matrix[2][0], self.parent_matrix[2][1], self.parent_matrix[2][2])
        print("\n")

    def setPuzzle(self, puzzle):
        self.parent_matrix = puzzle

class Queue(object):
    def __init__(self, priority, object):
        self.priority = priority
        self.object = object



class EightPuzzle:
    def __init__(self):
        self.goal_sate = goal_state
        # heuristic value
        self.h_val = 0
        # search depth of current instance
        self.depth = 0
        # parent node in search path
        self.parent = None
        self.search_matrix = []

        for i in range(3):
            self.search_matrix.append(goal_state[i][:])

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.search_matrix[row]))
            res += '\r\n'
        return res

    def show(self, puz):
        print('')
        print(puz[0][0], puz[0][1], puz[0][2])
        print(puz[1][0], puz[1][1], puz[1][2])
        print(puz[2][0], puz[2][1], puz[2][2])
        print("\n")


    def set(self, other):
        i=0;
        for row in range(3):
            for col in range(3):
                self.search_matrix[row][col] = int(other[i])
                i=i+1

    def check_solved(self, puzzle):
        # check if puzzle has been solved
        return self.goal_sate == puzzle

    def all(checkarray, queue):
        for i in range(len(queue)):
            for new_node in checkarray:
                if new_node.parent_matrix == queue[i].parent_matrix:
                    checkarray.remove(new_node)

        return checkarray



    def expandMoves(self, possible_moves, index_0, parent_node):
        new_puzzle_state = []
        temp_puzzle = []
        temp_index_swap = 0
        for i in possible_moves:
            temp_puzzle = copy.deepcopy(parent_node)
            temp_index_swap = temp_puzzle.parent_matrix[i[0]][i[1]]
            temp_puzzle.parent_matrix[i[0]][i[1]] = 0
            temp_puzzle.parent_matrix[index_0[0]][index_0[1]] = temp_index_swap
            new_puzzle_state.append(temp_puzzle)

        return new_puzzle_state

    def sort(queue):
        for passesLeft in range(len(queue)-1, 0, -1):
            for index in range(passesLeft):
                if (queue[index].f >  (queue[index + 1].f)):
                    queue[index], queue[index + 1] = queue[index + 1], queue[index]

        # for index in range(len(queue)):
        #     if (queue[index].f) > (queue[index + 1].f):
        #         queue[index], queue[index + 1] = queue[index + 1], queue[index]

        return queue

    def calculateManhattan(initial_state):
        man_dist = 0
        # search through the numbers in the puzzle
        for index in range(9):
            for i in range(3):
                for j in range(3):
                    # get where the number should be
                    if (index == goal_state[i][j]):
                        goalRow = i
                        goalCol = j
                    # get where the number is now
                    if (index == initial_state[i][j]):
                        puzzleRow = i
                        puzzleCol = j
            # calculate the Manhattan Distance based on the points (row/col)
            man_dist += ( abs(goalRow - puzzleRow) + abs(goalCol - puzzleCol) )

        return man_dist

    def solve(self):
        nodesExpanded = 0
        maxQueueSize = 0
        queue = []
        ## initial set of the main node
        node = Node()
        node.setPuzzle(self.search_matrix)
        node.depth = 0
        node.heuristic = EightPuzzle.calculateManhattan(node.parent_matrix)
        node.f = node.heuristic + node.depth
        queue.append(node)

        while True:
            if (len(queue) == 0):
                print("Puzzle search exhausted")
                sys.exit(0)

            print("Initializing : __ :")

            new_init_node = Node()
            new_init_node.setPuzzle(queue[0].parent_matrix)
            new_init_node.heuristic = queue[0].heuristic
            new_init_node.depth = queue[0].depth
            new_init_node.f = queue[0].f
            new_init_node.moves = queue[0].moves+1

            if (EightPuzzle.check_solved(self, new_init_node.parent_matrix)):
                # then print solution and return
                print (''
                 "Solution found!!")
                new_init_node.printPuzzle()
                print ('')
                print ("Expanded a total of", nodesExpanded, "nodes")
                print ("Maximum number of nodes in the queue was", maxQueueSize)
                print ("The depth of the goal node was", new_init_node.depth)
                print("Moves ===", new_init_node.moves)
                return

            print ('')
            print ("The best node to expand with g(n) =", new_init_node.depth, \
                  "and h(n) =", new_init_node.heuristic, "is... F = ", new_init_node.f)

            new_init_node.printPuzzle()
            ## remove the top fo the queue as node is beibg explored
            queue.pop(0)

            p_moves, index = EightPuzzle.possibleMoves(self, new_init_node)
            #list of possible moves
            expand_nodes = EightPuzzle.expandMoves(self, p_moves, index, new_init_node)
            dup_out = EightPuzzle.all(expand_nodes, queue)
            if len(dup_out) != 0:
                #print("possible moves \n")
                for nodes in dup_out:
                    #EightPuzzle.show(self, nodes.parent_matrix)
                    if (EightPuzzle.check_solved(self, nodes.parent_matrix)):
                        # then print solution and return
                        print (''
                         "Solution found!!")
                        nodes.printPuzzle()
                        print ('')
                        print ("Expanded a total of", nodesExpanded, "nodes")
                        print ("Maximum number of nodes in the queue was", maxQueueSize)
                        print ("The depth of the goal node was", nodes.depth)
                        print("Moves ===", nodes.moves)
                        return
                    temp_new_node = Node()
                    temp_new_node.setPuzzle(nodes.parent_matrix)
                    temp_new_node.heuristic = EightPuzzle.calculateManhattan(temp_new_node.parent_matrix)
                    # every time you expand, you add a depth
                    temp_new_node.depth = nodes.depth + 1
                    temp_new_node.f = temp_new_node.heuristic + temp_new_node.depth
                    temp_new_node.moves += 1
                    # and then add it to the queue, of course
                    queue.append(temp_new_node)

                    nodesExpanded += 1

                    if(len(queue) > maxQueueSize):
                        maxQueueSize = len(queue)

            print(nodesExpanded)
            queue = EightPuzzle.sort(queue)
            print("Proceeding with node::")
            a = queue[0]
            a.printPuzzle()



    def possibleMoves(self, node):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and column of the empty piece
        possible_m = []
        matrix = node.parent_matrix
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




if __name__ == "__main__":
    main()
