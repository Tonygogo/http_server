from wsgiref.simple_server import make_server
from urls import *
# def run_server(environ, start_response):
#     # 设置HTTP响应的状态码和头信息
#     start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])
#     return ['这是一个测试。。。'.encode(encoding='utf-8'), ]


# 设置HTTP响应的状态码和头信息
def send_header(start_response, status_code):
    start_response('%d OK' % status_code, [('Content-Type', 'text/html;charset=utf8'), ])


def run_server(environ, start_response):

    # 获取请求方式
    method = environ.get('REQUEST_METHOD')
    url = environ.get('PATH_INFO')
    query_string = environ.get('QUERY_STRING')
    if 'GET' == method:
        pass
    elif 'POST' == method:
        request_body_size = int(environ.get('CONTENT_LENGTH'))
        request_body = environ.get('wsgi.input')
        if request_body:
            query_string = request_body.read(request_body_size).decode(encoding='utf-8')

    # 寻找到合适的url
    response = None
    for urlpattern in urlpatterns:
        u = urlpattern[0]
        if url == u:
            # 先发送状态行
            send_header(start_response, 200)
            func = urlpattern[1]
            response = func(query_string)
            break
    else:
        # 先发送状态行
        send_header(start_response, 404)
        response = page_not_found()

    return [response.encode(encoding='utf-8'), ]


if __name__ == '__main__':
    server = make_server(host='127.0.0.1', port=8002, app=run_server)
    server.serve_forever()