from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, login_user, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("logged in successfully", category= 'Success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("incorrect password", category=error)
        else:
            flash("no user exist", category='error')

    return render_template("login.html", text="Testing", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sigin', methods=['GET', 'POST'])
def sigup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('confirmpassword')
        
        user = User.query.filter_by(email = email).first()
        if user:
            flash("the user is already exist", category='error')
        elif len(email)< 4:
            flash('email must more than 4 characters', category='error')
        elif len(name)<3:
            flash('name must more than 3 characters', category='error')
        elif password != password2:
            flash('password doesnt match', category='error')
        elif len(password) <4:
            flash('password must be meet the condition', category='error')
        else:
            new_user = User(email=email, name = name, password= generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('account created successfully', category='success')
            return redirect(url_for('views.home'))


    return render_template("sigin.html", user = current_user)