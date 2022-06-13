from flask import Flask, session, g, redirect, url_for
import config.config as config
from config.exts import db, mail
from blueprints import index_bp, data_bp, user_bp, login_bp
from flask_migrate import Migrate
from config.models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(index_bp)
app.register_blueprint(data_bp)
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/logo.ico'))


@app.before_request
def before_request():
    user_id = session.get('userid')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            g.user = user
        except Exception as e:
            print(e)
            g.user = ''


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


@app.teardown_request
def tear(e):
    if e:
        print('teardown_request')
        print(e)
        return redirect(url_for('login.notfound'))


@app.errorhandler(404)
# 捕获404错误
def demo2(error):
    # error接收errorhandler(404)返回的错误内容
    print('404')
    print(error)
    return redirect(url_for('login.notfound'))


if __name__ == '__main__':
    app.run()

