import random
import time
import json


class Record:
    def __init__(self):
        try:
            with open("records.json", "r") as file:
                content = file.read()
                if content:
                    self.records = json.load(file)
                    print(self.records)
                else:
                    self.records = {}
        except FileNotFoundError:
            self.records = {}

    def get_user(self, user):
        if user not in self.records:
            self.user = user
            self.records[self.user] = {
                "fastest_time" :float('inf'),
                "highest_score" : 0,
            }
            print("已为你创建新用户")
        else:
            self.user = user
    def save_records(self):
        with open("records.json", "w") as file:
            json.dump(self.records, file)


    def get_records(self,times,score):
        user_data = self.records[self.user]
        print(user_data)

        if times < user_data['fastest_time']:
            user_data['fastest_time'] = times
        if score > user_data['highest_score']:
            user_data['highest_score'] = score
        print(user_data)
        self.save_records()


def guess(times):
    target = random.randint(1, 100)
    check = False
    start_times = time.time()
    score = 100
    delete_score = 100 // times

    for i in range(times):
        try:
            guess_num = int(input("Enter your guess:"))
            if guess_num == target:
                check = True
                print(f"Congratulations! You guessed the correct number in {i + 1} attempts")
            elif guess_num > target:
                print(f"Incorrect! The number is less than {guess_num}.")
                score = score - delete_score
            elif guess_num < target:
                print(f"Incorrect! The number is greater than {guess_num}.")
                score = score - delete_score
        except ValueError:
            print("Please enter a number")

        if check:
            print("you win,game over")
            break
    end_time = time.time()
    if not check:
        print(f"you failed,the right number is {target}")
    execution_time = end_time - start_times
    print(f"共花费{execution_time}秒")
    if check == True:
        return execution_time,score
    elif check == False:
        return None



def main():
    print("Welcome to the Number Guess Game")
    print("I am thinking of a number between 1 and 100\n")
    print("-----------------------")
    user_name = input("Please enter your name: ")
    record = Record()
    record.get_user(user_name)

    while True:

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

            times,scores = guess(times)
            if times :
                print(times,scores)
                record.get_records(times,scores)
            elif times == None:
                print("No Score")

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