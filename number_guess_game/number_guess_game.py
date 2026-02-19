import random

class NumberGuess:
    def __init__(self,num):
        self.solid_number = random.randint(1, 100)
        self.num = num
        self.check = False

    def guess(self):
        if self.num == 1:
            times = 10
        elif self.num == 2:
            times = 5
        elif self.num == 3:
            times = 3

        for i in range(times):
            guess_num = int(input("Enter your guess:"))
            if guess_num == self.solid_number:
                self.check = True
                print(f"Congratulations! You guessed the correct number in {i+1} attempts")
            elif guess_num > self.solid_number:
                print(f"Incorrect! The number is less than {guess_num}.")
            elif guess_num < self.solid_number:
                print(f"Incorrect! The number is greater than {guess_num}.")

            if self.check:
                break

def main():
    print("Welcome to the Number Guess Game")
    print("I am thinking of a number between 1 and 100\n")

    while True:
        print("Please select the difficulty level:")
        print("""1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances""")
        number = int(input("Enter your choice: "))
        print("Great! You have selected the Medium difficulty level.\nLet's start the game!")
        numguess = NumberGuess(number)
        numguess.guess()
        str = input("Press Enter to continue  (Y/N)")
        if str == "Y" or str == "y":
            print("-----------------------")
            pass
        elif str == "N" or str == "n":
            print("Goodbye!")
            break

if __name__ == '__main__':
    main()