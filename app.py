"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


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
def shows_new_form():
    """ displays an add new user form """

    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def add_user():
    """ gets form information
        adds new_user to database
        redirects user to user list
    """

    first_name = request.form['first_name'].lower().capitalize()
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

    return render_template('user_detail.html',
                           full_name=user.full_name,
                           user_id=user_id,
                           url=user.pic_url)


@app.route('/users/<user_id>/edit')
def show_edit_form(user_id):
    """ shows page with new_user-like form
        with field values of current info.
    """
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html',
                           f_name=user.first_name,
                           l_name=user.last_name,
                           user_id=user_id,
                           url=user.pic_url)


@app.route('/users/<user_id>/edit', methods=['POST'])
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


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ deletes users info from database
    """
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
