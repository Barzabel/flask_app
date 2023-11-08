start:
	poetry run flask --app flask_app/example --debug run --port 8000

start_unicorn:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 flask_app.example:app