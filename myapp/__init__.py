from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from os import path
from dotenv import load_dotenv


db = SQLAlchemy()
load_dotenv()  
def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 180,
    }
    db.init_app(app)

    from .models import User, Blog

    with app.app_context():
        db.create_all()
        # Seed sample data
        if Blog.query.count() == 0:
            from werkzeug.security import generate_password_hash
            user = User(email='sample@example.com', name='Sample User', password=generate_password_hash('password', method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            sample_blogs = [
                {'title': 'Welcome to My Blog', 'content': 'This is the first blog post. Welcome to our blogging platform!'},
                {'title': 'Getting Started with Flask', 'content': 'Flask is a lightweight web framework for Python. It\'s great for building web applications quickly.'},
                {'title': 'The Importance of Clean Code', 'content': 'Writing clean, readable code is essential for maintainability and collaboration in software development.'}
            ]
            for blog_data in sample_blogs:
                blog = Blog(title=blog_data['title'], content=blog_data['content'], user_id=user.id)
                db.session.add(blog)
            db.session.commit()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


# def create_database():
#     if not path.exists('website/' +DB_NAME):
#         db.create_all()
#         print('Created Application')
