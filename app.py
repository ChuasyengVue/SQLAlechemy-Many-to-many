"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
app.app_context().push()
db.create_all()


app.config['SECRET_KEY'] = 'SecretKey1!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route('/')
def show_user():

    """Redirect to list of users"""

    return redirect ('/users')







@app.route('/users')
def users_listing():

    """Show lists of all users"""
    
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_user():
    
    """Show add form"""

    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def create_users():

    """Creates a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")
    
    

@app.route("/users/<int:user_id>")
def show_details(user_id):

    """Show details about the user"""

    user = User.query.get_or_404(user_id)

    return render_template("details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):

    """Show edit page on user"""

    user = User.query.get_or_404(user_id)
    
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):

    "submit edit user"

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):

    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User '{user.full_name}' deleted.")
    return redirect (f"/users")





@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """This shows the form for user to write a post"""

    user = User.query.get_or_404(user_id)

    return render_template("show_post_form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """This should add post form"""

    user = User.query.get_or_404(user_id)

    new_post= Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user)
    
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post'{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """This shows the users their post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_detail_page.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_form(post_id):
    """Shows the edit page for post form"""

    post = Post.query.get_or_404(post_id)

    return render_template("show_edit_form.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Allows user to edit their post"""

    post = Post.query.get_or_404(post_id)
    post.title= request.form['title']
    post.content= request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):

    """Delete user"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash(f"Post'{post.title}' deleted")

    return redirect (f"/users")




@app.route('/homepage')
def show_homepage():
    """This should show the homepage of Blogly recent posts"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("homepage.html", posts=posts)



@app.route('/tags')
def list_of_tags():
    """Show lists of tags"""

    tags = Tag.query.all()

    return render_template("tag_list.html", tags=tags)


@app.route('/tags/new')
def show_tag_form():

    posts=Post.query.all()

    return render_template('show_tag_form.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def add_tag():

    posts_id = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(posts_id)).all()
    new_tag = Tag(
        name = request.form['name'],
        posts = posts)
    
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):

    tag=Tag.query.get_or_404(tag_id)

    return render_template("tag_detail.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def tag_edit_form(tag_id):

    tag=Tag.query.get_or_404(tag_id)
    
    return render_template("tag_edit.html", tag=tag)



@app.route("/tags/<int:tag_id>/edit", methods=['POST'])
def tag_edit(tag_id):
    """Allows users to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['title']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")



@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tag_delete(tag_id):
    """Delete tags"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")