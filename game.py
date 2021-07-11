# imports
import random
import bot


# functions
def roll(number):
    dice = []

    for i in range(number):
        dice.append(random.randint(1,6))

    return sorted(dice)

def known_dice():
    revealed_dice = player_data[current_player]['dice']

    for player_name in player_names:
        revealed_dice.append(player_data[player_name]['revealed_dice'])

    # make complete list all raw data

    return sorted(revealed_dice)

def unknown_dice():
    unknown_dice = 0

    other_players = player_names
    other_players.remove(current_player)

    for other_player in other_players:
        unknown_dice += len(player_data[other_player]['dice'])

    return unknown_dice

def total_dice():
    total = 0
    
    for player_name in player_names:
        total += len(player_data[player_name]['dice']) + len(player_data[player_name]['revealed_dice'])

    return total


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
    current_player = player_names[turn-1]


    # bot first turn
    if current_player.startswith('bot'):
        current_guess = bot.bot_turn_first(known_dice(),unknown_dice())
        print("{bot} took it's turn".format(bot=current_player))

    # human first turn
    else:
        print("It's {player}'s turn".format(player=current_player))
        print("These are the dice you have rolled: {dice}".format(dice=player_data[current_player]['dice']))
        print("There are {number} dice you cannot see".format(number=unknown_dice()))
        print("What's your guess?")

        current_guess = []
        current_guess.append(int(input("How many? ")))
        current_guess.append(int(input("What number? ")))


        if current_guess[0] <= 0:
            raise Exception("Not a valid quantity.")

        if current_guess[0] > total_dice():
            raise Exception("Cannot guess higher than the total number of dice.")

        if current_guess[1] < 1 or current_guess[1] > 6:
            raise Exception("You cannot guess outside the 1-6 range.")


    # the game after the first turn
    while True:
        turn += 1
        current_player = player_names[(turn-1)%player_number]

        # bot turn
        if current_player.startswith('bot'):
            current_guess = bot.bot_turn(current_guess,known_dice(),unknown_dice())
            print("{bot} took it's turn".format(bot=current_player))

        # human turn
        else:
            print("It's {player}'s turn".format(player=current_player))
            print("The current guess is {number} {roll}s".format(number=current_guess[0], roll=current_guess[1]))

            # display revealed dice, their dice, and the number of unknown dice
            # let them choose to call a bluff, or take a guess
            # if guess was chosen, let them keep the dice they have, or put some dice out and re roll, then guess
            previous_guess = current_guess

            # validate the guess
            if current_guess[0] > total_dice():
                raise Exception("Cannot guess higher than the total number of dice.")

            if current_guess[1] < 1 or current_guess[1] > 6:
                raise Exception("You cannot guess outside the 1-6 range.")

            # check if the guess switched between 6 and 1-5


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