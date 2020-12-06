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
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FLIE', 'data.db'))
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


@app.context_processor  # todo  上下文处理器  使所有自定义变量在模板中可见
def inject_user():
    user = User.query.get(current_user.id)
    return dict(user=user)


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

        user = User.query.filter(User.name == username)
        if user.validate_password(password):  # 验证
            login_user(user)
            return redirect(url_for('index'))

        flash('您输入的用户名或密码无效。')
        return redirect((url_for('login')))

    return render_template('login.html')


@app.route('/logout')  # 用户注销
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup')  # todo 继续
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter(User.name == username)
        if user.validate_password(password):  # 验证
            login_user(user)
            return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/settings', methods=['GET', 'POST'])  # 修改用户信息
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        current_user.name = name
        password = request.form['password']
        current_user.password_hash = current_user.set_password(password)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('settings.html', user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

'''
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=False, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.name = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(name=username)
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')
'''
'''
# 虚拟数据
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'zouxlin'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Task(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
'''

if __name__ == '__main__':
    app.run()
