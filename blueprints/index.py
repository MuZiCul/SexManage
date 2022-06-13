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

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if hasattr(g, 'user'):
        try:
            data = {'username': g.user.username}
        except Exception as e:
            data = {'username': '暂无信息'}
        return render_template('index.html', data=data)
    else:
        return render_template('login.html')
