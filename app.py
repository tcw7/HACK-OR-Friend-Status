#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

from werkzeug.utils import redirect
from forms import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    friends = db.relationship('Friend', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friendname = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    services = db.relationship('Service', backref='friend', lazy=True)

    def __repr__(self):
        return '<Friend %r>' % self.friendname


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicename = db.Column(db.String(120), nullable=False)
    serviceidentifier = db.Column(db.String(120), nullable=False)
    servicestatus = db.Column(db.String(120), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey(
        'friend.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.servicename


db.create_all()

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/<string:user_name>')
def home_user(user_name):
    user_name = user_name
    friend_names = ['Andre', 'Sean', 'Shenan']
    return render_template('pages/placeholder.home.html', user_name=user_name, friend_names=friend_names)


@app.route('/show_friend?friend=<string:friend>')
def show_friend(friend):
    current_friend = friend
    friend_statuses = [
        {
            'service': 'Discord',
            'status': 'Active'
        },
        {
            'service': 'Slack',
            'status': 'Idle'
        },
        {
            'service': 'Zulip',
            'status': 'Idle'
        }
    ]
    return render_template('pages/placeholder.about.html', current_friend=current_friend, friend_statuses=friend_statuses)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        login_form = LoginForm(request.form)
        return render_template('forms/login.html', form=login_form)

    if request.method == 'POST':
        login_name = request.form.get('name')
        login_password = request.form.get('password')
        print(login_name, login_password)
        lookup = User.query.filter_by(name=login_name).first()
        print(lookup)
        if login_name == lookup.name:
            if login_password == lookup.password:
                session_user = login_name
                print(session_user)
        return redirect(f'/{session_user}')


@app.route('/register', methods=['GET', 'POST'])
def register():

    # user is visiting registration page for the first time
    if request.method == 'GET':
        register_form = RegisterForm(request.form)
        return render_template('forms/register.html', form=register_form)

    # user has submitted a request to register
    if request.method == 'POST':
        user = User(name=request.form.get("name"), email=request.form.get(
            "email"), password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
