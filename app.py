"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route('/')
def redirects_to_user_list():
    """ redirects to users list """

    return redirect("/users")


@app.route('/users')
def shows_users_list():
    """ displays up to date list of users """

    users = User.query.all()
    # users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('user_listing.html',
                           users=users)


@app.route('/users/new')
def shows_new_user_form():
    """ displays an add new user form """

    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """ gets form information
        adds new_user to database
        redirects user to user list
    """

    first_name = request.form['first_name'].lower().capitalize()
    if first_name == '':
        flash('Please Enter a First Name')
        return redirect("/users/new")
    last_name = request.form['last_name'].lower().capitalize()
    pic_url = request.form['pic_url'] or None
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    pic_url=pic_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """ shows page with users current info
        with buttons to edit their info
    """
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template('user_detail.html',
                           full_name=user.full_name,
                           user_id=user_id,
                           url=user.pic_url,
                           posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """ shows page with new_user-like form
        with field values of current info.
    """
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html',
                           f_name=user.first_name,
                           l_name=user.last_name,
                           user_id=user_id,
                           url=user.pic_url)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_info(user_id):
    """ changes user info in database and redirects user to users list.
    """
    user = User.query.get_or_404(user_id)

    f_name = request.form['first_name'].lower().capitalize()
    l_name = request.form['last_name'].lower().capitalize()
    p_url = request.form['pic_url']

    user.first_name = f_name
    user.last_name = l_name
    user.pic_url = p_url

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ deletes users info from database
    """
    user = User.query.get_or_404(user_id)
    # delete all users posts first

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

##################################################################
############################### POST ROUTES ######################
##################################################################


@app.route('/users/<int:user_id>/posts/new')
def display_new_post_form(user_id):
    """ Render add new post form """
    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """ Handle add form; add post and redirect to the user detail page. """

    title = request.form['title']
    content = request.form['content']

    user = User.query.get_or_404(user_id)

    user.posts.append(Post(title=title,
                           content=content,
                           user_id=user_id))

    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post_detail(post_id):
    """ show a post with buttons to edit and delete"""
    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """ Show form to edit a post, and to cancel (back to user page). """
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post_form(post_id):
    """ Handle editing of a post. Redirect back to the post view.  """
    title = request.form['title']
    content = request.form['content']
# implement validation
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f'/posts/{post_id}')

# fix view function names... again

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ Delete the post """
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
