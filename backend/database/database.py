from flask_sqlalchemy import SQLAlchemy
from flask import session, flash, redirect, url_for
from datetime import datetime

db = SQLAlchemy()

# 定義使用者模型（用來表示使用者表）
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

# 定義留言模型（用來表示留言表）
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 初始化資料庫
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# 驗證使用者是否已經登錄的裝飾器
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap
