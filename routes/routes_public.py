from models.Message import Message
from routes import (
    current_user,
    html_response,
    redirect
)
from utils import log


def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user(request)
    return html_response('index.html', username=u.username)


def static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\n\r\n'
        img = header + f.read()
        return img


def message_index(request):
    ms = Message.all()
    return html_response('messages.html', messages=ms)


def message_add_get(request):
    """
    主页的处理函数, 返回主页的响应
    GET /messages?message=123&author=admin HTTP/1.1
    Host: localhost:3000
    """
    # log('本次请求的 method', request.method)
    data = request.query
    Message.new(data)
    # log('get', data)
    # 应该在这里保存 message_list
    return redirect('/messages/index')


def message_add_post(request):
    log('本次请求的 method', request.method)
    data = request.form()
    Message.new(data)
    # log('post', data)
    # 应该在这里保存 message_list
    return redirect('/messages/index')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/': index,
        '/static': static,
        '/messages/index': message_index,
        '/messages/add/get': message_add_get,
        '/messages/add/post': message_add_post,
    }
    return d
