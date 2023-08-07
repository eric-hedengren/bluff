import random

starting_names = []

while True:
    starting_name = input("Enter a player name: ").strip().title()

    if starting_name == '' or starting_name == 'done' or starting_name == 'finished':
        break
    else:
        starting_names.append(starting_name)

if len(starting_names) < 2:
    raise Exception("Number of players must be equal or greater to 2. The game can't be played with no one or by yourself!")

if len(starting_names) != len(set(starting_names)):
    raise Exception("Cannot have duplicate player names. Stats are important and we can't track those if you have duplicates!")

dice_number = int(input("Enter the number of dice per player: "))

if dice_number <= 0:
    raise Exception("Number of dice should be greater than 0. Or everyone would lose instantly.")

player_dice = {}

for starting_name in starting_names:
    player_dice[starting_name] = dice_number

game_data = {}

while len(player_dice) > 1:
    if 'previous_winner' in game_data:
        starting_position = list(player_dice.keys()).index(game_data['previous_winner'])
        remaining_players = list(player_dice.keys())[starting_position:] + list(player_dice.keys())[:starting_position]
        remaining_dice = list(player_dice.values())[starting_position:] + list(player_dice.values())[:starting_position]
        player_dice = {}

        for position, player_name in enumerate(remaining_players):
            player_dice[player_name] = remaining_dice[position]

    player_names = list(player_dice.keys())
    player_data = {}

    for player_name in player_names:
        player_data[player_name] = [[], sorted([random.randint(1,6) for x in range(player_dice[player_name])])]

    current_turn = 0
    current_guess = [0, 0]
    game_data['bluff_called'] = False

    while game_data['bluff_called'] != True:
        current_turn += 1

        current_player = player_names[(current_turn-1)%len(player_names)]
        print("It's {player}'s turn".format(player=current_player))

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

        if current_turn > 1:
            print("{player} said there are {quantity}, {value}s".format(player=player_names[(current_turn-2)%len(player_names)], quantity=current_guess[0], value=current_guess[1]))

        if current_turn == 1:
            print("What's your guess?")

            current_guess[0] = int(input("How many? "))
            current_guess[1] = int(input("What number? "))

        else:
            option = input("Will you call bluff on their guess or raise it higher? ").strip().lower()

            if option == 'call' or option == 'bluff' or option == 'call it' or option == 'call bluff' or option == 'call the bluff':
                correct_amount = 0

                for player_name in player_data:
                    correct_amount += player_data[player_name][0].count(current_guess[1]) + player_data[player_name][1].count(current_guess[1])

                if current_guess[1] != 6:
                    for player_name in player_data:
                        correct_amount += player_data[player_name][0].count(6) + player_data[player_name][1].count(6)

                previous_player = player_names[(current_turn-2)%len(player_names)]

                if current_guess[0] == correct_amount:                
                    game_data['previous_winner'] = previous_player

                    for player_name in player_names:
                        if player_name != previous_player:
                            player_dice[player_name] -= 1

                    print("{caller} called bluff on {guesser}'s guess, but {guesser} guessed the exact amount!".format(caller=current_player, guesser=previous_player))
                    print("Everyone loses 1 dice, except {guesser}".format(guesser=previous_player))

                elif current_guess[0] < correct_amount:
                    game_data['previous_winner'] = previous_player
                    player_dice[current_player] -= (correct_amount - current_guess[0])

                    print("{caller} called bluff on {guesser}'s guess, but it was below the correct amount!".format(caller=current_player, guesser=previous_player))
                    print("{caller} loses {amount} dice".format(caller=current_player, amount=(correct_amount-current_guess[0])))

                elif current_guess[0] > correct_amount:
                    game_data['previous_winner'] = current_player
                    player_dice[previous_player] -= (current_guess[0] - correct_amount)

                    print("{caller} called bluff on {guesser}'s guess, and it was above the correct amount!".format(caller=current_player, guesser=previous_player))
                    print("{guesser} loses {amount} dice".format(guesser=previous_player, amount=(current_guess[0]-correct_amount)))

                for player_name in player_names:
                    if player_dice[player_name] <= 0:
                        del player_dice[player_name]

                game_data['bluff_called'] = True

            else:
                if len(player_data[current_player][1]) > 1:
                    option = input("Would you like to put out dice and roll the remaining ones? ").strip().lower()

                    if option != 'n' and option != 'no':
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

                        print("You have {revealed} out and rolled {unrevealed}".format(revealed=player_data[current_player][0], unrevealed=player_data[current_player][1]))

                print("What's your guess?")

                current_guess[0] = int(input("How many? "))
                current_guess[1] = int(input("What number? "))