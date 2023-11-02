from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
import json
import re

app = Flask(__name__)


def get_base():
    with open('fake_base.json', "r") as data:
        return json.load(data)


def write_base(user):
    data = get_base()
    if len(data['users']) == 0:
        user['id'] = 0
    else:
        user['id'] = data['users'][-1]['id'] + 1
    with open('fake_base.json', "w") as file:
        data['users'].append(user)
        json.dump(data, file)
    return True

def valide(user):
    errors = {}
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    data = get_base()
    if re.match(pattern, user['email']) is None:
        errors['email'] = 'Invalid email'
    if user['nickname'].isdigit():
        errors['nickname'] = 'Invalid nickname'
    for x in data['users']:
        if x['email'] == user['email']:
            errors['email'] = 'email is already used'
        if x['nickname'] == user['nickname']:
            errors['nickname'] = 'nickname is already used'
    return errors

@app.route('/')
def index():
    return 'hi'


@app.get('/users')
def get_users():
    users = get_base()['users']
    name = request.args.get('name')
    if name is None:
        name = ""
    user = list(filter(lambda x: name in x['nickname'], users))
    return render_template('users/index.html', users=user, search=name)


@app.get('/users/<id>')
def get_user_by_id(id):
    users = get_base()['users']
    user = next(filter(lambda x: x['id'] == id, users), None)
    if user is None:
        return 'Page not found', 404
    return render_template('users/show.html', user=user)


@app.route('/users/new', methods=['GET', 'POST'])
def users_form():
    user = {
        'nickname': '',
        'email': ''
    }
    errors = {}
    if request.method == 'GET':
        return render_template('users/users_form.html', user=user, errors=errors)
    elif request.method == 'POST':
        user = request.form.to_dict()
        errors = valide(user)
        if errors == {}:
            write_base(user)
            return redirect(url_for('get_users'))
        return render_template('users/users_form.html', user=user, errors=errors)
