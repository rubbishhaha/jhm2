import set
import time,os
os.system('cls' if os.name == 'nt' else 'clear')
inputing = True
while inputing:
    try:
        pnum = int(input("  WELCOME TO GHOST LEG !\n\nPlease type the number of player:"))
        rnum = int(input("Please type the number of row:"))
        player = set.set_player(pnum)
        board  = set.set_board(pnum,rnum)
        max_round = int(input("Please type the number of round:"))
        if max_round > pnum*rnum/2:
            print("the number of round is too large, please try again")
            break
        inputing = False
    except:
        print("Invalid input. Please try again")

os.system('cls' if os.name == 'nt' else 'clear')
print("---GAME START---")
time.sleep(1)
round = 0

while round < max_round:
    os.system('cls' if os.name == 'nt' else 'clear')
    set.board_show(board,round+1)
    access = False
    while access == False:
        try:
            board,access = set.add_line(board,int(input("column:"))-1,int(input("row:"))-1)
        except:
            stop = input("Invalid input. Please try again")
            if stop == "n":
                round += 10000
                access = True
                print("sodnf")
        if access == False:
            print("sorry! Line can not overlap with each other or itself. Please try another line.")
    round += 1

os.system('cls' if os.name == 'nt' else 'clear')
print("---GAME END---")
time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')
set.board_show(board,-1)
set.result_print(board,player)
input()