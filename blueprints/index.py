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

from blueprints.forms import LoginForm
from config.decorators import login_required
from config.models import UserModel
from utils.Aescrypt import Aescrypt

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if hasattr(g, 'user'):
        return redirect(url_for('article.index'))
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            account = form.account.data
            password = form.password.data
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
                return redirect('/index')
            elif user_username and check_password_hash(user_username.password, AES_password):
                if user_username.logout == 1:
                    flash('400', "status")
                    flash('该账号已停用！', 'msg')
                    return render_template('login.html', data=form)
                session['userid'] = user_username.id
                return redirect('/index')
            else:
                flash('400', "status")
                flash('账户或密码有误！', 'msg')
        else:
            flash('400', "status")
            flash('账户或密码格式有误，请检查！', 'msg')

        return render_template('login.html', data=form)

    else:
        return render_template('login.html')


@bp.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    # if hasattr(g, 'user'):
        return render_template('index.html')