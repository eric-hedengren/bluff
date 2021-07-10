import random


def roll(number):
    dice = []

    for i in range(number):
        dice.append(random.randint(1,6))

    return dice

def validate_guess_first(current):
    if current[0] <= 0:
        raise Exception("Not a valid quantity.")

    if current[1] < 1 or current[1] > 6:
        raise Exception("You can't guess outside the 1-6 range.")

def validate_guess(current):
    return None

def bot_turn_first(known,unknown):
    # guess is the only option
    return None # return guess

def bot_turn(guess,known,unknown):
    return None


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
    raise Exception("Number of players must be equal or greater to 2. The game wouldn't be fun with no one or by yourself!")

dice_number = int(input("Enter the number of dice per player: "))

if dice_number <= 0:
    raise Exception("Number of dice should be greater than 0. Or everyone would lose instantly.")

player_names = humans

for i in range(1,bots+1):
    player_names.append('bot'+str(i))


# loop for multiple games
while True:
    # initialize data
    player_data = {}

    for player_name in player_names:
        player_data[player_name] = {'dice': roll(dice_number), 'revealed_dice': []}

    #shuffle player order
    random.shuffle(player_names)

    player_number = len(player_names)
    turn = 0

    player_turn = player_names[turn]

    # first turn
    if player_turn.startswith('bot'):
        current_guess = bot_turn_first()

    else:
        print("It's {player}'s turn".format(player=player_turn))

        # display their dice, and the number of unknown dice

        current_guess = []
        current_guess.append(int(input("How many? ")))
        current_guess.append(int(input("What number? ")))

        validate_guess_first(current_guess)

    while True:
        player_turn = player_names[turn%player_number]

        if player_turn.startswith('bot'):
            current_guess = bot_turn()

        else:
            print("It's {player}'s turn".format(player=player_turn))
            print("The current guess is {number} {roll}s".format(number=current_guess[0], roll=current_guess[1]))

            # display revealed dice, their dice, and the number of unknown dice
            # let them choose to call a bluff, or take a guess
            # if guess was chosen, let them keep the dice they have, or put some dice out and re roll

        # check if the game is over

        break

    # end of game
    response = input("Play again? This will use the same settings. ").lower()

    if response == 'no':
        print("Thanks for playing!")
        break
    else:
        print("Alright great! Restarting...")
        continue