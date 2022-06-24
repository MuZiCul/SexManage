from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    g
)
from werkzeug.security import check_password_hash

from blueprints.forms import LoginForm
from config.exts import db
from config.models import UserModel, EmailCaptchaModel
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
        form = LoginForm(request.form)
        if form.validate():
            account = form.account.data
            password = form.password.data
            captcha = form.captcha.data
            AescryptOb = Aescrypt()
            user_username = UserModel.query.filter_by(username=account).first()
            if not user_username:
                flash('400', "status")
                flash('账户或密码有误！', 'msg')
                return render_template('login.html', data=form)
            captcha_model = EmailCaptchaModel.query.filter_by(email=user_username.email).first()
            if not captcha_model:
                flash('400', "status")
                flash('请先获取验证码！', 'msg')
                return render_template('login.html', data=form)
            if not captcha_model.type:
                flash('400', "status")
                flash('验证码已过期，请重新获取！', 'msg')
                return render_template('login.html', data=form)
            else:
                time_1 = captcha_model.create_time
                time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_1_struct = datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
                time_2_struct = datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
                total_seconds = (time_2_struct - time_1_struct).total_seconds()
                captcha_model.type = 0
                db.session.commit()
                data = AescryptOb.encryption(captcha)
                if total_seconds > 60:
                    flash('400', "status")
                    flash('验证码已过期，请重新获取！', 'msg')
                    return render_template('login.html', data=form)
                elif not check_password_hash(captcha_model.captcha, data):
                    flash('400', "status")
                    flash('验证码不正确！', 'msg')
                    return render_template('login.html', data=form)
            AES_password = AescryptOb.encryption(password)
            if user_username and check_password_hash(user_username.password, AES_password):
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
            flash('验证失败！', 'msg')

        return render_template('login.html', data=form)

    else:
        return render_template('login.html')


@bp.route('/logoff')
def logoff():
    session.clear()
    flash("账号已退出，3秒后跳转到首页！")
    return render_template('login.html')


@bp.route('/110')
def logoff110():
    session.clear()
    flash("账号已退出，3秒后跳转到首页！")
    return render_template('login.html')
