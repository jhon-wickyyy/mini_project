import psycopg2
from psycopg2.extras import RealDictCursor
import config

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

        self.init_table()

    def init_table(self):
        #用户表应在普通表之前建立
        uer_sql = """CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                     user_name VARCHAR(200) NOT NULL,
                     password VARCHAR(200) NOT NULL
                     )"""
        self.cur.execute(uer_sql)

        task_sql = """CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                deadline TIMESTAMP NOT NULL,
                created_at DATE DEFAULT CURRENT_TIMESTAMP,
                status Boolean DEFAULT FALSE NOT NULL
                ) """
        self.cur.execute(task_sql)

    def register_user(self,user_name,password):
        sql = """INSERT INTO users (user_name,password) VALUES (%s,%s)"""
        self.cur.execute(sql, (user_name,password,))
        return True

    def login_user(self,user_name,password):
        sql = """SELECT * FROM users WHERE user_name = %s AND password = %s"""
        self.cur.execute(sql, (user_name, password,))
        result = self.cur.fetchone()
        if result :
            user_id = result['user_id']
            return user_id
        else:
            return False

    def get_username(self,user_id):
        sql = """SELECT user_name FROM users WHERE user_id = %s"""
        self.cur.execute(sql, (user_id,))
        result = self.cur.fetchone()
        user_name = result['user_name']
        return user_name

    def create_task(self, user_id, title, descirption,deadline):
        sql =""" INSERT INTO tasks (user_id, title, description,deadline)
                values (%s,%s,%s,%s)"""
        self.cur.execute(sql, (user_id, title, descirption,deadline))

    def get_tasks(self,user_id):
        sql = """SELECT * FROM tasks WHERE user_id = %s"""
        self.cur.execute(sql, (user_id,))
        result = self.cur.fetchall()
        return result

    def get_task_by_id(self,task_id):
        sql = """SELECT * FROM tasks WHERE id = %s"""
        self.cur.execute(sql, (task_id,))
        row = self.cur.fetchone()
        return row

    def update_task(self,task_id,title,description):
        sql = """UPDATE tasks SET title = %s, description = %s WHERE id = %s"""
        self.cur.execute(sql, (title, description, task_id,))
        return True

    def toggle_task_status(self,task_id):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        else:
            new_status = not task['status']
            sql = """UPDATE tasks SET status = %s WHERE id = %s"""
            self.cur.execute(sql, (new_status, task_id))
            return True

    def delete_task(self,task_id):
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        else:
            sql = "DELETE FROM tasks WHERE id = %s"
            self.cur.execute(sql, (task_id,))
            return True

db_server = Database()

def main():
    #db_server.create_task(1, '完成季度财务报表', '整理并核对Q1所有部门的收支明细，提交至财务部。', '2024-03-31',)
    #db_server.toggle_task_status(3)
    #result = db_server.login_user('111','111')
    result = db_server.get_username(1)
    print(result)


if __name__ == '__main__':
    main()
