import json
import re
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request, jsonify,
)
from config.decorators import login_required
from config.exts import db
from config.models import SuccessPageUrlModel, FailPageUrlModel, FailImgModel, ConfigModel, DownloadAgainPageUrlModel, \
    ReImgUrlModel, SuccessImgModel

bp = Blueprint('data', __name__, url_prefix='/')


@bp.route('/spu', methods=['GET', 'POST'])
@login_required
def spu():
    try:
        page = int(request.args.get('page'))
        limit = int(request.args.get('limit'))
    except Exception as e:
        page = 1
        limit = 50
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
        kind = '自拍'
        if i.title:
            title = str(i.title).replace(' ', '')
            if '洲]' in title:
                title = title[4:]
                kind = '亚洲'
            elif '真]' in title:
                title = title[4:]
                kind = '写真'
            pnm = re.findall('\[(.*?)]', title, re.S)
            if len(pnm) > 1:
                pnm.reverse()
            if pnm:
                if 'P]' in title:
                    title = title.replace(f'[{pnm[0]}]', '')
        else:
            title = '暂无信息'

        dit = {'id': i.id if i.id else '暂无信息',
               'url': url,
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'title': title,
               'quality': quality,
               'kind': i.kind if i.kind else kind,
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
@login_required
def success():
    last_date = '不详'
    all_size = 0
    img_size = 0
    phones = 0
    pcs = 0
    data = SuccessPageUrlModel.query.order_by(db.text('-create_date')).all()
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
    elif all_size < 10240:
        all_size = str(round(all_size/1024, 2)) + 'GB'
    elif all_size < 102400:
        all_size = str(round(all_size/10240, 2)) + 'TB'
    elif all_size < 1024000:
        all_size = str(round(all_size/102400, 2)) + 'pB'
    dic = {'all_size': all_size, 'img_size': img_size, 'phones': phones, 'pcs': pcs, 'last_time': last_date}

    return render_template('success.html', data=dic)


@bp.route('/fail', methods=['GET', 'POST'])
@login_required
def fail():
    return render_template('fail.html')


@bp.route('/failImg', methods=['GET', 'POST'])
@login_required
def failImg():
    return render_template('failImg.html')


@bp.route('/quality4list', methods=['GET', 'POST'])
@login_required
def quality4list():
    return render_template('quality4list.html')


@bp.route('/reDownload', methods=['GET', 'POST'])
@login_required
def reDownload():
    return render_template('reDownload.html')


@bp.route('/successImg', methods=['GET', 'POST'])
@login_required
def successImg():
    return render_template('successImg.html')


@bp.route('/reImgDownload', methods=['GET', 'POST'])
@login_required
def reImgDownload():
    return render_template('reImgDownload.html')


@bp.route('/fpu', methods=['GET', 'POST'])
@login_required
def fpu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = FailPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id if i.id else '暂无信息',
               'url': i.url,
               'publish_date': i.publish_date if i.publish_date else '暂无数据',
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'reason': str(i.reason) if i.reason else '暂无信息',
               'title': i.title if i.title else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/rpu', methods=['GET', 'POST'])
@login_required
def rpu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = DownloadAgainPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id if i.id is not None else '暂无信息',
               'url': i.url if i.url is not None else '暂无信息',
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'state': i.state if i.state is not None else '暂无信息',
               'count': i.count if i.count is not None else '暂无信息',
               'title': i.title if len(i.title) else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/riu', methods=['GET', 'POST'])
@login_required
def riu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = ReImgUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id if i.id is not None else '暂无信息',
               'url': i.url if i.url is not None else '暂无信息',
               'create_date': str(i.create_date) if i.create_date else '暂无信息',
               'state': i.state if i.state is not None else '暂无信息',
               'count': i.count if i.count is not None else '暂无信息',
               'title': i.title if len(i.title) else '暂无信息'}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/fiu', methods=['GET', 'POST'])
@login_required
def fiu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = FailImgModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id
            , 'url': i.url
            , 'title': i.title if i.title else '暂无信息'
            , 'reason': i.reason if i.reason else '暂无信息'
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/siu', methods=['GET', 'POST'])
@login_required
def siu():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    data = SuccessImgModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for i in data[start:end]:
        dit = {'id': i.id, 'size': i.size, 'title': i.title, 'url': i.url, 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data), 'data': data_list}
    return dic


