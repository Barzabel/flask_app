from flask import Flask
from flask import request, flash, get_flashed_messages
from flask import render_template, redirect, url_for
import json
import re

app = Flask(__name__)
app.secret_key = "secret_key"  # only debug!!


def get_base():
    with open('fake_base.json', "r") as data:
        return json.load(data)


def write_base(user):
    data = get_base()
    if len(data['users']) == 0:
        user['id'] = 0
    else:
        user['id'] = max(data['users'], key=lambda x: x['id'])['id'] + 1
    data['users'].append(user)
    with open('fake_base.json', "w") as file:

        json.dump(data, file)
    return True


def patch_base(user):
    data = get_base()
    for x in range(len(data['users'])):
        if data['users'][x]['id'] == user['id']:
            data['users'][x] = user
            break
    with open('fake_base.json', "w") as file:
        json.dump(data, file)
    return True


def delete_base(id):
    data = get_base()
    new_data = [x for x in data['users'] if x['id'] != id]
    data['users'] = new_data
    with open('fake_base.json', "w") as file:
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


def valide_patch(user):
    errors = {}
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    if re.match(pattern, user['email']) is None:
        errors['email'] = 'Invalid email'
    if user['nickname'].isdigit():
        errors['nickname'] = 'Invalid nickname'
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
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'users/index.html',
        users=user,
        search=name,
        messages=messages,
    )


@app.post('/users')
def creat_user():
    user = request.form.to_dict()
    errors = valide(user)
    if errors == {}:
        write_base(user)
        flash('User was added successfully', 'success')
        return redirect(url_for('get_users'))
    return render_template('users/users_form.html', user=user, errors=errors)


@app.get('/users/new')
def user_form():
    errors = {}
    user = {
        'nickname': '',
        'email': ''
    }
    return render_template('users/users_form.html', user=user, errors=errors)


@app.get('/users/<int:id>')
def get_user_by_id(id):
    users = get_base()['users']
    user = next(filter(lambda x: x['id'] == id, users), None)
    if user is None:
        return 'Page not found', 404
    return render_template('users/show.html', user=user)


@app.get('/users/<int:id>/edit')
def get_form_edit(id):
    users = get_base()['users']
    user = next(filter(lambda x: x['id'] == id, users), None)
    errors = {}
    if user is None:
        return 'Page not found', 404
    return render_template('users/users_form_edit.html', user=user, errors=errors)


@app.post('/users/<int:id>/patch')
def patch_user(id):
    user = request.form.to_dict()
    user['id'] = id
    errors = valide_patch(user)
    if errors == {}:
        patch_base(user)
        flash('User was patch successfully', 'success')
        return redirect(url_for('get_users'))
    return render_template('users/users_form_edit.html', user=user, errors=errors)


@app.post('/users/<int:id>/delete')
def delete_user(id):
    delete_base(id)
    flash('User was delete successfully', 'success')
    return redirect(url_for('get_users'))
