import datetime
import json
from flask import (
    Blueprint,
    render_template,
    request, session,
)
import time
import calendar
from config.decorators import login_required
from config.exts import db
from config.models import SuccessPageUrlModel

bp = Blueprint('size', __name__, url_prefix='/')


@bp.route('/stats4day', methods=['GET', 'POST'])
@login_required
def stats4day():
    session['stats'] = 'day'
    return render_template('stats.html')


@bp.route('/stats4month', methods=['GET', 'POST'])
@login_required
def stats4month():
    session['stats'] = 'month'
    return render_template('stats.html')


@bp.route('/stats4year', methods=['GET', 'POST'])
@login_required
def stats4year():
    session['stats'] = 'year'
    return render_template('stats.html')


@bp.route('/stats4hour', methods=['GET', 'POST'])
@login_required
def stats4hour():
    session['stats'] = 'hour'
    return render_template('stats.html')


@bp.route('/statsData', methods=['GET', 'POST'])
@login_required
def statsData():
    if 'day' == session.get('stats'):
        return dayData(request.args)
    elif 'month' == session.get('stats'):
        return monthData(request.args)
    elif 'year' == session.get('stats'):
        return yearData(request.args)
    elif 'hour' == session.get('stats'):
        return hourData(request.args)
    else:
        return dayData(request.args)


