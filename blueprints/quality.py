import json

from flask import (
    Blueprint,
    request, render_template, g, session
)
from sqlalchemy import func

from config.decorators import login_required
from config.exts import db
from config.models import SuccessPageUrlModel, ConfigModel

bp = Blueprint('quality', __name__, url_prefix='/')


@bp.route('/quality', methods=['GET', 'POST'])
@login_required
def qualityPage():
    quality = request.args.get('quality')
    session['quality'] = quality
    last_date = '不详'
    all_size = 0
    img_size = 0
    phones = 0
    pcs = 0
    data = SuccessPageUrlModel.query.filter_by(quality=quality).order_by(db.text('-create_date')).all()
    for i in data:
        if i.all_size:
            all_size += float(i.all_size)
        if i.img_size:
            img_size += i.img_size
        if i.phoneImg:
            phones += i.phoneImg
        if i.pcImg:
            pcs += i.pcImg
    if data:
        if data[0].create_date:
            last_date = str(data[0].create_date)
    if all_size < 1024:
        all_size = str(round(all_size, 2)) + 'MB'
    elif all_size < 1024*1024:
        all_size = str(round(all_size/1024, 2)) + 'GB'
    elif all_size < 1024*1024*1024:
        all_size = str(round(all_size/1024/1024, 2)) + 'TB'
    elif all_size < 1024*1024*1024*1024:
        all_size = str(round(all_size/1024/1024/1024, 2)) + 'PB'
    dic = {'all_size': all_size, 'img_size': img_size, 'phones': phones, 'pcs': pcs, 'last_time': last_date}
    return render_template('quality.html', data=dic)


@bp.route('/getQuality', methods=['GET', 'POST'])
@login_required
def get_quality():
    quality = session.get('quality')
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = SuccessPageUrlModel.query.filter_by(quality=quality).order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        if i.url:
            url = i.url
            if 'data/' in i.url:
                url = url.split('data/')[1]
        else:
            url = '暂无数据'
        if i.publish_date:
            publish_date = i.publish_date
            if 'Posted' in publish_date:
                publish_date = publish_date[7:]
        else:
            publish_date = '暂无数据'

        dit = {'id': i.id if i.id else '暂无信息',
               'url': url,
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'title': i.title if i.title else '暂无信息',
               'all_size': i.all_size if i.all_size else '暂无信息',
               'avg_size': i.avg_size if i.avg_size else '暂无信息',
               'pcImg': i.pcImg if i.pcImg == 0 or i.pcImg else '暂无信息',
               'dir': i.dir if i.dir else '暂无信息',
               'publish_date': publish_date,
               'phoneImg': i.phoneImg if i.phoneImg == 0 or i.phoneImg else '暂无信息',
               'img_size': i.img_size if i.img_size else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return json.dumps(dic, ensure_ascii=False)


@bp.route('/list4quality', methods=['GET', 'POST'])
@login_required
def list4quality():
    data_list = []
    qualityNum = db.session.query(SuccessPageUrlModel.quality, func.count(SuccessPageUrlModel.id)).group_by(
        SuccessPageUrlModel.quality).all()
    quality_size = db.session.query(SuccessPageUrlModel.quality, func.sum(SuccessPageUrlModel.img_size)).group_by(
        SuccessPageUrlModel.quality).all()
    qualityImg = db.session.query(SuccessPageUrlModel.quality, func.sum(SuccessPageUrlModel.pcImg)).group_by(
        SuccessPageUrlModel.quality).all()
    qualityPhoneImg = db.session.query(SuccessPageUrlModel.quality, func.sum(SuccessPageUrlModel.phoneImg)).group_by(
        SuccessPageUrlModel.quality).all()
    ditNone = {'title': -1, 'qualityNum': 0, 'qualityAll_size': 0, 'qualityPcImg': 0, 'qualityPhoneImg': 0}
    for i in range(0, 10):
        locals()['dit' + str(i)] = {'title': i, 'qualityNum': 0, 'qualityAll_size': 0, 'qualityPcImg': 0,
                                    'qualityPhoneImg': 0}
    for i in qualityNum:
        locals()['dit' + str(i[0])]['qualityNum'] = str(i[1])
    for i in quality_size:
        locals()['dit' + str(i[0])]['qualityAll_size'] = str(i[1])
    for i in qualityImg:
        locals()['dit' + str(i[0])]['qualityPcImg'] = str(i[1])
    for i in qualityPhoneImg:
        locals()['dit' + str(i[0])]['qualityPhoneImg'] = str(i[1])
    for i in range(0, 10):
        data_list.append(locals()['dit' + str(i)])
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': 11, 'data': data_list}
    return dic
