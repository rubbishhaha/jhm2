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
    PLAYER_print(len(board)+1,"P")
    for row in range(len(board[0])):
        for u in range(4-len(str(row+1))):
            print(" ",end="")
        print(row +1,end="")
        for column in range(len(board)):
            print(COLUMN,end="")
            print(board[column][row],end="")
        print(COLUMN)
    PLAYER_print(len(board)+1,"C")
    if round != -1:
        print("round:",round)

def add_line(board,column,row):
    if column != len(board)-1:
        if board[column+1][row] == LINE:
            a1 = False
        else:
            a1 = True
    else:
        a1 = True

    if column != 0:
        if board[column-1][row] == LINE:
            a2 = False
        else:
            a2 = True
    else:
        a2 = True

    if board[column][row] == LINE:
        a3 = False
    else:
        a3 = True
    
    if  a1 == False or a2 == False or a3 == False:
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

def PLAYER_print(pnum,u):
    if u == "P":
        for o in range(pnum*3+6):
            print(" ",end="")
        print("PLAYER")
    print("    ",end="")
    for i in range(pnum):
        print(u,end="")
        print(i+1,end="")
        for l in range(6-len(str(i+1))):
            print(" ",end="")
        
    print("")
    if u == "C":
        for o in range(pnum*3+6):
            print(" ",end="")
        print("COLUMN")