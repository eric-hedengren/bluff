import random


def turn():
    current_player = player_names[(current_turn-1)%len(player_names)]
    print("It's {player}'s turn".format(player=current_player))

    if current_turn != 1:
        print("{player} said there are {quantity}, {value}s".format(player=player_names[(current_turn-2)%len(player_names)], quantity=current_guess[0], value=current_guess[1]))

    for player_name in player_data:
        if player_data[player_name][0] == []:
            if player_name != current_player:
                print("{player} has not revealed any dice and has {number} hidden dice".format(player=player_name, number=len(player_data[player_name][1])))
            else:
                print("You haven't revealed any dice and have {dice} hidden".format(dice=player_data[player_name][1]))

        else:
            if player_name != current_player:
                print("{player} has revealed {revealed} and has {number} hidden dice".format(player=player_name, revealed=player_data[player_name][0], number=len(player_data[player_name][1])))
            else:
                print("You have {revealed} revealed and have {unrevealed} hidden".format(revealed=player_data[player_name][0], unrevealed=player_data[player_name][1]))

    print("The next turn will go to {player}".format(player=player_names[(current_turn)%len(player_names)]))

    if current_turn == 1:
        print("What's your guess?")
        current_guess[0] = int(input("How many? "))
        current_guess[1] = int(input("What number? "))

    else:
        option = input("Will you call their guess or raise it higher? ").lower().strip()

        if option == 'call' or option == 'call it' or option == 'call the bluff':
            correct_amount = 0

            if current_guess[1] != 6:
                for player_name in player_data:
                    correct_amount += player_data[player_name][0].count(current_guess[1]) + player_data[player_name][1].count(current_guess[1])
                    correct_amount += player_data[player_name][0].count(6) + player_data[player_name][1].count(6)

            elif current_guess == 6:
                correct_amount += player_data[player_name][0].count(current_guess[1]) + player_data[player_name][1].count(current_guess[1])

            if current_guess[0] == correct_amount:
                for player_name in player_dice:
                    if player_name != current_player:
                        player_dice[player_name] -= 1

            elif current_guess[0] < correct_amount:
                player_dice[current_player] -= (correct_amount - current_guess[0])

            elif current_guess[0] > correct_amount:
                player_dice[player_names[(current_turn-2)%len(player_names)]] -= (current_guess[0] - correct_amount)

            for player_name in player_dice:
                if player_dice[player_name] <= 0:
                    del player_dice[player_name]

            return True

        else:
            if len(player_data[current_player][1]) > 1:
                option = input("Would you like to put out dice and roll the remaining ones? ").lower().strip()

                if option != 'n' and option != 'no':
                    if player_data[current_player][0] == []:
                        print("You haven't revealed any dice and have {dice} hidden".format(dice=player_data[current_player][1]))
                    else:
                        print("You have {revealed} revealed and have {unrevealed} hidden".format(revealed=player_data[current_player][0], unrevealed=player_data[current_player][1]))

                    value = int(input("Which number would you like to put out? "))

                    if value < 1 or value > 6:
                        raise Exception("Not a valid number!")

                    unrevealed = player_data[current_player][1]
                    amount = unrevealed.count(value)

                    if amount == len(unrevealed):
                        amount -= 1

                    player_data[current_player][0].extend([value]*amount)
                    player_data[current_player][1] = [number for number in unrevealed if number != value]

                    if value != 6:
                        unrevealed = player_data[current_player][1]
                        amount = unrevealed.count(6)

                        if amount == len(unrevealed):
                            amount -= 1

                        player_data[current_player][0].extend([6]*amount)
                        player_data[current_player][1] = [number for number in unrevealed if number != 6]

                    player_data[current_player][0] = sorted(player_data[current_player][0])
                    player_data[current_player][1] = sorted([random.randint(1,6) for x in range(len(player_data[current_player][1]))])

                    print("{player} said there are {quantity}, {value}s".format(player=player_names[(current_turn-2)%len(player_names)], quantity=current_guess[0], value=current_guess[1]))

                    for player_name in player_data:
                        if player_data[player_name][0] == []:
                            if player_name != current_player:
                                print("{player} has not revealed any dice and has {number} hidden dice".format(player=player_name, number=len(player_data[player_name][1])))
                            else:
                                print("You haven't revealed any dice and have {dice} hidden".format(dice=player_data[player_name][1]))

                        else:
                            if player_name != current_player:
                                print("{player} has revealed {revealed} and has {number} hidden dice".format(player=player_name, revealed=player_data[player_name][0], number=len(player_data[player_name][1])))
                            else:
                                print("You have {revealed} revealed and have {unrevealed} hidden".format(revealed=player_data[player_name][0], unrevealed=player_data[player_name][1]))

            print("What's your guess?")

            current_guess[0] = int(input("How many? "))
            current_guess[1] = int(input("What number? "))


player_names = []

while True:
    player_name = input("Enter a player name: ").lower().strip().title()

    if player_name == '' or player_name == 'done' or player_name == 'finished':
        break
    else:
        player_names.append(player_name)

if len(player_names) < 2:
    raise Exception("Number of players must be equal or greater to 2. The game can't be played with no one or by yourself!")

if len(player_names) != len(set(player_names)):
    raise Exception("Cannot have duplicate player names. Stats are important and we can't track those if you have duplicates!")


dice_number = int(input("Enter the number of dice per player: "))

if dice_number <= 0:
    raise Exception("Number of dice should be greater than 0. Or everyone would lose instantly.")

player_dice = {}

for player_name in player_names:
    player_dice[player_name] = dice_number


current_turn = 0
current_guess = [0, 0]


while len(player_dice) > 1:
    player_data = {}

    for player_name in player_dice:
        player_data[player_name] = [[], sorted([random.randint(1,6) for x in range(player_dice[player_name])])]

    called = False

    while called != True:
        current_turn += 1
        called = turn()