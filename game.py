import random

def roll(number):
    dice = []

    for i in range(number):
        dice.append(random.randint(1,6))

    return dice

humans = []

while True:
    human = input("Enter a player name: ").lower()

    if human == '' or human == 'done':
        break
    else:
        humans.append(human)

bots = input("Enter the number of bots: ")

if bots == '':
    bots = 0

bots = int(bots)

if len(humans) + bots < 2:
    raise Exception("Number of players must be equal or greater to 2. The game wouldn't be fun by yourself!")

dice_number = int(input("Enter the number of dice per player: "))

if dice_number <= 0:
    raise Exception("Number of dice should be greater than 0. Or everyone would lose instantly.")

player_names = humans

for i in range(1,bots+1):
    player_names.append('bot'+str(i))

player_data = {}

for player_name in player_names:
    player_data[player_name] = {'dice': roll(dice_number)}

random.shuffle(player_names)