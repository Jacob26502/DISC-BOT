import random
rnd=random.randint(0,6)
while True:
    if rnd ==int(input("please guess a number between 1 and 6\n")):
        print("you guessed well done")
        break
    else:
        print("try again\n")
