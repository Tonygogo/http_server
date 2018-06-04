from jinja2 import Environment, PackageLoader


def list_user(params=None):
    try:
        # 获取参数
        param_dict = format_params(params)
        # 获取模板
        env = Environment(loader=PackageLoader('templates', ''))
        template = env.get_template('index.html')
        content = template.render()
        # 给出响应
        return content
    except Exception as e:
        page_not_found(params)


def detail(params=None):
    try:
        # 获取参数
        param_dict = format_params(params)
        id = param_dict.get('id')
        # 获取模板
        env = Environment(loader=PackageLoader('templates', ''))
        template = env.get_template('detail.html')
        content = template.render({'id': id})
        # 给出响应
        return content
    except Exception as e:
        page_not_found(params)


def page_not_found(params=None):
    return "<h1>Page Not Found</h1>"


# 格式化参数：# key1=1&key2=2&key3=3，把参数返回一个字典
def format_params(params):
    param_dict = {}
    if not params:
        return param_dict

    params_arr = params.split('&')
    for param in params_arr:
        # param--->key1=1
        param_dict[param.split('=')[0]] = param.split('=')[1]
    print('请求参数：%s' % param_dict)
    return param_dict