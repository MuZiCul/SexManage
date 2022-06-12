import json
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request, jsonify,
)
from config.exts import db
from config.models import SuccessPageUrlModel, FailPageUrlModel, FailImgModel, ConfigModel

bp = Blueprint('data', __name__, url_prefix='/')


@bp.route('/spu', methods=['GET', 'POST'])
def spu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = SuccessPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    DQ = ['垃圾', '劣质', '一般', '清晰', '标清', '高清',
          '超高', '顶级', '巨顶', '动图']
    for i in data[start:end]:
        if i.quality in range(0, 9):
            quality = DQ[i.quality]
        else:
            quality = '暂无评价'
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
               'quality': quality,
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


@bp.route('/success', methods=['GET', 'POST'])
def success():
    all_size = 0
    img_size = 0
    phones = 0
    pcs = 0
    data = SuccessPageUrlModel.query.all()
    for i in data:
        if i.all_size:
            all_size += float(i.all_size)
        if i.img_size:
            img_size += i.img_size
        if i.phoneImg:
            phones += i.phoneImg
        if i.pcImg:
            pcs += i.pcImg
    last_time = ConfigModel.query.filter_by(id=1).first()
    if last_time:
        last_date = last_time.last_date
    else:
        last_date = '不详'
    dic = {'all_size': round(all_size, 2), 'img_size': img_size, 'phones': phones, 'pcs': pcs, 'last_time': last_date}

    return render_template('success.html', data=dic)


@bp.route('/fail', methods=['GET', 'POST'])
def fail():
    return render_template('fail.html')


@bp.route('/failImg', methods=['GET', 'POST'])
def failImg():
    return render_template('failImg.html')


@bp.route('/fpu', methods=['GET', 'POST'])
def fpu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = FailPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        if i.url:
            url = i.url
            if 'data/' in i.url:
                url = url.split('data/')[1]
        else:
            url = '暂无数据'
        dit = {'id': i.id if i.id else '暂无信息',
               'url': url,
               'publish_date': i.publish_date if i.publish_date else '暂无数据',
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'title': i.title if i.title else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/fiu', methods=['GET', 'POST'])
def fiu():
    data = FailImgModel.query.all()
    data_list = []
    for i in data:
        dit = {'id': i.id, 'url': i.url, 'create_date': i.create_date}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/clearFailPage', methods=['GET', 'POST'])
def clearFailPage():
    start = datetime.now()
    failData = FailPageUrlModel.query.all()
    SuccessData = SuccessPageUrlModel.query.all()
    SuccessDataUrlList = []
    for i in SuccessData:
        SuccessDataUrlList.append(i.url)
    for i in failData:
        if i.url in SuccessDataUrlList:
            failPageUrl = FailPageUrlModel.query.filter_by(url=i.url).all()
            for j in failPageUrl:
                pageUrl = FailPageUrlModel.query.filter_by(id=j.id).first()
                db.session.delete(pageUrl)
                db.session.commit()
    end = datetime.now()
    time = (end - start).seconds
    return jsonify({'code': 200, 'msg': '清理完成，本次用时 {:.0f}分 {:.0f}秒'.format(time // 60, time % 60)})
