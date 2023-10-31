from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila', 'Andrey']


@app.route('/')
def index():
    return 'hi'


@app.get('/users')
def get_users():
    name = request.args.get('name')
    if name is None:
        name = ""
    user = list(filter(lambda x: name in x, users))
    return render_template('users/index.html', users=user, search=name)


@app.get('/users/<id>')
def get_user_by_id(id):
    return render_template('users/show.html', id=id)


@app.post('/users')
def users_post():
    return 'Users', 302
