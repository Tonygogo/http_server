"""
1、导包
2、实例化scoket对象
3、绑定ip 端口
4、监听
5、接收请求
6、处理请求并给出响应
7、关闭连接
"""
import socket,threading

from urls import *

# 发送状态行
def send_header(conn, status_code):
    status_line = "HTTP/1.1 %d OK \r\nContent-Type: text/html; charset=utf-8\r\n\r\n" % status_code
    conn.send(status_line.encode(encoding="utf-8"))

def handler_conn(conn):
    # 接收客户端的数据
    request = []
    data = conn.recv(1024)

    data = data.decode(encoding='utf-8')
    print('客户端的数据：%s' % data)

    # 获取url地址
    # GET /detail HTTP/1.1
    request_line = data.split('\r\n')[0]
    url = request_line.split(' ')[1]
    print('请求的url地址是：%s' % url)

    method = request_line.split(' ')[0]

    # 接收get参数
    params = None
    if 'GET' == method:
        urls = url.split('?')
        if len(urls) > 1:
            url = urls[0]
            # key1=1&key2=2&key3=3
            params = urls[1]

    # 寻找到合适的url
    for urlpattern in urlpatterns:
        u = urlpattern[0]
        if url == u:
            # 先发送状态行
            send_header(conn, 200)
            func = urlpattern[1]
            response = func(params)
            conn.send(response.encode(encoding='utf-8'))
            break
    else:
        # 先发送状态行
        send_header(conn, 404)
        response = page_not_found()
        conn.send(response.encode(encoding='utf-8'))

    # 关闭连接
    conn.close()


def main():
    s = socket.socket()
    s.bind(('127.0.0.1', 8001))
    s.listen(5)
    print("服务器启动：%s:%d.." % ('127.0.0.1', 8001))
    while True:
        conn, addr = s.accept()
        print("与%s:%s建立连接" % addr)
        # 创建子线程
        t = threading.Thread(target=handler_conn, args=(conn,))
        t.start() # 开启线程


if __name__ == '__main__':
    main()
