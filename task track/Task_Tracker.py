import argparse
import json
import os
import time


class TaskTracker:
    def __init__(self):
        self.filename = "my_data.json"
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.data = {}
            return

        try:
            with open(self.filename, 'r',encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    self.data = json.loads(content)
                else:
                    self.data = {}
        except (json.JSONDecodeError, Exception):
            print(f"警告：{self.filename} 文件内容损坏或为空，已重置数据。")
            self.data = {}

    def write_task(self):

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_task(self,taskname,description = " "):
        if not self.data:
            new_id = 1
        else:
            all_ids = [int(k) for k in self.data.keys()]
            new_id = max(all_ids) + 1
        str_id = str(new_id)

        current_time = self.get_time()

        self.data[str_id]= {
            "id":str_id,
            "description":description,
            "taskname": taskname,
            "status": "todo",
            "createdAt": current_time,
            "updatedAt": current_time,
        }
        self.write_task()

    def delete_task(self,task_id):
        str_id = str(task_id)
        if str_id not in self.data:
            print(f"{str_id}不存在")
        else:
            del self.data[str_id]

            self.write_task()

    def update_task(self,task_id,status):
        str_id = str(task_id)
        if str_id not in self.data:
            print("task not exist")
            return
        else:
            if status not in("todo", "in-progress", "done"):
                print('status not exist,please check in "todo", "in-progress", "done"')
                return
            else:
                current_time = self.get_time()

                self.data[str_id]["status"] = status
                self.data[str_id]["updatedAt"] = current_time

                self.write_task()

    def get_time(self):
        stamp_time = time.time()
        current_time = time.strftime('%Y-%m-%d,%H:%M:%S', time.localtime(stamp_time))
        return current_time



    def list_tasks(self):
        if not self.data:
            print("目前没有任务。")
            return

            # 打印表头
        print(f"{'ID':<5} {'状态':<12} {'任务名称':<17}{'任务描述'}")
        print("-" * 40)

        for t_id, task in self.data.items():
            # 使用 f-string 的对齐功能
            print(f"{t_id:<5} {task['status']:<12} {task['taskname']:<17}{task['description']}")

def main():
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers(title = '子命令',dest = 'command')

    add_tasks = sub_parser.add_parser('add',help='add a new task')
    add_tasks.add_argument('taskname',type=str,help='it is task`s name')
    add_tasks.add_argument('-d',"--description",type=str,help='it is task`s description')

    delete_tasks = sub_parser.add_parser('delete',help='delete a task')
    delete_tasks.add_argument('task_id',help='it is task`s id')

    update_tasks = sub_parser.add_parser('update',help='update a task')
    update_tasks.add_argument('task_id',help='it is task`s id')
    update_tasks.add_argument('status',type=str,help='it is task`s status')

    sub_parser.add_parser('list',help='list all tasks')

    args = parser.parse_args()

    tasktracker = TaskTracker()

    if args.command == 'add':
        tasktracker.add_task(args.taskname,args.description)
    elif args.command == 'delete':
        tasktracker.delete_task(args.task_id)
    elif args.command == 'update':
        tasktracker.update_task(args.task_id,args.status)
    elif args.command == 'list':
        tasktracker.list_tasks()




if __name__ == '__main__':
    main()
