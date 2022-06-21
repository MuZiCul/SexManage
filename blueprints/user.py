import json

from flask import (
    Blueprint,
    render_template,
    request, redirect, url_for)

from config.decorators import login_required
from config.exts import db
from config.models import LogModel, ConfigModel

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


