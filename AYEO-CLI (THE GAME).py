import random
import time
import sys
import json

# Global variables # Global variables

save_file = 'bingo_game_state.txt'
Numbers1 = []  # List to store numbers for the first table
Numbers2 = []  # List to store numbers for the second table
Game_Table1 = []
Game_Table2 = []
Computer = "Computer"
Table_Numbers = []
count1 = 0
count2 = 0
count3 = 0
result1_str = ""
result2_str = ""
result3_str = ""
User_Name = ""
Com_or_Friend = 0
continuity = 'yes'
friend_name = ""

def save_game_state():
    game_state = {
        'User_Name': User_Name,
        'Com_or_Friend': Com_or_Friend,
        'friend_name': friend_name,
        'count1': count1,
        'count2': count2,
        'count3': count3,
        'result1_str': result1_str,
        'result2_str': result2_str,
        'result3_str': result3_str,
        'Table_Numbers': Table_Numbers,
        'Game_Table1': Game_Table1,
        'Game_Table2': Game_Table2,
        'Dimension': Dimension
    }
    for key, value in game_state.items():
        if callable(value):
            game_state[key] = str(value)

    # Write the game state to the file
    with open('bingo_game_state.txt', 'w') as f1:
        f1.write(json.dumps(game_state))

def load_game_state():
    try:
        with open('bingo_game_state.txt', 'r') as f1:
            game_state = json.loads(f1.read())
            global User_Name, Com_or_Friend, count1, count2, count3, User_Result, Com_Result, friend_result_str, Table_Numbers, Game_Table1, Game_Table2, Game_Table3, Dimension, friend_name
            User_Name = game_state.get('User_Name', '')
            Com_or_Friend = game_state.get('Com_or_Friend', 0)
            friend_name = game_state.get('friend_name', '')
            count1 = game_state.get('count1', 0)
            count2 = game_state.get('count2', 0)
            count3 = game_state.get('count3', 0)
            result1_str = game_state.get('result1_str', 0)
            result2_str = game_state.get('result2_str', 0)
            result3_str = game_state.get('result3_str', 0)
            Table_Numbers = game_state.get('Table_Numbers', 0)
            Game_Table1 = game_state.get('Game_Table1', 0)
            Game_Table2 = game_state.get('Game_Table2', 0)
            Dimension = game_state.get('Dimension', 0)
            if (count1 or count2 or count3)>=5:
                count1 = 0 

            else:

                # Load other important variables
                print("Game state loaded successfully.")
                print(f"Resuming game for {User_Name}")
                print(f"{User_Name}'s Table:")
                print_table(Game_Table1)
                Table1_is_bingo()
                if Com_or_Friend == "friend":
                    print(f"{friend_name}'s Table:")
                    print_table(Game_Table2)
                    Table3_is_bingo()
                if Com_or_Friend == "computer":
                    print("Computer's Table:")
                    print_table(Game_Table2)
                    Table2_is_bingo()

    except FileNotFoundError:
        pass
    return count3,count2,count1

def Number_Set(Numbers):
    start = 0
    for i in range(1, Dimension + 1):
        for j in range(1, Dimension + 1):
            start += 1
            Numbers.append(start)

def Numbers():
    Number_Set(Numbers1)
    Number_Set(Numbers2)

def Table(Game_Table, Numbers, Name):
    for i in range(Dimension):
        Game_Table.append([])
        for j in range(Dimension):
            number = random.choice(Numbers)
            Game_Table[i].append(number)
            Numbers.remove(number)
    print(f"{Name}'s Table:")
    for i in range(len(Game_Table)):
        print(" ".join(str(num).rjust(4) for num in Game_Table[i]))
    return Game_Table

def Game_Numbers():
    start = 0
    for i in range(1, Dimension + 1):
        for j in range(1, Dimension + 1):
            start += 1
            Table_Numbers.append(start)


def Change_num_to_x_in_both_tables(first_Game_Table, second_Game_Table, number):
    for i in range(len(first_Game_Table)):
        for j in range(len(first_Game_Table)):
            if first_Game_Table[i][j] == number:
                first_Game_Table[i][j] = "x"
    for i in range(len(second_Game_Table)):
        for j in range(len(second_Game_Table)):
            if second_Game_Table[i][j] == number:
                second_Game_Table[i][j] = "x"


