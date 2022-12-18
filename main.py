class Node:
    def __init__(self, id, parent, answer): self.up, self.right, self.down, self.left, self.parent, self.name, self.id, self.answer = None, None, None, None, parent, "n", id, answer
    def __repr__(self): return f"N{self.id}"

class Header:
    def __init__(self, id): self.up, self.right, self.down, self.left, self.total_1, self.name, self.id, self.parent = None, None, None, None, 0, "h", id, self

    def __repr__(self): return f"H{self.id}"

def create_nodes(id1, id2, id3, id4, header_list, copy_list, answer):
    p1, p2, p3, p4 = header_list[id1], header_list[id2], header_list[id3], header_list[id4]
    n1, n2, n3, n4 = Node(id1, p1, answer), Node(id2, p2, answer), Node(id3, p3, answer), Node(id4, p4, answer)
    u1, u2, u3, u4 = copy_list[id1], copy_list[id2], copy_list[id3], copy_list[id4]

    p1.total_1, p2.total_1, p3.total_1, p4.total_1, = p1.total_1 + 1, p2.total_1 + 1, p3.total_1 + 1, p4.total_1 + 1
    
    n1.right, n2.right, n3.right, n4.right = n2, n3, n4, n1
    n1.left, n2.left, n3.left, n4.left = n4, n1, n2, n3

    u1.down, u2.down, u3.down, u4.down = n1, n2, n3, n4
    n1.up, n2.up, n3.up, n4.up = u1, u2, u3, u4

    p1.up, p2.up, p3.up, p4.up, = n1, n2, n3, n4
    n1.down, n2.down, n3.down, n4.down = p1, p2, p3, p4

    copy_list[id1], copy_list[id2], copy_list[id3], copy_list[id4] = n1, n2, n3, n4


def initialize_nodes(board):
    header_list = [Header(x) for x in range(324)]
    copy_list = [x for x in header_list]
    numbers = {x for x in range(10)}
    row_pos = [numbers.difference(set(x)) for x in board]
    col_pos = [numbers.difference(set(board[a][x] for a in range(9))) for x in range(9)]
    block_pos = [numbers.difference(set(el for part in board[x:x + 3] for el in part[y: y + 3])) for x in range(0,9,3) for y in range(0,9,3)]
    for i in range(9):
        for j in range(9):
            if board[i][j]: continue
            k = (i // 3) * 3 + (j // 3)
            poses = row_pos[i] & col_pos[j] & block_pos[k]
            for pos in poses:
                cell_index = i * 9 + j
                row_index = 80 + i * 9 + pos
                col_index = 161  + j * 9 + pos
                block_index = 242 + k * 9 + pos
                create_nodes(cell_index, row_index, col_index, block_index, header_list, copy_list, (i,j,pos))

    header_list = [x for num,x in enumerate(header_list) if copy_list[num].name == "n"]
    before = initial = Header(-1)
    for current in header_list:
        before.right = current
        current.left = before
        before = current

    before.right = initial
    initial.left = before
    return initial
    
def get_min_col(initial):
    before = min_node = initial.right
    while before.right != initial:
        before = before.right
        if before.total_1 < min_node.total_1: min_node = before

    return min_node



    
def cover(node):
    before = col = node.parent
    col.left.right = col.right
    col.right.left = col.left
    while before.down.name != "h":
        current = before = before.down
        while current.right != before:
            current = current.right
            current.up.down = current.down
            current.down.up = current.up
            current.parent.total_1 += -1


def uncover(node):
    before = col = node.parent
    while before.up.name != "h":
        current = before = before.up
        while current.left != before:
            current = current.left
            current.up.down = current
            current.down.up = current
            current.parent.total_1 += 1
    
    col.left.right = col
    col.right.left = col

        
def DLX(solution, initial):
    if initial.right == initial: return True
    node = col = get_min_col(initial)
    cover(col)
    while node.down.name != "h": 
        current = node = node.down
        solution.add(node)
        while current.right != node:
            current = current.right
            cover(current)
        
        if DLX(solution, initial): return True
        current = node
        solution.remove(node)
        while current.left != node:
            current = current.left
            uncover(current)
    
    uncover(col)
        

def solve(board):
    initial = initialize_nodes(board)
    result = set()
    DLX(result, initial)
    for el in result:
        i,j,k = el.answer
        board[i][j] = k
    
    return board
