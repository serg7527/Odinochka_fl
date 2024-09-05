from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = "your_secret_key"  # Замените на свой секретный ключ
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ads.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


BASE_DIR = Path(__file__).parent.parent.resolve()
UPLOAD_FOLDER = BASE_DIR / "static/uploads"  # Папка для сохранения загруженных изображений
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
