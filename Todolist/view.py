from db import db_server
import datetime
from config import *
import os
import auth


def render_template(file_name,context=None):
    file_path = os.path.join(TEMPLATES_FILE,file_name)

    with open(file_path,'r',encoding='utf-8') as f:
        html_content = f.read()

    if context is None:
        return html_content

    for key,value in context.items():
        placeholder = f"{{{{{key}}}}}"
        html_content = html_content.replace(placeholder,str(value))

    return html_content


def handle_home_page(user_id):
    html_body = f""
    tasks = db_server.get_tasks(user_id)
    user_name = db_server.get_username(user_id)

    for task in tasks:

        id = task.get('id')
        status = task.get('status')
        new_status = ""
        if status == True:
            new_status = "√"
        elif status == False:
            new_status = "×"
        html_body += f"""
                        <div style="background:#F5F5F5">
                            <a href="/task?id={id}">{task.get('title')}</a>
                            <p style="color:gray">截止时间: {task.get('deadline')}</p>

                            <form method="POST" action="/task/toggle">
                                <input type="hidden"  name="id" value="{id}">
                                <button type="submit">完成状态：{new_status}</button>
                            </form>

                            <form method="POST" action="/task/delete">
                                <input type="hidden"  name="id" value="{id}">
                                <button type="submit">删除</button>
                            </form>
                        </div>
                        """
    context = {
        'user_name':user_name,
        'tasks_html':html_body
    }
    final_html = render_template("index.html",context)

    return final_html, '200 OK', ''


def handle_task_page(id):
    task = db_server.get_task_by_id(id)
    print(task)

    context = {
        'Title':task.get('title'),
        'title':task.get('title'),
        'current_time':task.get('create_at'),
        'deadline':task.get('deadline'),
        'description':task.get('description'),
        'task_id':id
    }
    final_html = render_template('tasks.html', context)

    return final_html, '200 OK', ''


def handle_edit_page(id):
    task = db_server.get_task_by_id(id)


    context = {
        'page_title':'编辑任务',
        'id':id,
        'action':'/task/edit',
        'title':task.get('title'),
        'deadline':task.get('deadline'),
        'description':task.get('description'),
        'create_at':task.get('create_at')
    }
    final_html = render_template('form.html', context)
    return final_html, '200 OK', ''


def process_edit_page(body_params):
    id = body_params.get('id')[0]
    title = body_params.get('title')[0]
    description = body_params.get('description')[0]
    db_server.update_task(id, title, description)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers


def process_delete(body_params):
    id = body_params.get('id')[0]
    db_server.delete_task(id)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers


def process_toggle(body_params):
    id = body_params.get('id')[0]
    db_server.toggle_task_status(id)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers


def handle_add_page():
    today_date = datetime.date.today().isoformat()
    print(today_date)

    context = {
        'page_title': '编辑任务',
        'id': id,
        'action': '/task/add',
        'title': '',
        'deadline': '',
        'description': '',
        'create_at': today_date

    }
    final_html = render_template('form.html', context)
    return final_html, '200 OK', ''


def process_add_page(body_params, user_id):
    title = body_params.get('title')[0]
    description = body_params.get('description')[0]
    deadline = body_params.get('deadline')[0]
    db_server.create_task(user_id, title, description, deadline)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers


def handle_register_page():
    final_html = render_template('register.html',)
    return final_html, '200 OK', ''


def process_register_page(body_params):
    title = body_params.get('title')[0]
    password = body_params.get('password')[0]
    db_server.register_user(title, password)
    extra_headers = f"Location: /login"

    return "", "302 FOUND", extra_headers


def handle_login_page():
    final_html = render_template('login.html',)
    return final_html, '200 OK',''


def process_login_page(body_params):
    title = body_params.get('title')[0]
    password = body_params.get('password')[0]
    user_id = db_server.login_user(title, password)

    if user_id:

        session_id = auth.create_id(user_id)
        extra_headers = f"Location: /\r\nSet-Cookie:session_id={session_id}; Path=/;"

        return "", "302 FOUND", extra_headers

    else:
        html_body = f"""
                        <h1>该用户不存在</h1>
                        <a href="/login">返回登录界面</a>    
                    """
        return html_body, '200 OK', ''


def process_error():
    return "", "404 NOT FOUND", ""

