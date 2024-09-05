from flask import Blueprint, render_template

from app.models import Ad

bp = Blueprint("home", __name__)


@bp.route("/", methods=["GET"])
def index():
    ads = Ad.query.all()  # Извлекаем все объявления из базы данных
    return render_template("index.html", ads=ads)
