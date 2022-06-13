from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
    g
)
from werkzeug.security import check_password_hash

from config.decorators import login_required
from config.models import UserModel
from utils.Aescrypt import Aescrypt

bp = Blueprint('login', __name__, url_prefix='/')


@bp.route('/404', methods=['GET', 'POST'])
def notfound():
    return render_template('404.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if hasattr(g, 'user'):
        return redirect(url_for('index.index'))
    if request.method == 'POST':
        form = checkLoginForm(request.form.to_dict())
        if form['code'] == 200:
            account = form['account']
            password = form['password']
            AescryptOb = Aescrypt()
            AES_password = AescryptOb.encryption(password)
            user_email = UserModel.query.filter_by(email=account).first()
            user_username = UserModel.query.filter_by(username=account).first()
            if user_email and check_password_hash(user_email.password, AES_password):
                if user_email.logout == 1:
                    flash('400', "status")
                    flash('该账号已停用！', 'msg')
                    return render_template('login.html', data=form)
                session['userid'] = user_email.id
                return redirect(url_for('index.index'))
            elif user_username and check_password_hash(user_username.password, AES_password):
                if user_username.logout == 1:
                    flash('400', "status")
                    flash('该账号已停用！', 'msg')
                    return render_template('login.html', data=form)
                session['userid'] = user_username.id
                return redirect(url_for('index.index'))
            else:
                flash('400', "status")
                flash('账户或密码有误！', 'msg')
        else:
            flash('400', "status")
            flash('账户或密码格式有误，请检查！', 'msg')

        return render_template('login.html', data=form)

    else:
        return render_template('login.html')


@bp.route('/logoff')
def logoff():
    session.clear()
    flash("账号已退出，3秒后跳转到首页！")
    return render_template('login.html')


def checkLoginForm(form):
    account = form['account']
    password = form['password']
    if not account or not password:
        return {'code': 400, 'msg': '账号或密码不能为空'}
    if len(account) < 5 or len(account) > 20 or len(password) < 5 or len(password) > 20:
        return {'code': 400, 'msg': '账号/密码长度应该在5-20位之间'}
    return {'code': 200, 'account': account, 'password': password}
