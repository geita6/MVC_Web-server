from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    # 链接中有user_id，查看其他人的微博；
    if 'user_id' in request.query:
        user_id = request.query['user_id']
        u = User.find_by(id=int(user_id))
        # log('跳', u)
        weibos = Weibo.find_all(user_id=u.id)

    # 链接中没有user_id，查看自己的微博；
    else:
        u = current_user(request)
        # log('不跳', u)
        weibos = Weibo.find_all(user_id=u.id)

    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user(request)
    form = request.form()
    # log("weibo add form", form)
    Weibo.add(form, u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


# 修改删除weibo函数
def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    # 注意删除所有微博对应评论
    cs = Comment.find_all(weibo_id=weibo_id)
    for c in cs:
        c.delete(c.id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['id'])
    w = Weibo.find_by(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    form = request.form()
    Weibo.update(form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    # log('comment add form', form)
    weibo_id = int(form['weibo_id'])

    Comment.add(form, u.id, weibo_id)

    # log('comment add', u, form)
    return redirect('/weibo/index')


# 新建删除评论函数
def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')


# 新建修改评论 的 页面 函数
def comment_edit(request):
    comment_id = int(request.query['id'])
    c = Comment.find_by(id=comment_id)
    return html_response('comment_edit.html', comment=c)


# 新建修改评论 的 更新数据 函数
def comment_update(request):
    form = request.form()
    Comment.update(form)
    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    def f(request):
        # log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            log('能删除或修改微博')
            return route_function(request)
        else:
            log('不能删除或修改微博')
            return redirect('/weibo/index')

    return f


# 新建 修改评论的权限认证 函数
def comment_owner_required(route_function):
    def f(request):
        # log('comment_owner_required  in')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']

        c = Comment.find_by(id=int(comment_id))
        if c.user_id == u.id:
            log('能修改评论')
            return route_function(request)
        else:
            log('不能修改评论')
            return redirect('/weibo/index')

    return f


# 新建 删除评论的权限认证 函数
def comment_owner_or_weibo_owner_required(route_function):
    def f(request):
        # log('comment_owner_or_weibo_owner_required  in')
        u = current_user(request)
        if 'id' in request.query:
            comment_id = request.query['id']
        else:
            comment_id = request.form()['id']
        c = Comment.find_by(id=int(comment_id))
        w = Weibo.find_by(id=c.weibo_id)

        if u.id == c.user_id or u.id == w.user_id:
            log('能删除评论')
            return route_function(request)
        else:
            log('不能删除评论')
            return redirect('/weibo/index')

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/delete': login_required(comment_owner_or_weibo_owner_required(comment_delete)),
        '/comment/edit': login_required(comment_owner_required(comment_edit)),
        '/comment/update': login_required(comment_owner_required(comment_update)),
    }
    return d
