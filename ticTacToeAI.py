import math
import console_movement
from os import system, name
import random 

moves_x = []
moves_o = []
win = False
squares = [(2,5), (2,11), (2,17), (5,5), (5,11), (5,17), (8,5), (8,11), (8,17)]

def main():
    input("Let's play tic-tac-toe! Note: In this version you'll face an unbeatable AI, good luck!")
    play()

def drawBoard():
    print("Move the cursor with the arrow keys and press ENTER to make your play.")
    print("        |     |       ")
    print("        |     |       ")
    print("   _____|_____|_____  ")
    print("        |     |       ")
    print("        |     |       ")
    print("   _____|_____|_____  ")
    print("        |     |       ")
    print("        |     |       ")
    print("        |     |       ")

def clear():
    system("cls") if name == "nt" else system("clear")

def play():
    global win, moves_x, moves_o

    win = False
    round = 0
    moves_x.clear()
    moves_o.clear()
    available_moves = squares.copy()

    clear()
    drawBoard()
    console_movement.move_cursor(available_moves[0][0], available_moves[0][1])

    while(True):
        move = ()
        player = "X" if round % 2 == 0 else "O"
        playing_moves = moves_x if player == "X" else moves_o

        if player == "X":
            try:
                move = console_movement.run_cursor_movement()
            except KeyboardInterrupt:
                clear()
                print("Program terminated by User. Exiting...")
                break

        move = validate_coords(move) if player == "X" else ai_move(available_moves)
        if move is not None:
            console_movement.replace_at_position(player, move[0], move[1])
            available_moves.remove(move)
            round += 1

            if win_condition(playing_moves, move):
                console_movement.move_cursor(10, 0)
                input(f"Player {player} has won! Press ENTER to play again.")
                play()

            if (round == 9):
                console_movement.move_cursor(10, 0)
                input("It's a tie! Press ENTER to settle the score!")
                play()
            
            console_movement.move_cursor(available_moves[0][0], available_moves[0][1])


# verify cursor is in valid position and centers inputs 
def validate_coords(coords):
    match coords:
        case (x, y) if 3 <= coords[1] <= 7 and 1 <= coords[0] <= 3:
            coords = squares[0]
        case (x, y) if 9 <= coords[1] <= 13 and 1 <= coords[0] <= 3:
            coords = squares[1]
        case (x, y) if 15 <= coords[1] <= 19 and 1 <= coords[0] <= 3:
            coords = squares[2]
        case (x, y) if 3 <= coords[1] <= 7 and 4 <= coords[0] <= 6:
            coords = squares[3]
        case (x, y) if 9 <= coords[1] <= 13 and 4 <= coords[0] <= 6:
            coords = squares[4]
        case (x, y) if 15 <= coords[1] <= 19 and 4 <= coords[0] <= 6:
            coords = squares[5]
        case (x, y) if 3 <= coords[1] <= 7 and 7 <= coords[0] <= 9:
            coords = squares[6]
        case (x, y) if 9 <= coords[1] <= 13 and 7 <= coords[0] <= 9:
            coords = squares[7]
        case (x, y) if 15 <= coords[1] <= 19 and 7 <= coords[0] <= 9:
            coords = squares[8]
        case _:
            coords =  None
        
    if coords is None or coords in moves_x or coords in moves_o:
        return None
    else:
        moves_x.append(coords)
        return coords

def win_condition(plays, move):
    countLines = 0
    countColunms = 0

    if (5,11) in plays:
        if (2,5) in plays and (8,17) in plays or (2,17) in plays and (8,5) in plays:
            return True

    for i in plays:
        if i[0] == move[0]:
            countColunms += 1
        if i[1] == move[1]:
            countLines += 1
        if countLines == 3 or countColunms == 3:
            return True
    return False

def ai_move(available_moves):
    global moves_x, moves_o

    if len(available_moves) == 9:
        move = random.choice(available_moves)
    else:
        move = minimax(moves_o, available_moves, "O")["position"]

    moves_o.append(move)
    return move

def minimax(playing_moves, available_moves, playing):
    other_player = "O" if playing == "X" else "X"
    other_moves = moves_o if playing == "X" else moves_x

    # if the game was won in the last hypothetical round, return score
    if win_condition(other_moves, other_moves[len(other_moves)-1]):
        return {"position": None, "score": len(available_moves) +1 if playing == "X" else (-1 *(len(available_moves) +1))}
    
    # if game wasn't won and there are no more possible moves, it's a tie 
    elif len(available_moves) == 0:
        return {"position": None, "score": 0}
    
    if playing == "O":
        best = {"position": None, "score": -math.inf} # if ai is playing, maximize the score
    else:
        best = {"position": None, "score": math.inf} # if player is playing, minimize the score

    for possible_move in available_moves[:]:
        # simulate the move
        playing_moves.append(possible_move)
        available_moves.remove(possible_move)

        # recurse to simulate game after that move
        sim_score = minimax(other_moves, available_moves, other_player)
        
        # remove the simulated move
        playing_moves.pop()
        available_moves.append(possible_move)
        sim_score["position"] = possible_move

        # update the score dictionary
        if playing == "O":  # trying to maximize ai score
            if sim_score["score"] > best["score"]:
                best = sim_score
        else: # trying to minimize player score
            if sim_score["score"] < best["score"]:
                best = sim_score
    return best

main()    