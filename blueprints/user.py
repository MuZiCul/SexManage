import datetime
import json
import random
import string

from flask import (
    Blueprint,
    render_template,
    request, redirect, url_for, jsonify)

from flask_mail import Message
from werkzeug.security import generate_password_hash

from config.decorators import login_required
from config.exts import db, mail
from config.models import LogModel, ConfigModel, UserModel, EmailCaptchaModel
from utils.Aescrypt import Aescrypt

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/log_data', methods=['GET', 'POST'])
@login_required
def log_data():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = LogModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id if i.id else '暂无信息',
               'level': str(i.level) if i.level else '暂无信息',
               'time': str(i.time) if i.time else '暂无信息',
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'content': i.content if i.content else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return json.dumps(dic, ensure_ascii=False)


@bp.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    return render_template('log.html')


@bp.route('/sensitive', methods=['GET', 'POST'])
@login_required
def sensitive():
    data = ConfigModel.query.filter_by(key='sensitive').first()
    if data:
        if data.value == '1':
            data.value = '0'
            db.session.commit()
        else:
            data.value = '1'
            db.session.commit()

    return redirect(url_for('login.logoff'))


@bp.route('/captcha', methods=['GET', 'POST'])
def getCaptcha():
    username = request.form.get('account')
    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({'code': 400, 'message': '账户不存在！'})
    email = user.email
    if not email:
        return jsonify({'code': 400, 'message': '账户不存在！'})
    getCaptchaTimeReturn = getCaptchaTime(email)
    if getCaptchaTimeReturn:
        return getCaptchaTimeReturn
    try:
        email = email.replace(' ', '')
        captcha = ''.join(random.sample(string.digits, 6))
        message = Message(subject='【木梓爬虫管理登录】验证码',
                          recipients=[email],
                          body=f'【木梓爬虫管理】您的本次验证码是：{captcha}，请勿告知任何人，本次验证码将在几秒后失效！')
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.type = 0
            captcha_model.create_time = datetime.datetime.now()
            db.session.commit()
        else:
            AescryptOb = Aescrypt()
            captcha_model = EmailCaptchaModel(email=email, captcha=generate_password_hash(AescryptOb.encryption(captcha)), type=1)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({'code': 200})
    except Exception as e:
        return jsonify({'code': 400, 'message': e})


def getCaptchaTime(email):
    captcha_model = EmailCaptchaModel.query.filter_by(email=email).order_by(db.text('-create_time')).first()
    if captcha_model:
        time_1 = captcha_model.create_time
        time_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_1_struct = datetime.datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        if total_seconds < 60:
            return jsonify({'code': 400, 'message': '获取验证码过于频繁，请稍后再试！'})
        else:
            return False


