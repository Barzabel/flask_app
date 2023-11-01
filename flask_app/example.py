from flask import Flask
from flask import request
from flask import render_template, redirect
import json

app = Flask(__name__)


def get_base():
    with open('fake_base.json', "r") as data:
        return json.load(data)


def write_base(user):
    data = get_base()
    with open('fake_base.json', "w") as file:
        data["base"].append(user)
        json.dump(data, file)


@app.route('/')
def index():
    return 'hi'


@app.get('/users')
def get_users():
    users = get_base()['base']
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
    user = {'id': 1, 'first_name': 'vasa'}
    write_base(user)
    return redirect('Users', 302)