@bp.route('/delData', methods=['GET', 'POST'])
@login_required
def delData():
    kind = request.form.get('type')
    id = request.form.get('id')
    if kind == 1 or kind == '1':
        spu = SuccessPageUrlModel.query.filter_by(id=id).first()
        db.session.delete(spu)
        db.session.commit()
        return jsonify({'code': 200})
    if kind == 2 or kind == '2':
        fpu = FailPageUrlModel.query.filter_by(id=id).first()
        db.session.delete(fpu)
        db.session.commit()
        return jsonify({'code': 200})
    return jsonify({'code': 400})


@bp.route('/clearFailPage', methods=['GET', 'POST'])
@login_required
def clearFailPage():
    start = datetime.now()
    failData = FailPageUrlModel.query.all()
    SuccessData = SuccessPageUrlModel.query.all()
    SuccessDataUrlList = []
    for i in SuccessData:
        SuccessDataUrlList.append(i.url)
    for i in failData:
        if i.url in SuccessDataUrlList:
            failPageUrl = FailPageUrlModel.query.filter(FailPageUrlModel.url.like("%" + i.url + "%")).all()
            for j in failPageUrl:
                pageUrl = FailPageUrlModel.query.filter_by(id=j.id).first()
                db.session.delete(pageUrl)
                db.session.commit()
    end = datetime.now()
    time = (end - start).seconds
    return jsonify({'code': 200, 'msg': '清理完成，本次用时 {:.0f}分 {:.0f}秒'.format(time // 60, time % 60)})


@bp.route('/clearReDownPage', methods=['GET', 'POST'])
@login_required
def clearReDownPage():
    start = datetime.now()
    failData = DownloadAgainPageUrlModel.query.all()
    SuccessData = SuccessPageUrlModel.query.all()
    SuccessDataUrlList = []
    for i in SuccessData:
        SuccessDataUrlList.append(i.url)
    for i in failData:
        if i.url in SuccessDataUrlList:
            failPageUrl = DownloadAgainPageUrlModel.query.filter(
                DownloadAgainPageUrlModel.url.like("%" + i.url + "%")).all()
            for j in failPageUrl:
                pageUrl = DownloadAgainPageUrlModel.query.filter_by(id=j.id).first()
                db.session.delete(pageUrl)
                db.session.commit()
    end = datetime.now()
    time = (end - start).seconds
    return jsonify({'code': 200, 'msg': '清理完成，本次用时 {:.0f}分 {:.0f}秒'.format(time // 60, time % 60)})


@bp.route('/addAgainDownload', methods=['GET', 'POST'])
@login_required
def addAgainDownload():
    try:
        type = request.form.get('type')
        id = request.form.get('id')
        if type == 1 or type == '1':
            pageUrl = SuccessPageUrlModel.query.filter_by(id=id).first()
            again = DownloadAgainPageUrlModel(url=pageUrl.url, title=pageUrl.title)
            db.session.add(again)
            db.session.commit()
            db.session.delete(pageUrl)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '添加到重新下载列表成功！'})
        elif type == 0 or type == '0':
            pageUrl = FailPageUrlModel.query.filter_by(id=id).first()
            again = DownloadAgainPageUrlModel(url=pageUrl.url, title=pageUrl.title)
            db.session.add(again)
            db.session.commit()
            db.session.delete(pageUrl)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '添加到重新下载列表成功！'})
    except Exception as e:
        return jsonify({'code': 400, 'msg': f'添加失败:{str(e)}'})


@bp.route('/addReImg', methods=['GET', 'POST'])
@login_required
def addReImg():
    try:
        type = request.form.get('type')
        id = request.form.get('id')
        if type == 1 or type == '1':
            pageUrl = SuccessImgModel.query.filter_by(id=id).first()
            again = ReImgUrlModel(url=pageUrl.url, title=pageUrl.title)
            db.session.add(again)
            db.session.commit()
            db.session.delete(pageUrl)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '添加到重新下载列表成功！'})
        elif type == 0 or type == '0':
            pageUrl = FailImgModel.query.filter_by(id=id).first()
            again = ReImgUrlModel(url=pageUrl.url, title=pageUrl.title)
            db.session.add(again)
            db.session.commit()
            db.session.delete(pageUrl)
            db.session.commit()
            return jsonify({'code': 200, 'msg': '添加到重新下载列表成功！'})
    except Exception as e:
        return jsonify({'code': 400, 'msg': f'添加失败:{str(e)}'})

