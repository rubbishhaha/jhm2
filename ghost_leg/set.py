BLANK = "      "
LINE =  "------"
COLUMN = "|"
def set_player(Pnum):
    a = {}
    for i in range(Pnum):
        a[i] = i
    return a
def set_board(Pnum,rnum):
    a = []
    for i in range(Pnum-1):
        a.append({})
        for u in range(rnum):
            a[i][u] = BLANK
    return a
def board_show(board,round):
    COLUMN_print(len(board)+1)
    for row in range(len(board[0])):
        for column in range(len(board)):
            print(COLUMN,end="")
            print(board[column][row],end="")
        print(COLUMN)
    if round != -1:
        print("round:",round)
def add_line(board,column,row):
    if column != len(board):
        if board[column-1][row] == LINE:
            a1 = False
        else:
            a1 = True
    else:
        a1 = True

    if column != 0:
        if board[column+1][row] == LINE:
            a2 = False
        else:
            a2 = True
    else:
        a2 = True

    if board[column][row] == LINE:
        a3 = False
    else:
        a3 = True    
    
    if  a1 or a2 or a3 == False:
        access = False
    else:
        access = True
        board[column][row] = LINE
    return board,access

def result_print(board,player):
    for r in range(len(board[0])):
        for c in range(len(board)):
            if board[c][r] == LINE:
                a = int(player[c])
                player[c] = int(player[c+1])
                player[c+1] = a
    print("\n---RESULT---\n")
    for i in range(len(player)):
        print(f"column {i+1}: P{player[i]+1}")
    return player
def COLUMN_print(pnum):
    for i in range(pnum):
        print(f"P{i+1}     ",end="")
    print("")
