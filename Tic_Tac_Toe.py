import random
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="tic_tac_toe"
)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Game_Results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Game_Mode VARCHAR(255),
                Player_x VARCHAR(255),
                Player_o VARCHAR(255),
                Winner VARCHAR(255),
                Date TIMESTAMP
            )''')
conn.commit()

Board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
Game_Current_Player = "X"
Game_Winner = None
Game_Running = True
Player_X_Name = ""
Player_O_Name = ""
Current_Player_Name = ""

def Game_Print_Board(Board):
    print(f"{Board[0]} | {Board[1]} | {Board[2]}")
    print("---------")
    print(f"{Board[3]} | {Board[4]} | {Board[5]}")
    print("---------")
    print(f"{Board[6]} | {Board[7]} | {Board[8]}")

def Game_Input(Board):
    global Current_Player_Name
    valid_input = False
    while not valid_input:
        try:
            inp = int(input(f"Player {Current_Player_Name}, select a spot 1-9: "))
            if inp < 1 or inp > 9:
                print("Invalid input. Please select a spot within 1-9.")
            elif Board[inp-1] != "-":
                print("Oops, that spot is already taken.")
            else:
                Board[inp-1] = Game_Current_Player
                valid_input = True
        except ValueError:
            print("Invalid input. Please enter a number.")
def Game_Input_Two_Player(Board):
    global Current_Player_Name
    valid_input = False
    while not valid_input:
        try:
            inp = int(input(f"Player {Current_Player_Name}, select a spot 1-9: "))
            if inp < 1 or inp > 9:
                print("Invalid input. Please select a spot within 1-9.")
            elif Board[inp-1] != "-":
                print("Oops, that spot is already taken.")
            else:
                Board[inp-1] = Game_Current_Player
                valid_input = True
        except ValueError:
            print("Invalid input. Please enter a number.")
def Computer_Move(Board):
    available_spots = [index for index, value in enumerate(Board) if value == "-"]
    move = random.choice(available_spots)
    Board[move] = Game_Current_Player
def checkHorizontal(Board):
    global Game_Winner
    if Board[0] == Board[1] == Board[2] and Board[0] != "-":
        Game_Winner = Board[0]
        return True
    elif Board[3] == Board[4] == Board[5] and Board[3] != "-":
        Game_Winner = Board[3]
        return True
    elif Board[6] == Board[7] == Board[8] and Board[6] != "-":
        Game_Winner = Board[6]
        return True
def checkVertical(Board):
    global Game_Winner
    if Board[0] == Board[3] == Board[6] and Board[0] != "-":
        Game_Winner = Board[0]
        return True
    elif Board[1] == Board[4] == Board[7] and Board[1] != "-":
        Game_Winner = Board[1]
        return True
    elif Board[2] == Board[5] == Board[8] and Board[2] != "-":
        Game_Winner = Board[2]
        return True
def checkDiagonal(Board):
    global Game_Winner
    if Board[0] == Board[4] == Board[8] and Board[0] != "-":
        Game_Winner = Board[0]
        return True
    elif Board[2] == Board[4] == Board[6] and Board[2] != "-":
        Game_Winner = Board[2]
        return True
def Check_If_Win(Board):
    global Game_Running, Game_Winner
    if checkHorizontal(Board) or checkVertical(Board) or checkDiagonal(Board):
        Game_Print_Board(Board)
        Game_Winner = Player_X_Name if Game_Current_Player == "X" else Player_O_Name
        print(f"The winner is {Game_Winner}!")
        Game_Running = False
def Check_If_Tie(Board):
    global Game_Running
    if "-" not in Board:
        Game_Print_Board(Board)
        print("It's a tie!")
        Game_Running = False
def Game_Switch_Player():
    global Game_Current_Player, Current_Player_Name
    if Game_Current_Player == "X":
        Game_Current_Player = "O"
        Current_Player_Name = Player_O_Name
    else:
        Game_Current_Player = "X"
        Current_Player_Name = Player_X_Name
def Game_Reset_Board():
    global Board, Game_Current_Player, Game_Winner, Game_Running, Current_Player_Name
    Board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    Game_Current_Player = "X"
    Game_Winner = None
    Game_Running = True
    Current_Player_Name = Player_X_Name
def save_game_result(game_mode, player_x, player_o, winner):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO Game_Results (Game_Mode, Player_x, Player_o, Winner, Date) VALUES (%s, %s, %s, %s, %s)",
              (game_mode, player_x, player_o, winner, date))
    conn.commit()
def Play_Game(game_mode, player_x, player_o):
    global Game_Running, Game_Current_Player, Game_Winner, Player_X_Name, Player_O_Name, Current_Player_Name
    Player_X_Name = player_x
    Player_O_Name = player_o
    Current_Player_Name = Player_X_Name
    while Game_Running:
        Game_Print_Board(Board)
        if Game_Current_Player == "X":
            Game_Input(Board)
        else:
            if game_mode == "Single Player":
                Computer_Move(Board)
            else:
                Game_Input_Two_Player(Board)
        
        Check_If_Win(Board)
        Check_If_Tie(Board)
        
        if Game_Running:
            Game_Switch_Player()

    winner = Game_Winner if Game_Winner else "Tie"
    save_game_result(game_mode, player_x, player_o, winner)

while True:
    print("Welcome to Tic-Tac-Toe!!!")
    print("1. Single Player")
    print("2. Two Players")
    mode_choice = input("Choose Game Mode (1/2) :-  ")
    if mode_choice == "1":
        Game_Mode = "Single Player"
        player_x = input("Enter Player X name :- ")
        player_o = "Computer"
    elif mode_choice == "2":
        Game_Mode = "Two Players"
        player_x = input("Enter Player X name :- ")
        player_o = input("Enter Player O name :- ")
    else:
        print("Invalid choice. Please select 1 or 2.")
        continue
    
    Play_Game(Game_Mode, player_x, player_o)
    
    play_again = input("Do you want to play again??? (yes/no) :- ")
    if play_again.lower() == "no":
        print("Thanks For Playing Game!!!")
        break
    else:
        Game_Reset_Board()

conn.close()