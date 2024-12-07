import set
pnum = int(input("  WELCOME TO GHOST LEG !\n\nPlease type the number of player:"))
rnum = int(input("Please type the number of row:"))
player = set.set_player(pnum)
board  = set.set_board(pnum,rnum)
max_round = int(input("Please type the number of round:"))
print("---GAME START---")
round = 0
while round < max_round:
    set.board_show(board)
    player,board = set.add_line(player,board,int(input("column:"))-1,int(input("row:"))-1)
    print(player)
    round += 1