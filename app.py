import os
import platform
import click
from flask import Flask
from flask import escape
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user


app = Flask(__name__)
app.debug = True  # 调试模式开关
app.secret_key = os.getenv('SECRET_KEY', 'dev')

# 数据库配置
pf = platform.system()
if pf == 'Windows':
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, os.getenv('DATABASE_FLIE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader  # 登录验证时LoginManger从数据库加载用户
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    content = db.Column(db.String(60))
    is_completed = db.Column(db.Boolean)

'''
@app.context_processor  # todo  上下文处理器  使所有自定义变量在模板中可见
def inject_user():
    user = User.query.get(current_user.id)
    return dict(user=user)
'''

@app.route('/', methods=['GET', 'POST'])  # 主页面
def index():
    if not current_user.is_authenticated:  # 判断用户是否登录
        return redirect(url_for('login'))

    if request.method == 'POST':
        content = request.form.get('content')

        if request.form.get('submit') == '添加任务':  # 增加待办功能
            task = Task(user=current_user.id, content=content, is_completed=False)
            db.session.add(task)

        elif request.form.get('submit') == '保存':  # 修改待办功能
            task = Task.query.get(request.form.get('task_id'))
            task.content = content

        db.session.commit()
        return redirect(url_for('index'))

    tasks = Task.query.filter(Task.user == current_user.id)  # 读取用户待办
    return render_template('index.html', tasks=tasks)  # todo  关联app.context_processor


@login_required
def delete(task_id):  # 删除待办功能
    db.session.delete(Task.query.get(task_id))
    db.session.commit()
    return url_for('index')


@login_required
def complete(task_id):  # 完成待办功能
    task = Task.query.get(task_id)
    task.is_completed = True
    db.session.commit()
    return url_for('index')


@app.route('/login', methods=['GET', 'POST'])  # 用户登录
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter(User.name == username).first()  # 验证
        if user is None:
            flash('该用户不存在')
            return redirect(url_for('login'))
        if user.validate_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('密码错误')
        return redirect((url_for('login')))

    return render_template('login.html')


@app.route('/logout')  # 用户注销
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])  # 注册新用户
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter(User.name == username) is not None:
            flash('该用户名已被注册。')
            redirect(url_for('register'))

        user = User(name=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('成功注册新用户。')
        redirect(url_for('index'))

    return render_template('register.html')


@app.route('/settings', methods=['GET', 'POST'])  # 修改用户信息
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        current_user.name = name
        password = request.form['password']
        current_user.set_password(password)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('settings.html', user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):  # 初始化数据库
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


if __name__ == '__main__':
    app.run()
