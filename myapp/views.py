from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Blog
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# ---------------- BLOG ROUTES ---------------- #

@views.route('/blogs')
@login_required
def blogs():
    posts = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template("blogs.html", posts=posts)

@views.route('/blog/add', methods=['GET', 'POST'])
@login_required
def add_blog():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        new_blog = Blog(
            title=title,
            content=content,
            user_id=current_user.id
        )

        db.session.add(new_blog)
        db.session.commit()

        flash("Blog added successfully!", "success")
        return redirect(url_for('views.blogs'))

    return render_template("add_blog.html")

@views.route('/blog/<int:id>')
@login_required
def view_blog(id):
    post = Blog.query.get_or_404(id)
    return render_template("view_blog.html", post=post)

@views.route('/blog/delete/<int:id>')
@login_required
def delete_blog(id):
    post = Blog.query.get_or_404(id)

    if post.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('views.blogs'))

    db.session.delete(post)
    db.session.commit()
    flash("Blog deleted!", "success")

    return redirect(url_for('views.blogs'))
