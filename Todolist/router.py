import view
import auth


def dispatch_router(method,path,parse_params,body_params,session_id):

    user_id = None
    if session_id:
        user_id = auth.get_current_user(session_id)

    public_path = {'/login','/register'}

    if path not in public_path and not user_id :

        html_body = ""
        status_code = "302 Found"
        extra_headers = "Location: /login\r\n"
        return html_body, status_code, extra_headers

    if path in public_path and user_id :
        html_body = ""
        status_code = "302 Found"
        extra_headers = "Location: /\r\n"
        return html_body, status_code, extra_headers

    if method == "GET" and path == "/":
        html_body,status_code,extra_headers = view.handle_home_page(user_id)
        return html_body,status_code,extra_headers

    elif method == "GET" and path == "/task":
        id = parse_params.get('id')[0]
        html_body,status_code,extra_headers = view.handle_task_page(id)
        return html_body, status_code, extra_headers

    elif method == "GET" and path == "/task/edit":
        id = parse_params.get('id')[0]
        html_body,status_code,extra_headers = view.handle_edit_page(id)
        return html_body, status_code, extra_headers

    elif method == "POST" and path == "/task/edit":
        html_body,status_code,extra_headers = view.process_edit_page(body_params)
        return html_body,status_code,extra_headers

    elif method == "POST" and path == "/task/toggle":
        html_body, status_code, extra_headers = view.process_toggle(body_params)
        return html_body, status_code, extra_headers

    elif method == "POST" and path == "/task/delete":
        html_body, status_code, extra_headers = view.process_delete(body_params)
        return html_body, status_code, extra_headers

    elif method == "GET" and path == "/task/add":
        html_body, status_code, extra_headers = view.handle_add_page()
        return html_body, status_code, extra_headers

    elif method == "POST" and path == "/task/add":
        html_body, status_code, extra_headers = view.process_add_page(body_params,user_id)
        return html_body, status_code, extra_headers

    elif method == "GET" and path == "/register":
        html_body, status_code, extra_headers = view.handle_register_page()
        return html_body, status_code, extra_headers

    elif method == "POST" and path == "/register":
        html_body, status_code, extra_headers = view.process_register_page(body_params)
        return html_body, status_code, extra_headers

    elif method == "GET" and path == "/login":
        html_body, status_code, extra_headers = view.handle_login_page()
        return html_body, status_code, extra_headers

    elif method == "POST" and path == "/login":
        html_body, status_code, extra_headers = view.process_login_page(body_params)
        return html_body, status_code, extra_headers

    else:
        html_body, status_code, extra_headers =view.process_error()
        return html_body, status_code, extra_headers