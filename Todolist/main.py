import socket

import Http_engine
import router
from config import SERVER_HOST,SERVER_PORT


def start_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind((SERVER_HOST,SERVER_PORT))
    client_socket.listen(7)
    print(f"服务器已监听，监听地址为http://{SERVER_HOST}:{SERVER_PORT}")

    while True:
        conn, addr = client_socket.accept()
        raw_request = conn.recv(8192).decode('utf-8')

        method, path, parse_params = Http_engine.handle_request_url(raw_request)
        body_params = Http_engine.handle_request_body(raw_request)
        session_id = Http_engine.get_session_id(raw_request)

        html_body,status_code,extra_headers = router.dispatch_router(method,path,parse_params,body_params,session_id)


        body_byte_len = len(html_body.encode('utf-8'))


        http_response = (
            f"HTTP/1.1 {status_code}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {body_byte_len}\r\n"
            "Server: Hardcore-Python-Server\r\n"
            f"{extra_headers}"  # 用于插入 Cookie 或 Location 跳转指令
            "\r\n"
            f"{html_body}"
        )
        conn.sendall(http_response.encode('utf-8'))
        conn.close()

if __name__ == "__main__":
    start_server()
