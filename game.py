from random import randint

humans = []

while True:
    human = input("Enter a player name: ").lower()

    if human == '' or human == 'done':
        break
    else:
        humans.append(human)

bots = int(input("Enter the number of bots: "))

if len(humans) + bots < 2:
    raise Exception("Number of players must be equal or greater to 2. The game wouldn't be fun by yourself!")

players = {}