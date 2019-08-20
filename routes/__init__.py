import json
import os.path
from urllib.parse import quote

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class GuaTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)


# parent = os.path.dirname(os.path.dirname(__file__))
# path = os.path.join(parent, 'templates')
# # 创建一个加载器, jinja2 会从这个目录中加载模板
# loader = FileSystemLoader(path)
# # 用加载器创建一个环境, 有了它才能读取模板文件
# e = Environment(loader=loader)

# e = initialized_environment()


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            if u is None:
                return User.guest()
            else:
                return u
    else:
        return User.guest()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=admin
    """
    header = 'HTTP/1.1 {} OK r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, session_id=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """

    h = {
        'Location': url,
    }
    if isinstance(session_id, str):
        h.update({
            'Set-Cookie': 'session_id={}; path=/'.format(session_id)
        })
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    # HTTP 1.1 302 ok
    # Location: /todo
    #
    response = formatted_header(h, 302) + '\r\n'
    return response.encode()


def html_response(filename, **kwargs):
    body = GuaTemplate.render(filename, **kwargs)

    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    headers = {
        'Content-Type': 'text/html',
    }
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data):
    body = json.dumps(data, indent=2, ensure_ascii=False)
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    headers = {
        'Content-Type': 'application/json',
    }
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f(request):
        # log('login_required')
        u = current_user(request)
        if u.is_guest():
            log('游客用户')
            return redirect('/user/login/view')
        else:
            log('已登录用户', route_function)
            return route_function(request)

    return f

# @login_required
# def f():
#     pass
# '/f': login_required(f)
