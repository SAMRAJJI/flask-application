from myapp import create_app, db
from myapp.models import Blog, User

app = create_app()

with app.app_context():
    # Check if sample blogs already exist
    if Blog.query.count() == 0:
        # Get the first user or create one
        user = User.query.first()
        if not user:
            user = User(email='sample@example.com', name='Sample User', password='hashedpassword')
            db.session.add(user)
            db.session.commit()

        sample_blogs = [
            {
                'title': 'Welcome to My Blog',
                'content': 'This is the first blog post. Welcome to our blogging platform!'
            },
            {
                'title': 'Getting Started with Flask',
                'content': 'Flask is a lightweight web framework for Python. It\'s great for building web applications quickly.'
            },
            {
                'title': 'The Importance of Clean Code',
                'content': 'Writing clean, readable code is essential for maintainability and collaboration in software development.'
            }
        ]

        for blog_data in sample_blogs:
            blog = Blog(
                title=blog_data['title'],
                content=blog_data['content'],
                user_id=user.id
            )
            db.session.add(blog)

        db.session.commit()
        print("Sample blogs added successfully!")
    else:
        print("Sample blogs already exist.")