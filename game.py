import random

starting_names = []

while True:
    starting_name = input("Enter a player name: ").strip().title()

    if starting_name == '' or starting_name == 'done' or starting_name == 'finished':
        break
    else:
        starting_names.append(starting_name)

if len(starting_names) < 2:
    raise Exception("Number of players must be equal or greater than 2. The game can't be played with no one or by yourself!")

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

        for player_name in player_names:
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

            if current_guess[0] <= 0:
                raise Exception("You can't guess that!")

            if current_guess[1] < 1 or current_guess[1] > 6:
                raise Exception("That number isn't valid.")

        else:
            option = input("Will you call the bluff on their guess or raise it higher? ").strip().lower()

            if option == 'call' or option == 'bluff' or option == 'call it' or option == 'call bluff' or option == 'call the bluff':
                correct_amount = 0

                for player_name in player_names:
                    correct_amount += player_data[player_name][0].count(current_guess[1]) + player_data[player_name][1].count(current_guess[1])

                if current_guess[1] != 6:
                    for player_name in player_names:
                        correct_amount += player_data[player_name][0].count(6) + player_data[player_name][1].count(6)

                previous_player = player_names[(current_turn-2)%len(player_names)]

                if current_guess[0] == correct_amount:                
                    game_data['previous_winner'] = previous_player

                    for player_name in player_names:
                        if player_name != previous_player:
                            player_dice[player_name] -= 1

                    print("{caller} called the bluff on {guesser}'s guess, but {guesser} guessed the exact amount!".format(caller=current_player, guesser=previous_player))

                    remaining_opponents = []

                    for player_name in player_names:
                        if player_name != previous_player:
                            if player_dice[player_name]:
                                remaining_opponents.append(player_name)

                    if len(remaining_opponents) == len(player_names)-1 and len(remaining_opponents) != 1:
                        print("Everyone loses 1 dice except {guesser}".format(guesser=previous_player))
                    elif len(remaining_opponents) > 2:
                        print("{opponents} lose 1 dice".format(opponents=', '.join(remaining_opponents[:-1])+', and '+remaining_opponents[-1]))
                    elif len(remaining_opponents) == 2:
                        print("{opponents} lose 1 dice".format(opponents=' and '.join(remaining_opponents)))
                    elif len(remaining_opponents) == 1:
                        print("{opponent} loses 1 dice".format(opponent=remaining_opponents[0]))

                elif current_guess[0] < correct_amount:
                    game_data['previous_winner'] = previous_player
                    player_dice[current_player] -= (correct_amount - current_guess[0])

                    print("{caller} called the bluff on {guesser}'s guess, but it was below the correct amount!".format(caller=current_player, guesser=previous_player))

                    if player_dice[current_player] > 0:
                        print("{caller} loses {amount} dice".format(caller=current_player, amount=(correct_amount-current_guess[0])))

                elif current_guess[0] > correct_amount:
                    game_data['previous_winner'] = current_player
                    player_dice[previous_player] -= (current_guess[0] - correct_amount)

                    print("{caller} called the bluff on {guesser}'s guess, and it was above the correct amount!".format(caller=current_player, guesser=previous_player))

                    if player_dice[previous_player] > 0:
                        print("{guesser} loses {amount} dice".format(guesser=previous_player, amount=(current_guess[0]-correct_amount)))

                losing_players = []

                for player_name in player_names:
                    if player_dice[player_name] <= 0:
                        losing_players.append(player_name)
                        del player_dice[player_name]

                if len(losing_players) == len(player_names)-1 and len(losing_players) != 1:
                    print("Everyone ran out of dice, except {winner}!".format(winner=previous_player))
                elif len(losing_players) > 2:
                    print("{players} ran out of dice!".format(players=', '.join(losing_players[:-1])+', and '+losing_players[-1]))
                elif len(losing_players) == 2:
                    print("{players} ran out of dice!".format(players=' and '.join(losing_players)))
                elif len(losing_players) == 1:
                    print("{player} ran out of dice!".format(player=losing_players[0]))

                game_data['bluff_called'] = True

            else:
                unrevealed = player_data[current_player][1]

                if len(unrevealed) > 1:
                    option = input("Would you like to put out dice and roll the remaining ones? ").strip().lower()

                    if option != 'n' and option != 'no':
                        value = int(input("Which number would you like to put out? "))

                        if value < 1 or value > 6:
                            raise Exception("Not a valid number!")

                        if value not in unrevealed:
                            raise Exception("You don't have that number in your dice!")

                        complete = False
                        amount = unrevealed.count(value)

                        if amount == len(unrevealed):
                            amount -= 1
                            complete = True

                        player_data[current_player][0].extend([value]*amount)
                        player_data[current_player][1] = [number for number in unrevealed if number != value]

                        if not complete and value != 6:
                            unrevealed = player_data[current_player][1]
                            amount = unrevealed.count(6)

                            if amount == len(unrevealed):
                                amount -= 1

                            player_data[current_player][0].extend([6]*amount)
                            player_data[current_player][1] = [number for number in unrevealed if number != 6]

                        player_data[current_player][0] = sorted(player_data[current_player][0])
                        player_data[current_player][1] = sorted([random.randint(1,6) for x in range(len(player_data[current_player][1]))])

                        print("You have {revealed} out and rolled {unrevealed}".format(revealed=player_data[current_player][0], unrevealed=player_data[current_player][1]))

                elif len(unrevealed) == 1:
                    option = input("Would you like to reroll your hidden dice? ").strip().lower()

                    if option != 'n' and option != 'no':
                        player_data[current_player][1] = sorted([random.randint(1,6) for x in range(len(player_data[current_player][1]))])
                        print("You rolled {unrevealed}".format(unrevealed=player_data[current_player][1]))

                previous_guess = current_guess.copy()
                print("What's your guess?")

                current_guess[0] = int(input("How many? "))
                current_guess[1] = int(input("What number? "))

                if current_guess[1] < 1 or current_guess[1] > 6:
                    raise Exception("That number isn't valid.")

                if current_guess[1] != 6 and previous_guess[1] != 6:
                    if current_guess[0] == previous_guess[0] and current_guess[1] <= previous_guess[1] or current_guess[1] == previous_guess[1] and current_guess[0] <= previous_guess[0]:
                        raise Exception("Guess was not raised!")

                elif current_guess[1] == 6 and previous_guess[1] == 6:
                    if current_guess[0] <= previous_guess[0]:
                        raise Exception("Guess was not raised!")

                elif current_guess[1] != 6 and previous_guess[1] == 6:
                    if current_guess[0] < previous_guess[0]*2:
                        raise Exception("Guess was not raised!")

                elif current_guess[1] == 6 and previous_guess[1] != 6:
                    if current_guess[0]*2 <= previous_guess[0]:
                        raise Exception("Guess was not raised!")

print("{winner} wins!".format(winner=game_data['previous_winner']))