def hourData(args):
    page = int(args.get('page'))
    limit = int(args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    year = time.strftime('%Y', time.localtime())
    moth = time.strftime('%m', time.localtime())
    day = time.strftime('%d', time.localtime())
    hour = time.strftime('%H', time.localtime())
    today = now_time[0:13]
    yesterday = f'{year}-{moth}-{int(day)-1}'
    today_month = calendar.monthrange(int(year), int(moth))[1]
    today_month_ = calendar.monthrange(int(year), int(moth)-1)[1]
    today_month_1 = calendar.monthrange(int(year)-1, 12)[1]
    yesterday_month = calendar.monthrange(int(year), int(moth)-1)[1]
    if today_month == int(day):
        yesterday = f'{year}-{int(moth)-1}-{yesterday_month}'
    start_hour = f'{yesterday} {hour}'
    end_hour = f'{today}'
    if int(hour)-1<0:
        if int(day)-2<0:
            if int(moth)-1<0:
                stop_hour = f'{int(year)-1}-12-{today_month_1} {23}'
            else:
                stop_hour = f'{year}-{int(moth)-1}-{today_month_} {23}'
        else:
            stop_hour = f'{year}-{moth}-{int(day)-2} {23}'
    else:
        stop_hour = f'{yesterday} {int(hour)-1}'
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    yesterday_data = SuccessPageUrlModel.query.filter(db.cast(SuccessPageUrlModel.create_date, db.DATE) == db.cast(yesterday, db.DATE)).order_by(db.text('-create_date')).all()
    today_data = SuccessPageUrlModel.query.filter(db.cast(SuccessPageUrlModel.create_date, db.DATE) == db.cast(datetime.datetime.now(), db.DATE)).order_by(db.text('-create_date')).all()
    data_list = []
    for url in today_data:
        create_date = str(url.create_date)[:13]
        if create_date in stop_hour:
            break
        try:
            locals()['dit_' + create_date]['title'] = str(create_date)+'时'
        except Exception as e:
            locals()['dit_' + create_date] = {'title': str(create_date)+'时', 'all_size': 0, 'img_nums': 0, 'pcImg': 0,
                                              'phoneImg': 0, 'quality_1': 0, 'quality0': 0, 'quality1': 0,
                                              'quality2': 0, 'quality3': 0, 'quality4': 0, 'quality5': 0, 'quality6': 0,
                                              'quality7': 0, 'quality8': 0, 'quality9': 0, }
        if url.all_size:
            all_size = url.all_size
            all_size = round(float(all_size), 2)
        else:
            all_size = 0
        locals()['dit_' + create_date]['all_size'] += all_size
        if '0' == str(url.quality):
            locals()['dit_' + create_date]['quality0'] += 1
        if url.quality:
            if url.quality == 1:
                locals()['dit_' + create_date]['quality1'] += 1
            if url.quality == 2:
                locals()['dit_' + create_date]['quality2'] += 1
            if url.quality == 3:
                locals()['dit_' + create_date]['quality3'] += 1
            if url.quality == 4:
                locals()['dit_' + create_date]['quality4'] += 1
            if url.quality == 5:
                locals()['dit_' + create_date]['quality5'] += 1
            if url.quality == 6:
                locals()['dit_' + create_date]['quality6'] += 1
            if url.quality == 7:
                locals()['dit_' + create_date]['quality7'] += 1
            if url.quality == 8:
                locals()['dit_' + create_date]['quality8'] += 1
            if url.quality == 9:
                locals()['dit_' + create_date]['quality9'] += 1
        if url.quality is None:
            locals()['dit_' + create_date]['quality_1'] += 1

        if url.img_size:
            img_size = url.img_size
        else:
            img_size = 0
        locals()['dit_' + create_date]['img_nums'] += float(img_size)
        if url.pcImg:
            pcImg = url.pcImg
        else:
            pcImg = 0
        locals()['dit_' + create_date]['pcImg'] += float(pcImg)
        if url.phoneImg:
            phoneImg = url.phoneImg
        else:
            phoneImg = 0
        locals()['dit_' + create_date]['phoneImg'] += float(phoneImg)

    for url in yesterday_data:
        create_date = str(url.create_date)[:13]
        if create_date in stop_hour:
            break
        try:
            locals()['dit_' + create_date]['title'] = str(create_date)+'时'
        except Exception as e:
            locals()['dit_' + create_date] = {'title': str(create_date)+'时', 'all_size': 0, 'img_nums': 0, 'pcImg': 0,
                                              'phoneImg': 0, 'quality_1': 0, 'quality0': 0, 'quality1': 0,
                                              'quality2': 0, 'quality3': 0, 'quality4': 0, 'quality5': 0, 'quality6': 0,
                                              'quality7': 0, 'quality8': 0, 'quality9': 0, }
        if url.all_size:
            all_size = url.all_size
            all_size = round(float(all_size), 2)
        else:
            all_size = 0
        locals()['dit_' + create_date]['all_size'] += all_size
        if '0' == str(url.quality):
            locals()['dit_' + create_date]['quality0'] += 1
        if url.quality:
            if url.quality == 1:
                locals()['dit_' + create_date]['quality1'] += 1
            if url.quality == 2:
                locals()['dit_' + create_date]['quality2'] += 1
            if url.quality == 3:
                locals()['dit_' + create_date]['quality3'] += 1
            if url.quality == 4:
                locals()['dit_' + create_date]['quality4'] += 1
            if url.quality == 5:
                locals()['dit_' + create_date]['quality5'] += 1
            if url.quality == 6:
                locals()['dit_' + create_date]['quality6'] += 1
            if url.quality == 7:
                locals()['dit_' + create_date]['quality7'] += 1
            if url.quality == 8:
                locals()['dit_' + create_date]['quality8'] += 1
            if url.quality == 9:
                locals()['dit_' + create_date]['quality9'] += 1
        if url.quality is None:
            locals()['dit_' + create_date]['quality_1'] += 1

        if url.img_size:
            img_size = url.img_size
        else:
            img_size = 0
        locals()['dit_' + create_date]['img_nums'] += float(img_size)
        if url.pcImg:
            pcImg = url.pcImg
        else:
            pcImg = 0
        locals()['dit_' + create_date]['pcImg'] += float(pcImg)
        if url.phoneImg:
            phoneImg = url.phoneImg
        else:
            phoneImg = 0
        locals()['dit_' + create_date]['phoneImg'] += float(phoneImg)

    for i in range(0, 25):
        try:
            if len(str(i)) == 2:
                data_list.append(locals()['dit_' + f'{start_hour[0:10]} {i}'])
            elif len(str(i)) == 1:
                data_list.append(locals()['dit_' + f'{start_hour[0:10]} 0{i}'])
        except Exception as e:
            continue
    for i in range(0, 25):
        try:
            if len(str(i)) == 2:
                data_list.append(locals()['dit_' + f'{end_hour[0:10]} {i}'])
            elif len(str(i)) == 1:
                data_list.append(locals()['dit_' + f'{end_hour[0:10]} 0{i}'])
        except Exception as e:
            continue
    data_list.reverse()
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data_list), 'data': data_list[start:end]}
    return json.dumps(dic, ensure_ascii=False)


