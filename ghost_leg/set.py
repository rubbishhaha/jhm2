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
    for i in range(Pnum):
        a.append({})
        for u in range(rnum):
            a[i][u] = BLANK
    return a
def board_show(board):
    for row in range(len(board[0])):
        for column in range(len(board)):
            print(COLUMN,end="")
            print(board[column][row],end="")
        print(COLUMN)
def add_line(player,board,column,row):
    board[column][row] = LINE
    for r in range(len(board[0])):
        for c in range(len(board)):
            if board[c][r] == LINE:
                print("zazazazazazazaazazazzaaza")
    return player,board