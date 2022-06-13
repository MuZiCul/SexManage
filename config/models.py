from config.exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    logout = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now)


class SuccessPageUrlModel(db.Model):
    __tablename__ = "spu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), default='')
    title = db.Column(db.String(200), default='')
    quality = db.Column(db.Integer, default=0)
    all_size = db.Column(db.String(50), default='')
    avg_size = db.Column(db.String(50), default='')
    img_size = db.Column(db.Integer, default=0)
    pcImg = db.Column(db.Integer, default=0)
    phoneImg = db.Column(db.Integer, default=0)
    dir = db.Column(db.String(200), default='')
    publish_date = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)


class ConfigModel(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_date = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)


class FailPageUrlModel(db.Model):
    __tablename__ = "fpu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), default='')
    title = db.Column(db.String(200), default='')
    publish_date = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)


class DownloadAgainPageUrlModel(db.Model):
    __tablename__ = "againpage"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), default='')
    title = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)


class FailImgModel(db.Model):
    __tablename__ = "fiu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now)
