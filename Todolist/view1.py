from db import db_server
import datetime
import auth


def handle_home_page(user_id):
    html_body = """
            <h1>Todo List</h1>
            <a href="/task/add">添加任务</a>
            <hr>
            """
    tasks = db_server.get_tasks(user_id)

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

    return html_body,'200 OK',''

def handle_task_page(id):
    task = db_server.get_task_by_id(id)
    html_body = f"""
                    <h1>{task.get('title')}</h1>
                    <hr>
                    <p style="color:gray">创建时间{task.get('created_at')}</p>
                    <p style="color:gray">截止时间： {task.get('deadline')}</p>
                    <h2>{task.get('description')}</h2>
                    <a href="/task/edit?id={task.get('id')}">[编辑]</a>
                    <a href="/">返回主页面</a>
                    """
    return html_body, '200 OK', ''

def handle_edit_page(id):
    task = db_server.get_task_by_id(id)

    html_body = f"""
                    <h1>编辑页面</h1>
                    <a href="/task?id={id}">[返回]</a>
                    <hr>
                    <form method="POST" action="/task/edit">
                    
                        <input type="hidden"  name="id" value="{task.get('id')}">
                        
                        <div>
                            <label>标题：</label><br>
                            
                            <input type="text" name="title" value="{task.get('title')}">
                        </div>
                        
                        <div>
                            <label>描述：</label><br>
                            <textarea name="description" rows="5" cols="60">{task.get('description')}</textarea>
                        </div>
                        
                        
                        
                        <button type="submit">[提交]</button>
                    </form>
                    """
    return html_body, '200 OK', ''

def process_edit_page(body_params):
    id = body_params.get('id')[0]
    title = body_params.get('title')[0]
    description = body_params.get('description')[0]
    db_server.update_task(id,title,description)
    extra_headers = f"Location: /"

    return "","302 FOUND",extra_headers

def process_delete(body_params):
    id = body_params.get('id')[0]
    db_server.delete_task(id)
    extra_headers = f"Location: /"

    return "","302 FOUND",extra_headers

def process_toggle(body_params):
    id = body_params.get('id')[0]
    db_server.toggle_task_status(id)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers

def handle_add_page():

    today_date = datetime.date.today().isoformat()
    print(today_date)

    html_body = f"""
                    <h1>添加任务</h1>
                    <a href="/">[返回]</a>
                    <hr>
                    <form method="POST" action="/task/add">

                        <div>
                            <label>任务名称：</label><br>

                            <input type="text" name="title" value="添加任务名称">
                        </div>

                        <div>
                            <label>描述：</label><br>
                            <textarea name="description" rows="5" cols="60">输入任内务描述</textarea>
                        </div>
                        
                        <div style="margin-bottom: 15px;">
                            <label >选择截止日期：</label>
                            <input 
                                type="date" name="deadline" min="{today_date}" value="{today_date}" required
                            >
                        </div>

                        <button type="submit">[提交]</button>
                    </form>
                    """
    return html_body, '200 OK', ''

def process_add_page(body_params,user_id):
    title = body_params.get('title')[0]
    description = body_params.get('description')[0]
    deadline = body_params.get('deadline')[0]
    db_server.create_task(user_id, title, description,deadline)
    extra_headers = f"Location: /"

    return "", "302 FOUND", extra_headers

def handle_register_page():

    html_body = """    
                    <h1>注册账号</h1>
                    <hr>
                    <form method="POST" action="/register">
                        
                        <div>
                            <label>新用户名</label>
                            <input type="text" name="title" value="请输入用户名" require>
                        </div>
                        
                        <div>
                            <label>密码</label>
                            <input type="password" name="password" value="请输入密码" require>
                        </div>
                        
                        <button type="submit">提交</button>
                    </form>
                    """

    return html_body, '200 OK', ''

def process_register_page(body_params):
    title = body_params.get('title')[0]
    password = body_params.get('password')[0]
    db_server.register_user(title,password)
    extra_headers = f"Location: /login"

    return "", "302 FOUND", extra_headers

def handle_login_page():
    html_body = """    
                    <h1>登录</h1>
                    <hr>
                    <form method="POST" action="/login">

                        <div>
                            <label>用户名</label>
                            <input type="text" name="title"  require>
                        </div>

                        <div>
                            <label>密码</label>
                            <input type="password" name="password"  require>
                        </div>

                        <button type="submit">提交</button>
                    </form>
                    """

    return html_body, '200 OK', ''

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
    return "","404 NOT FOUND",""

