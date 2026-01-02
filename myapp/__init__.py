from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from os import path

db = SQLAlchemy()

DB_URI= 'postgresql://neondb_owner:npg_kehtJmr3vTG1@ep-still-term-ahqmmfs2-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'SHDFJKLHAFBGFJACHKASDUFOEWhrtiyrhfrifhflakflierh'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 180,
    }
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User, Note

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
