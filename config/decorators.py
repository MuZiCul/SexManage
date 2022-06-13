from flask import g, redirect, url_for, session, render_template
from functools import wraps


def login_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            try:
                print(g.user.id)
                return fun(*args, **kwargs)
            except Exception as e:
                print('前端session未清空：', str(e))
                session.clear()
                return render_template('login.html')
        else:
            return redirect(url_for('login.login'))
    return wrapper