def exiting():
    print('exiting....')
    time.sleep(1)
    sys.exit(1)

def restart():
    time.sleep(1)
    main()



# Change a user-selected number to 'x' in the tables
def Change_user_num_to_x():
    # Asks the user to enter a number
    while True:
        user_input = input("Enter your number...")
        if user_input.lower() == "exit":
            exiting()
        elif user_input.lower()=="restart":
            restart()
        else:
            try:
                num = int(user_input)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    while num not in Table_Numbers:
        print(f"Valid Numbers: {Table_Numbers}")
        while True:
            try:
                num = int(input("Enter a valid number..."))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    Table_Numbers.remove(num)
    Change_num_to_x_in_both_tables(Game_Table1, Game_Table2, num)
    print(f"{User_Name}'s Table:")
    for i in range(len(Game_Table1)):
        print(" ".join(str(num).rjust(4) for num in Game_Table1[i]))
    Table1_is_bingo()
    print("Computer's Table:")
    for i in range(len(Game_Table2)):
        print(" ".join(str(num).rjust(4) for num in Game_Table2[i]))
    Table2_is_bingo()
    save_game_state()

def print_table(game_table):
    for row in game_table:
        print(" ".join(str(cell).rjust(4) for cell in row))

def Change_com_num_to_x():
    def check_for_win(game_table, num):
        for i in range(Dimension):
            if all(item == "x" for item in game_table[i]) or all(game_table[j][i] == "x" for j in range(Dimension)):
                return True

        if all(game_table[i][i] == "x" for i in range(Dimension)) or all(
                game_table[i][Dimension - 1 - i] == "x" for i in range(Dimension)):
            return True
        return False

    def evaluate_move(game_table, num):
        temp_game_table = [row[:] for row in game_table]

        temp_game_table = [row[:] for row in Game_Table2]
        for i in range(len(temp_game_table)):
            for j in range(len(temp_game_table[i])):
                if temp_game_table[i][j] == num:
                    temp_game_table[i][j] = "x"
                    if check_for_win(temp_game_table, num):
                        return "win"

        return "other"

    for num in Table_Numbers:
        move_evaluation = evaluate_move(Game_Table2, num)
        if move_evaluation == "win":
            Table_Numbers.remove(num)
            Change_num_to_x_in_both_tables(Game_Table1, Game_Table2, num)
            print(f"Computer chose {num} ")
            print(f"{User_Name}'s Table:")
            print_table(Game_Table1)
            Table1_is_bingo()
            print("Computer's Table:")
            print_table(Game_Table2)
            Table2_is_bingo()
            save_game_state()
            return

    num = random.choice(Table_Numbers)
    Table_Numbers.remove(num)
    Change_num_to_x_in_both_tables(Game_Table1, Game_Table2, num)
    print(f"Computer chose {num}")
    print(f"{User_Name}'s Table:")
    print_table(Game_Table1)
    Table1_is_bingo()
    print("Computer's Table:")
    print_table(Game_Table2)
    Table2_is_bingo()
    save_game_state()

