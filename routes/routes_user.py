from urllib.parse import unquote_plus, quote

from models.session import Session
from routes import (
    current_user,
    html_response,
    redirect
)

from utils import log
from models.user import User


# 不要这么 import
# from xx import a, b, c, d, e, f


def login(request):
    """
    登录页面的路由函数
    """
    log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    user_current = current_user(request)
    log('current user', user_current)
    form = request.form()
    user, result = User.login(form)
    if user.is_guest():
        return redirect('/user/login/view?result={}'.format(result))
    else:
        session_id = Session.add(user_id=user.id)
        return redirect('/user/login/view?result={}'.format(result), session_id)


def login_view(request):
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return html_response(
        'login.html',
        username=u.username,
        result=result,
    )


def register(request):
    """
    注册页面的路由函数
    """
    form = request.form()

    u, result = User.register(form)
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(quote(result)))


# @route('/register', 'GET')
def register_view(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return html_response('register.html', result=result)


# RESTFul
# GET /login login_get
# POST /login login_post
# UPDATE /user login_update
# DELETE /user login_delete
#
# GET /login
# POST /login/view
# POST /user/update
# GET /user/delete

# user_get()
# user_post()
# def user:
#     if method == 'GET':
#         return user_get()
#     else:
#         return user_post()


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
    }
    return r
