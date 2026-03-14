import socket
from config import *
import urllib.parse
from view import *




def start_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind((HOST, PORT))
    client_socket.listen(5)
    print(f"服务器已监听，监听地址为http://{HOST}:{PORT}")
    while True:
        client_connection, client_address = client_socket.accept()
        raw_request_data = client_connection.recv(8192).decode('utf-8')

        request_line = raw_request_data.split('\n')[0].strip()
        parts = request_line.split(' ')
        if len(parts) >= 2:
            method = parts[0]
            raw_url = parts[1]
        else:
            method = None
            raw_url = "/"

            print(f"收到了{request_line}")

        parsed_url = urllib.parse.urlparse(raw_url)
        print(parsed_url)
        path =  parsed_url.path
        parsed_parms = urllib.parse.parse_qs(parsed_url.query)
        print(f"在{method}模式下，访问路径：{path},携带参数{parsed_parms}")



        if method == "GET" and path == "/":
            html_body,status_code,extra_headers = handle_home_page()

        elif method == "GET" and path == "/article":
            articles_id = parsed_parms.get("id","")[0]
            html_body,status_code,extra_headers = handle_article_page(articles_id)

        elif method == "GET" and path == "/login":
            html_body, status_code, extra_headers = handle_admin_login()
            print("login success")

        elif method == "POST" and path == "/login":
            html_body, status_code, extra_headers = process_admin_login(raw_request_data)

        elif path.startswith("/admin"):
            username = get_current_user(raw_request_data)

            if not username:
                html_body = ""
                status_code = "302 Found"
                extra_headers = "Location: /login\r\n"

            else:
                if method == "GET" and path == "/admin":
                    html_body,status_code,extra_headers = handle_admin_dashboard(username)

                elif method == "GET" and path == "/admin/add":
                    html_body, status_code, extra_headers = handle_admin_add_page()

                elif method == "POST" and path == "/admin/add":
                    html_body, status_code, extra_headers = process_admin_add(raw_request_data,username)

                elif method == "GET" and path == "/admin/edit":
                    articles_id = parsed_parms.get("article_id","")[0]
                    html_body, status_code, extra_headers = handle_admin_edit_page(articles_id)

                elif method == "POST" and path == "/admin/edit":
                    html_body, status_code, extra_headers = process_admin_edit(raw_request_data)

                elif method == "POST" and path == "/admin/delete":
                    html_body, status_code, extra_headers = process_admin_delete(raw_request_data)

        #防止乱输入网址
        else:
            html_body = "<h1>404 NOT FOUND</h1>"
            status_code = 404
            extra_headers = ""


        http_response = (
            f"HTTP/1.1 {status_code}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Server: Hardcore-Python-Server\r\n"
            f"{extra_headers}"  # 用于插入 Cookie 或 Location 跳转指令
            "\r\n"
            f"{html_body}"
        )

        client_connection.sendall(http_response.encode('utf-8'))
        client_connection.close()


if __name__ == "__main__":
    start_server()