def dayData(args):
    page = int(args.get('page'))
    limit = int(args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    year = time.strftime('%Y', time.localtime())
    moth = time.strftime('%m', time.localtime())
    day = time.strftime('%d', time.localtime())
    monthRange = calendar.monthrange(int(year), int(moth) - 1)
    lastMonth = str(int(moth) - 1)
    if len(lastMonth) == 1:
        lastMonth = '0' + lastMonth
    lastMonthFirst = f'{year}-{lastMonth}-01'
    data = SuccessPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for url in data:
        create_date = str(url.create_date)[:10]
        if create_date in lastMonthFirst:
            break
        try:
            locals()['dit_' + create_date]['title'] = create_date
        except Exception as e:
            locals()['dit_' + create_date] = {'title': create_date, 'all_size': 0, 'img_nums': 0, 'pcImg': 0,
                                              'phoneImg': 0, 'quality_1': 0, 'quality0': 0, 'quality1': 0,
                                              'quality2': 0, 'quality3': 0, 'quality4': 0, 'quality5': 0, 'quality6': 0,
                                              'quality7': 0, 'quality8': 0, 'quality9': 0, }
        if url.all_size:
            all_size = url.all_size
            all_size = round(float(all_size), 2)
        else:
            all_size = 0
        locals()['dit_' + create_date]['all_size'] += all_size
        if '0' == str(url.quality):
            locals()['dit_' + create_date]['quality0'] += 1
        if url.quality:
            if url.quality == 1:
                locals()['dit_' + create_date]['quality1'] += 1
            if url.quality == 2:
                locals()['dit_' + create_date]['quality2'] += 1
            if url.quality == 3:
                locals()['dit_' + create_date]['quality3'] += 1
            if url.quality == 4:
                locals()['dit_' + create_date]['quality4'] += 1
            if url.quality == 5:
                locals()['dit_' + create_date]['quality5'] += 1
            if url.quality == 6:
                locals()['dit_' + create_date]['quality6'] += 1
            if url.quality == 7:
                locals()['dit_' + create_date]['quality7'] += 1
            if url.quality == 8:
                locals()['dit_' + create_date]['quality8'] += 1
            if url.quality == 9:
                locals()['dit_' + create_date]['quality9'] += 1
        if url.quality is None:
            locals()['dit_' + create_date]['quality_1'] += 1

        if url.img_size:
            img_size = url.img_size
        else:
            img_size = 0
        locals()['dit_' + create_date]['img_nums'] += float(img_size)
        if url.pcImg:
            pcImg = url.pcImg
        else:
            pcImg = 0
        locals()['dit_' + create_date]['pcImg'] += float(pcImg)
        if url.phoneImg:
            phoneImg = url.phoneImg
        else:
            phoneImg = 0
        locals()['dit_' + create_date]['phoneImg'] += float(phoneImg)
    for i in range(1, int(monthRange[1]) + 1):
        try:
            data_list.append(locals()['dit_' + f'{year}-{lastMonth}-{i}'])
        except Exception as e:
            continue
    for i in range(1, int(day) + 1):
        try:
            data_list.append(locals()['dit_' + f'{year}-{moth}-{i}'])
        except Exception as e:
            continue
    data_list.reverse()
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data_list), 'data': data_list[start:end]}
    return json.dumps(dic, ensure_ascii=False)


