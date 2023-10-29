from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def index():
    return 'hi'


@app.get('/users')
def users_get():
    return 'GET /users'


@app.post('/users')
def users_post():
    return 'Users', 302

@app.get('/courses/<id>')
def courses(id):
    return 'Course id: {}'.format(id)
