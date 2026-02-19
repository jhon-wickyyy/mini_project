import random
import time
import json
import os


class Record:
    def __init__(self):
        try:
            with open("records.json", "r") as file:
                # 加上 safeguard，防止文件是空的报错
                content = file.read()
                if content:
                    self.records = json.loads(content)
                else:
                    self.records = {}
        except (FileNotFoundError, json.JSONDecodeError):
            self.records = {}

        # 不要在这里初始化 user 相关的属性，容易造成状态污染
        self.current_user = None

    def get_user(self, user):
        self.current_user = user
        if user not in self.records:
            print(f"🆕 已为你创建新用户: {user}")
            self.records[user] = {
                "fastest_time": float('inf'),  # 无穷大，完美
                "highest_score": 0,  # 拼写修正 score
            }
        else:
            print(f"👋 欢迎回来, {user}")
            # 打印一下当前数据给用户看
            data = self.records[user]
            best = data['fastest_time']
            if best == float('inf'):
                best = "暂无"
            else:
                best = f"{best:.2f}s"
            print(f"当前纪录 -> 最快: {best} | 最高分: {data['highest_score']}")

    def save_records(self):
        try:
            with open("records.json", "w") as file:
                json.dump(self.records, file, indent=4)
        except IOError:
            print("保存失败")

    def update_records(self, times, score):  # 改名为 update 更贴切
        # 直接获取字典的引用
        user_data = self.records[self.current_user]
        updated = False

        # 【重点】直接和字典里的数据比！不要用 self.fastest_time！
        if times < user_data['fastest_time']:
            user_data['fastest_time'] = times
            print("⚡ 打破最快记录！")
            updated = True

        # 【重点】拼写修正 score
        if score > user_data['highest_score']:
            user_data['highest_score'] = score
            print("🏆 创造新高分！")
            updated = True

        if updated:
            self.save_records()


def guess(limit):
    target = random.randint(1, 100)
    # print(target) # 老师帮你删掉了作弊码

    start_time = time.time()
    score = 100
    penalty = 100 // limit  # 动态扣分，比较公平

    print(f"\n游戏开始！机会: {limit}")

    for i in range(limit):
        try:
            guess_num = int(input(f"[{i + 1}/{limit}] Enter your guess: "))

            if guess_num == target:
                end_time = time.time()
                duration = end_time - start_time
                print(f"🎉 Congratulations! used {i + 1} attempts.")

                # 赢了！直接返回数据。这时候还没扣分，满分就是100。
                return duration, score

            elif guess_num > target:
                print("📉 Too High!")
            elif guess_num < target:
                print("📈 Too Low!")

            # 【重点】只有猜错才扣分
            score -= penalty

        except ValueError:
            print("⚠️ Please enter a number")

    # 循环结束还没 return，说明输了
    print(f"💀 You failed! The number was {target}")
    return None, 0  # 输了返回 None


def main():
    print("=== Number Guess Game v5.0 ===")
    user_name = input("Please enter your name: ").strip()
    if not user_name: user_name = "Player1"

    record = Record()
    record.get_user(user_name)

    while True:
        print("-" * 30)
        print("1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances)")
        try:
            choice = input("Enter choice (1-3): ")
            if choice == '1':
                times = 10
            elif choice == '2':
                times = 5
            elif choice == '3':
                times = 3
            else:
                print("Invalid choice")
                continue

            # 获取游戏结果
            duration, score = guess(times)

            # 【重点】只有赢了(duration不是None)才记录！
            if duration is not None:
                print(f"本局耗时: {duration:.2f}s, 得分: {score}")
                record.update_records(duration, score)

        except ValueError:
            print("Please enter a number")

        confirm = input("\nPlay again? (Y/N): ").upper()
        if confirm != "Y":
            print("Goodbye!")
            break


if __name__ == '__main__':
    main()