def monthData(args):
    page = int(args.get('page'))
    limit = int(args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    year = time.strftime('%Y', time.localtime())
    moth = time.strftime('%m', time.localtime())
    yearFirst = f'{year}-01'
    data = SuccessPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for url in data:
        create_date = str(url.create_date)[:7]
        if create_date in yearFirst:
            break
        try:
            locals()['dit_' + create_date]['title'] = create_date
        except Exception as e:
            locals()['dit_' + create_date] = {'title': create_date, 'all_size': 0, 'img_nums': 0, 'pcImg': 0,
                                              'phoneImg': 0, 'quality_1': 0, 'quality0': 0, 'quality1': 0,
                                              'quality2': 0, 'quality3': 0, 'quality4': 0, 'quality5': 0, 'quality6': 0,
                                              'quality7': 0, 'quality8': 0, 'quality9': 0, }
        if '0' == str(url.quality):
            locals()['dit_' + create_date]['quality0'] += 1
        if url.quality:
            if url.quality == 1:
                locals()['dit_' + create_date]['quality1'] += 1
            if url.quality == 2:
                locals()['dit_' + create_date]['quality2'] += 1
            if url.quality == 3:
                locals()['dit_' + create_date]['quality3'] += 1
            if url.quality == 4:
                locals()['dit_' + create_date]['quality4'] += 1
            if url.quality == 5:
                locals()['dit_' + create_date]['quality5'] += 1
            if url.quality == 6:
                locals()['dit_' + create_date]['quality6'] += 1
            if url.quality == 7:
                locals()['dit_' + create_date]['quality7'] += 1
            if url.quality == 8:
                locals()['dit_' + create_date]['quality8'] += 1
            if url.quality == 9:
                locals()['dit_' + create_date]['quality9'] += 1
        if url.quality is None:
            locals()['dit_' + create_date]['quality_1'] += 1
        if url.all_size:
            all_size = url.all_size
            all_size = round(float(all_size), 2)
        else:
            all_size = 0
        locals()['dit_' + create_date]['all_size'] += all_size
        if url.img_size:
            img_size = url.img_size
        else:
            img_size = 0
        locals()['dit_' + create_date]['img_nums'] += float(img_size)
        if url.pcImg:
            pcImg = url.pcImg
        else:
            pcImg = 0
        locals()['dit_' + create_date]['pcImg'] += float(pcImg)
        if url.phoneImg:
            phoneImg = url.phoneImg
        else:
            phoneImg = 0
        locals()['dit_' + create_date]['phoneImg'] += float(phoneImg)
    for i in range(1, int(moth) + 1):
        try:
            if len(str(i)) == 1:
                timothy = '0' + str(i)
            else:
                timothy = i
            data_list.append(locals()['dit_' + f'{year}-{timothy}'])
        except Exception as e:
            continue
    data_list.reverse()
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data_list), 'data': data_list[start:end]}
    return json.dumps(dic, ensure_ascii=False)


def yearData(args):
    page = int(args.get('page'))
    limit = int(args.get('limit'))
    start = (page - 1) * limit
    end = start + limit
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    year = time.strftime('%Y', time.localtime())
    year = int(year) - 5
    yearFirst = f'{year}'
    data = SuccessPageUrlModel.query.order_by(db.text('-create_date')).all()
    data_list = []
    for url in data:
        create_date = str(url.create_date)[:4]
        if create_date in yearFirst:
            break
        try:
            locals()['dit_' + create_date]['title'] = create_date
        except Exception as e:
            locals()['dit_' + create_date] = {'title': create_date, 'all_size': 0, 'img_nums': 0, 'pcImg': 0,
                                              'phoneImg': 0, 'quality_1': 0, 'quality0': 0, 'quality1': 0,
                                              'quality2': 0, 'quality3': 0, 'quality4': 0, 'quality5': 0, 'quality6': 0,
                                              'quality7': 0, 'quality8': 0, 'quality9': 0, }
        if '0' == str(url.quality):
            locals()['dit_' + create_date]['quality0'] += 1
        if url.quality:
            if url.quality == 1:
                locals()['dit_' + create_date]['quality1'] += 1
            if url.quality == 2:
                locals()['dit_' + create_date]['quality2'] += 1
            if url.quality == 3:
                locals()['dit_' + create_date]['quality3'] += 1
            if url.quality == 4:
                locals()['dit_' + create_date]['quality4'] += 1
            if url.quality == 5:
                locals()['dit_' + create_date]['quality5'] += 1
            if url.quality == 6:
                locals()['dit_' + create_date]['quality6'] += 1
            if url.quality == 7:
                locals()['dit_' + create_date]['quality7'] += 1
            if url.quality == 8:
                locals()['dit_' + create_date]['quality8'] += 1
            if url.quality == 9:
                locals()['dit_' + create_date]['quality9'] += 1
        if url.quality is None:
            locals()['dit_' + create_date]['quality_1'] += 1
        if url.all_size:
            all_size = url.all_size
            all_size = round(float(all_size), 2)
        else:
            all_size = 0
        locals()['dit_' + create_date]['all_size'] += all_size
        if url.img_size:
            img_size = url.img_size
        else:
            img_size = 0
        locals()['dit_' + create_date]['img_nums'] += float(img_size)
        if url.pcImg:
            pcImg = url.pcImg
        else:
            pcImg = 0
        locals()['dit_' + create_date]['pcImg'] += float(pcImg)
        if url.phoneImg:
            phoneImg = url.phoneImg
        else:
            phoneImg = 0
        locals()['dit_' + create_date]['phoneImg'] += float(phoneImg)
    for i in range(year, year + 6):
        try:
            data_list.append(locals()['dit_' + str(i)])
        except Exception as e:
            continue
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': len(data_list), 'data': data_list[start:end]}
    return json.dumps(dic, ensure_ascii=False)