def Change_user_with_friend_num_to_x():
    while True:
        user_input = input(f"{User_Name}, Enter your number...")
        if Dimension.lower() == "exit":
            exiting()
        try:
            num = int(user_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while num not in Table_Numbers:
        print(f"Valid Numbers: {Table_Numbers}")
        while True:
            try:
                num = int(input("Enter a valid number..."))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    Table_Numbers.remove(num)
    Change_num_to_x_in_both_tables(Game_Table1, Game_Table2, num)

    print(f"{User_Name}'s Table:")
    for i in range(len(Game_Table1)):
        print(" ".join(str(num).rjust(4) for num in Game_Table1[i]))
    Table1_is_bingo()

    print(f"{friend_name}'s Table:")
    for i in range(len(Game_Table2)):
        print(" ".join(str(num).rjust(4) for num in Game_Table2[i]))
    Table3_is_bingo()
    
    save_game_state()  

def Change_friend_num_to_x():
    while True:
        user_input = input("Enter your number...")
        if user_input.lower() == "exit":
            exiting()
        elif user_input.lower() == "restart":
            restart()
        else:
            try:
                num = int(user_input)
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    while num not in Table_Numbers:
        print(f"Valid Numbers: {Table_Numbers}")
        while True:
            try:
                num = int(input("Enter a valid number..."))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    Table_Numbers.remove(num)
    Change_num_to_x_in_both_tables(Game_Table1, Game_Table2, num)

    print(f"{User_Name}'s Table:")
    for i in range(len(Game_Table1)):
        print(" ".join(str(num).rjust(4) for num in Game_Table1[i]))
    Table1_is_bingo()

    print(f"{friend_name}'s Table:")
    for i in range(len(Game_Table2)):
        print(" ".join(str(friend_num).rjust(4) for friend_num in Game_Table2[i]))
    Table3_is_bingo()
    
    save_game_state() 

def count_bingo_lines(game_table, count):
    for i in range(Dimension):
        if all(item == "x" for item in game_table[i]):
            count += 1
        if all(game_table[j][i] == "x" for j in range(Dimension)):
            count += 1
    if all(game_table[i][i] == "x" for i in range(Dimension)):
        count += 1
    if all(game_table[i][Dimension - 1 - i] == "x" for i in range(Dimension)):
        count += 1
    return count

def Table1_is_bingo():
    global count1
    count1 = 0
    count1 = count_bingo_lines(Game_Table1, count1)
    if count1 > 0 and count1 <= Dimension:
        Result(count1, result1_str)
        print(f"{User_Name}'s score is: {Result(count1, result1_str)}")

def Table2_is_bingo():
    global count2
    count2 = 0
    count2 = count_bingo_lines(Game_Table2, count2)
    if count2 > 0 and count2 <= Dimension:
        Result(count2, result2_str)
        print(f"Computer's score is: {Result(count2, result2_str)}")

def Table3_is_bingo():
    global count3
    count3 = 0
    count3 = count_bingo_lines(Game_Table2, count3)
    if count3 > 0 and count3 <= Dimension:
        Result(count3, result3_str)
        print(f"{friend_name}'s score is: {Result(count3, result3_str)}")

def Result(count, result_str):
    if count == 1:
        result_str = "B"
    elif count == 2:
        result_str = "BI"
    elif count == 3:
        result_str = "BIN"
    elif count == 4:
        result_str = "BING"
    elif count == 5:
        result_str = "BINGO"
    return result_str

def take_dimensions():
    global Dimension
    while True:
        try:
            Dimension = (input(f"{User_Name}, Do you want to play with default dimensions (5x5) or do you want customized dimensions (larger than 5) (Default), (Custom): "))
            if Dimension.lower() == "exit":
                exiting()
            if Dimension.lower() == 'default':
                Dimension = 5
                break
            elif Dimension == 'custom':
                while True:
                    try:
                        Dimension = int(input("Enter the dimension you need (must be equal to or larger than 5): "))
                        if Dimension >= 5:
                            break
                        else:
                            print("Please enter dimensions equal to or larger than 5.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                break
            elif Dimension == 'exit':
                save_game_state()
                exiting()
            elif Dimension == "restart":
                reset_game_state()
                restart()
            else:
                print("Please enter either default or custom")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def ask_for_continuity(first_Game_Table, second_Game_Table):
    while True:
        try:
            continuity = (input("Do you want to play again (yes,no): "))
            if continuity in ('yes', 'no'):
                if continuity.lower() == ('yes'):
                    Table_Numbers.clear()
                    first_Game_Table.clear()
                    second_Game_Table.clear()
                    count1 = 0
                    count2 = 0
                    main()
                elif continuity.lower() == ('no'):
                    save_game_state()
                    print("Exiting...")
                    time.sleep(1)
                    sys.exit(1)
                break
        except ValueError:
            print("Invalid input.  ")
        break

def is_game_vs_computer_done():
    global count1
    global count2
    if count1 >= 5 and count2 >= 5:
        print(f"Draw, Good job {User_Name} but you need to practice more")
        ask_for_continuity(Game_Table1, Game_Table2)
    elif count1 >= 5:
        print(f"Congratulaions {User_Name}, You Won")
        ask_for_continuity(Game_Table1, Game_Table2)
    elif count2 >= 5:
        print("Computer Won, Wanna lose again ?")
        ask_for_continuity(Game_Table1, Game_Table2)

def is_game_vs_friend_done():
    global count1
    global count3
    if count1 >= 5 and count3 >= 5:
        print(f"Draw, Good job {User_Name} and {friend_name}")
        ask_for_continuity(Game_Table1, Game_Table2)
    elif count1 >= 5:
        print(f"Congratulaions {User_Name}, {friend_name} wanna lose again?")
        ask_for_continuity(Game_Table1, Game_Table2)
    elif count3 >= 5:
        print(f"Congratulaions {friend_name}, {User_Name} wanna lose again?")
        ask_for_continuity(Game_Table1, Game_Table2)

def playing_vs_computer_progress():
    global count1
    global count2
    while count1 < Dimension and count2 < Dimension:
        Change_user_num_to_x()
        is_game_vs_computer_done()
        print("Wait till Computer think....")
        time.sleep(1.5)
        Change_com_num_to_x()
        is_game_vs_computer_done()

    # These lines should be inside the while loop
    Game_Table1.clear()
    Game_Table2.clear()
    count1 = 0
    count2 = 0

    # clear game tables and reset the count



# function to make the steps of playing vs computer
def playing_vs_friend_progress():
    global count1
    global count3
    while count1 < Dimension and count3 < Dimension:
        Change_user_with_friend_num_to_x()
        is_game_vs_friend_done()
        Change_friend_num_to_x()
        is_game_vs_friend_done()
    Game_Table1.clear()
    Game_Table2.clear()
    count1 = 0
    count3 = 0

    # clear game tables and reset the count

def reset_game_state():
    global count1, count2, count3, Game_Table1, Game_Table2, Dimension
    count1 = 0
    count2 = 0
    count3 = 0
    Game_Table1.clear()
    Game_Table2.clear()
    Dimension = 0
    

while True:
    try:
        Reload_option = input('Do you want to reload the previous game? (yes, no): ')
        if Reload_option.lower() in ['yes', 'no', 'exit']:
            break
        else:
            print('Invalid entry. Please enter either "yes" or "no".')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

            
# the main function to play the game
def main():
    global User_Name
    global Com_or_Friend
    global continuity
    global friend_name
    global count1
    global count2
    global count3
    global Reload_option


    while True:
        if Reload_option.lower() == 'yes':
            Reload_option = "AYEO"
            load_game_state()  # Load the game state
            if (count3 or count2 or count1) >= 5:
                print('Game is already finished')

                while True:
                    try:
                        replay = input("Do you want to replay? (yes/no): ")
                        if replay.lower() == 'yes':
                            Game_Table1.clear()
                            Game_Table2.clear()
                            count1 = 0
                            count2 = 0
                            count3 = 0
                            main()
                        elif replay.lower() == 'no':
                            print('Exiting....')
                            time.sleep(1)
                            sys.exit(0)
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")
                    except Exception as e:
                        print(f"An error occurred: {e}")

            else:
                if Com_or_Friend.lower() == 'computer':
                    playing_vs_computer_progress()
                elif Com_or_Friend.lower() == 'friend':
                    playing_vs_friend_progress()
                        
        elif Reload_option.lower() == 'exit':
            print("Exiting.")
            time.sleep(1)
            sys.exit()

        print('Initiating a game')
        User_Name = input("Hello, enter your name: ")
        print(f"Hello {User_Name}, do you want to play against the computer or against your friend:")

        while True:
            try:
                Com_or_Friend = input("Computer, Friend: ")
                if Com_or_Friend.lower() in ['computer', 'friend']:
                    break
                else:
                    print("Please enter either friend or computer.")
            except ValueError:
                print("Invalid input. Please enter a valid value.")

        reset_game_state()
            
        continuity = 'yes'
        while continuity.lower() != 'no':
            Game_Table1.clear()
            Game_Table2.clear()
            count1 = 0
            count2 = 0
            count3 = 0
            if Com_or_Friend.lower() == 'computer':
                take_dimensions()
                Numbers()
                Game_Numbers()
                Table(Game_Table1, Numbers1, User_Name)
                Table(Game_Table2, Numbers2, Computer)
                playing_vs_computer_progress()
            elif Com_or_Friend.lower() == 'friend':
                friend_name = input("Enter your friend's name: ")
                print(f"Hello {friend_name}")
                take_dimensions()
                Numbers()
                Game_Numbers()
                Table(Game_Table1, Numbers1, User_Name)
                Table(Game_Table2, Numbers2, friend_name)
                playing_vs_friend_progress()
            break  

if __name__ == '__main__':
    main()
# End of game script