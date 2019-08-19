from flask import render_template, make_response, flash, redirect, url_for
from flask_restful import Resource
from forms import LoginForm, RegisterUserForm, PostForm, DropDownListOfUsers
from flask_login import current_user, login_user, logout_user, login_required
from model import User, Post
from app import api, db
from flask import request
from werkzeug.urls import url_parse
from sqlalchemy import desc, column


class index(Resource):
    # @login_required
    def get(self):
        # user1 = {'username': 'Marta'}
        # user2 = {'username': 'Łukasz'}
        #
        # posts = [
        #     {
        #         'author': user2,
        #         'body': 'Today is a nice weather!'
        #     },
        #     {
        #         'author': user1,
        #         'body': 'I hope i will win in lottery today.'
        #     }
        # ]
        posts = Post.query.order_by(desc(Post.timestamp)).limit(5)
        # users = User.query.order_by(User.username).all()
        form = DropDownListOfUsers()
        return make_response(render_template('index.html', title='Home', posts=posts, form=form))

    def post(self):
        user_id = request.form.get('drop_down_list')
        posts = Post.query.filter_by(user_id=user_id).order_by(desc(Post.timestamp)).limit(5)
        form = DropDownListOfUsers()
        return make_response(render_template('index.html', title='Home', posts=posts, form=form))

# @app.route('/login', methods=['GET', 'POST'])
class login(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        return make_response(render_template('login.html', title='Sign In', form=form))

    def post(self):
        form = LoginForm()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)


class logout(Resource):
    def get(self):
        logout_user()
        return redirect(url_for('index'))

class register(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegisterUserForm()
        return make_response(render_template('register.html', title='Register', form=form))

    def post(self):
        form = RegisterUserForm()
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

class make_post(Resource):
    @login_required
    def get(self):
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        form = PostForm()
        return make_response(render_template('make_post.html', title='Make post', form=form))

    @login_required
    def post(self):
        form = PostForm()

        post = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post was send!')
        return redirect(url_for('index'))


api.add_resource(index, '/', '/index')
api.add_resource(login, '/login_page', methods=['GET', 'POST'])
api.add_resource(logout, '/logout', methods=['GET'])
api.add_resource(register, '/register', methods=['GET', 'POST'])
api.add_resource(make_post, '/make_post', methods=['GET', 'POST'])

