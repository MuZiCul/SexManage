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

bp = Blueprint('user', __name__, url_prefix='/')


