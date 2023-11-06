from flask import Flask
from flask import request, flash, get_flashed_messages
from flask import render_template, redirect, url_for, make_response
import json
import re

app = Flask(__name__)
app.secret_key = "secret_key"  # only debug!!

DATA_BASE = 'users'

def get_id(users):
    if len(users) == 0:
        return 0
    else:
        return max(users, key=lambda x: x['id'])['id'] + 1


def valide(user):
    errors = {}
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    if re.match(pattern, user['email']) is None:
        errors['email'] = 'Invalid email'
    if user['nickname'].isdigit():
        errors['nickname'] = 'Invalid nickname'
    return errors


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/users')
def get_users():
    users = json.loads(request.cookies.get(DATA_BASE,  json.dumps([])))
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
        users = json.loads(request.cookies.get(DATA_BASE,  json.dumps([])))
        user['id'] = get_id(users)
        users.append(user)
        flash('User was added successfully', 'success')
        response = make_response(redirect(url_for('get_users')))
        response.set_cookie(DATA_BASE, json.dumps(users))
        return response
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
    users = json.loads(request.cookies.get(DATA_BASE, json.dumps([])))
    user = next(filter(lambda x: x['id'] == id, users), None)
    if user is None:
        return 'Page not found', 404
    return render_template('users/show.html', user=user)


@app.get('/users/<int:id>/edit')
def get_form_edit(id):
    users = json.loads(request.cookies.get(DATA_BASE, json.dumps([])))
    user = next(filter(lambda x: x['id'] == id, users), None)
    errors = {}
    if user is None:
        return 'Page not found', 404
    return render_template('users/users_form_edit.html', user=user, errors=errors)


@app.post('/users/<int:id>/patch')
def patch_user(id):
    user = request.form.to_dict()
    user['id'] = id
    errors = valide(user)
    if errors == {}:
        users = json.loads(request.cookies.get(DATA_BASE, json.dumps([])))
        for index, old_user in enumerate(users):
            if id == old_user['id']:
                users[index] = user
                break
        else:
            return 'Page not found', 404

        flash('User was patch successfully', 'success')
        response = make_response(redirect(url_for('get_users')))
        response.set_cookie(DATA_BASE, json.dumps(users))
        return response
    return render_template('users/users_form_edit.html', user=user, errors=errors)


@app.post('/users/<int:id>/delete')
def delete_user(id):
    users = json.loads(request.cookies.get(DATA_BASE, json.dumps([])))
    print(users)
    new_users = [user for user in users if user['id'] != id]
    flash('User was delete successfully', 'success')
    response = make_response(redirect(url_for('get_users')))
    response.set_cookie(DATA_BASE, json.dumps(new_users))
    return response
