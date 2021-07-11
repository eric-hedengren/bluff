# imports
import random
import bot


# functions
def roll(number):
    dice = []

    for i in range(number):
        dice.append(random.randint(1,6))

    return sorted(dice)

def known_dice(current_player):
    revealed_dice = player_data[current_player]['dice']

    for player_name in player_names:
        revealed_dice.append(player_data[player_name]['revealed_dice'])

    # make complete list all raw data

    return sorted(revealed_dice)

def unknown_dice(current_player):
    unknown_dice = 0

    other_players = player_names
    other_players.remove(current_player)

    for other_player in other_players:
        unknown_dice += len(player_data[other_player]['dice'])

    return unknown_dice

def validate_guess(current):
    return current


# players
humans = []

while True:
    human = input("Enter a player name: ").lower()

    if human == '' or human == 'done' or human == 'finished':
        break
    else:
        humans.append(human)

bots = input("Enter the number of bots: ")

if bots == '':
    bots = 0

bots = int(bots)

if len(humans) + bots < 2:
    raise Exception("Number of players must be equal or greater to 2. The game can't be played with no one or by yourself!")


# player names
player_names = humans

for i in range(1,bots+1):
    player_names.append('bot'+str(i))

if len(player_names) != len(set(player_names)):
    raise Exception("Cannot have duplicate player names. Stats are important and we can't track those if you have duplicates!")


# number of dice
dice_number = int(input("Enter the number of dice per player: "))

if dice_number <= 0:
    raise Exception("Number of dice should be greater than 0. Or everyone would lose instantly.")


# the main game
while True:
    # initialize data
    player_number = len(player_names)
    player_data = {}

    for player_name in player_names:
        player_data[player_name] = {'dice': roll(dice_number), 'revealed_dice': []}


    # determine player order
    random.shuffle(player_names)

    turn = 1
    player_turn = player_names[turn-1]


    # bot first turn
    if player_turn.startswith('bot'):
        current_guess = bot.bot_turn_first(known_dice(player_turn),unknown_dice(player_turn))

    # human first turn
    else:
        print("It's {player}'s turn".format(player=player_turn))
        print("These are the dice you have rolled: {dice}".format(dice=player_data[player_turn]['dice']))
        print("There are {number} dice you cannot see".format(number=unknown_dice(player_turn)))
        print("What's your guess?")

        current_guess = []
        current_guess.append(int(input("How many? ")))
        current_guess.append(int(input("What number? ")))


        if current_guess[0] <= 0:
            raise Exception("Not a valid quantity.")

        if current_guess[1] < 1 or current_guess[1] > 6:
            raise Exception("You can't guess outside the 1-6 range.")


    # the game after the first turn
    while True:
        turn += 1
        player_turn = player_names[(turn-1)%player_number]

        # bot turn
        if player_turn.startswith('bot'):
            current_guess = bot.bot_turn(current_guess,known_dice(player_turn),unknown_dice(player_turn))

        # human turn
        else:
            print("It's {player}'s turn".format(player=player_turn))
            print("The current guess is {number} {roll}s".format(number=current_guess[0], roll=current_guess[1]))

            # display revealed dice, their dice, and the number of unknown dice
            # let them choose to call a bluff, or take a guess
            # if guess was chosen, let them keep the dice they have, or put some dice out and re roll

        # if a guess was called: 
        # check who won the round
        # take away the right amount of dice from certain players
        # check if the game is over

        break


    # save game stats


    # end of game
    response = input("Play again? This will use the same settings. ").lower()

    if response == 'no':
        print("Thanks for playing!")
        break
    else:
        print("Alright great! Restarting...")
        continue