from flask import Flask


UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set('*.doc','*.png','*.jpeg','*.pdf')

app = Flask(__name__)
app.config.from_object('config')