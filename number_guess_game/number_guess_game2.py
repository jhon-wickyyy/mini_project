import random
import time
import json


def guess(times):
    solid_number = random.randint(1, 100)
    check = False
    stat_times = time.time()
    for i in range(times):
        try:
            guess_num = int(input("Enter your guess:"))
            if guess_num == solid_number:
                check = True
                print(f"Congratulations! You guessed the correct number in {i + 1} attempts")
            elif guess_num > solid_number:
                print(f"Incorrect! The number is less than {guess_num}.")
            elif guess_num < solid_number:
                print(f"Incorrect! The number is greater than {guess_num}.")
        except ValueError:
            print("Please enter a number")

        if check:
            print("you win,game over")
            break
    end_time = time.time()
    if not check:
        print(f"you failed,the right number is {solid_number}")
    execition_time = end_time - stat_times
    print(f"共花费{execition_time}秒")

def main():
    print("Welcome to the Number Guess Game")
    print("I am thinking of a number between 1 and 100\n")

    while True:
        print("-----------------------")
        print("Please select the difficulty level:")
        print("""1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances""")
        try:
            number = int(input("Enter your choice: "))
            if number == 1:
                times = 10
            elif number == 2:
                times = 5
            elif number == 3:
                times = 3
            else:
                print("Please enter 1 or 2 or 3")
                continue

            guess(times)

        except ValueError:
            print("Please enter a number")


        confirm = input("Press Enter to continue  (Y/N)")
        if  confirm == "Y" or  confirm == "y":
            print("-----------------------")
        elif  confirm == "N" or  confirm == "n":
            print("Goodbye!")
            break
        else:
            print("Please enter Y or N")
            break



if __name__ == '__main__':
    main()