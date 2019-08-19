from models.user import User
from routes import (
    current_user,
    redirect,
    html_response)
from utils import log


def route_admin(request):
    users = User.all()
    log('in admin')
    return html_response('admin_index.html', users=users)


def edit_password(request):
    u = current_user(request)
    log("in admin edit", u.id, u.password, u)
    return html_response('admin_password_edit.html', user=u)


def update_user_password(request):
    form = request.form()
    # 调用User类中的update方法，处理这个更新密码的请求
    User.update(form)
    return redirect('/admin/users')


def is_admin_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_admin():
            log('管理员')
            return route_function(request)
        else:
            return redirect('/user/login/view')

    return f


def route_dict():
    d = {
        '/admin/users': is_admin_required(route_admin),
        '/admin/edit': is_admin_required(edit_password),
        '/admin/update': is_admin_required(update_user_password),
    }
    return d
