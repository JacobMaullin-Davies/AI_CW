import sys, copy
goal_state =  [[0,1,2],
               [3,4,5],
               [6,7,8]]


def main():
     puzzle = EightPuzzle()
     puzzle.set("724506831")
     #puzzle.set("142375680")
     #puzzle.set("123045678")
     #puzzle.set("1253406789")
     print("initial:: \n")
     puzzle.show()
     print("solving:: \n")
     puzzle.solve()

def show(puzzle):
    print('')
    print(puzzle[0][0],puzzle[0][1],puzzle[0][2])
    print(puzzle[1][0],puzzle[1][1],puzzle[1][2])
    print(puzzle[2][0],puzzle[2][1],puzzle[2][2])
    print("\n")

def checkSolved(path_node):
    return path_node.matrix == goal_state

def manhattanDistance(search, goal):
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
        # calculate the Manhattan Distance based on the points (row/col)
        man_dist += (abs(goal_row - puzzle_row) + abs(goal_col - puzzle_col))
    return man_dist

def possibleMoves(matrix_search):
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
    return node.fn

def in_list(node, closed_nodes):
    for c_nodes in closed_nodes:
        if node == c_nodes.matrix:
            return True

def add_queue(new_path, Queue):
    for node in Queue:
        if new_path.matrix == node.matrix and node.fn >= new_path.fn:
            return False
    return True

class Node:
    def __init__(self):
        self.gn = 0
        self.hn = 0
        self.moves = 0
        self.matrix = []
        self.fn = 0
        self.path = []

    def setPuzzle(self, puzzle):
        self.matrix = puzzle

    def set_fn(self):
        self.fn = self.gn + self.hn


class EightPuzzle:
    def __init__(self):
        self.search_matrix = [[0,0,0],[0,0,0],[0,0,0]]
        self.goal_matrix = goal_state

    def set(self, other):
        i=0;
        for row in range(3):
            for col in range(3):
                self.search_matrix[row][col] = int(other[i])
                i=i+1

    def show(self):
        print('')
        print(self.search_matrix[0][0], self.search_matrix[0][1], self.search_matrix[0][2])
        print(self.search_matrix[1][0], self.search_matrix[1][1], self.search_matrix[1][2])
        print(self.search_matrix[2][0], self.search_matrix[2][1], self.search_matrix[2][2])
        print("\n")

    def expandMoves(self, possible_moves, index_0, parent_node):
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

    def sort(queue):
        for passesLeft in range(len(queue)-1, 0, -1):
            for index in range(passesLeft):
                if (queue[index].fn >  (queue[index + 1].fn)):
                    queue[index], queue[index + 1] = queue[index + 1], queue[index]

        return queue

    def solve(self):
        self.parent = 0
        self.gn = 0
        self.hn = manhattanDistance(self.search_matrix, self.goal_matrix)
        nodesExpanded = 0
        maxQueueSize = 0

        priority_queue = []
        closed_nodes = []

        initial_node = Node()
        initial_node.setPuzzle(self.search_matrix)
        initial_node.hn = self.hn
        initial_node.gn = -1



        priority_queue.append(initial_node)

        while 1:
            if (len(priority_queue) == 0):
                print("Puzzle search exhausted")
                sys.exit(0)

            path_node = Node()
            path_node.setPuzzle(priority_queue[0].matrix)
            path_node.hn = priority_queue[0].hn
            path_node.gn = priority_queue[0].gn
            path_node.moves = priority_queue[0].moves
            path_node.path = priority_queue[0].path
            path_node.set_fn()


            current_node = priority_queue[0]
            closed_nodes.append(current_node)
            priority_queue.pop(0)


            print("Going with path node: \n")
            show(path_node.matrix)

            if checkSolved(path_node):
                print("Solved")
                print("In moves: ")
                print(path_node.moves)
                print("Solution: ")
                path_node.path.append(self.goal_matrix)
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
                new_path.hn = manhattanDistance(new_path.matrix, self.goal_matrix)
                new_path.gn = path_node.gn + 1
                new_path.moves = path_node.moves + 1
                new_path.path = copy.deepcopy(path_node.path)
                new_path.path.append(path_node.matrix)
                new_path.set_fn()
                if add_queue(new_path, priority_queue):
                    priority_queue.append(new_path)
                    nodesExpanded += 1

            if(len(priority_queue) > maxQueueSize):
                maxQueueSize = len(priority_queue)
            priority_queue.sort(key=heuristic)
            print("fn",priority_queue[0].fn)
            print("man val", priority_queue[0].hn)
            print("depth", priority_queue[0].gn)
            print(nodesExpanded)
            print(maxQueueSize)

if __name__ == "__main__":
    main()
