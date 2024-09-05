import os
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required

from app.config import app, db
from app.models import Ad

bp = Blueprint("ad", __name__, url_prefix="/ad")


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_ad():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.files["image"]

        # Сохранение изображения на сервере
        image_filename = None
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

        new_ad = Ad(title=title, description=description, image_filename=image_filename)
        db.session.add(new_ad)
        db.session.commit()

        flash("Объявление успешно добавлено!", "success")
        return redirect(url_for("home.index"))

    return render_template("add_ad.html")


@bp.route("/edit/<int:ad_id>", methods=["GET", "POST"])
@login_required
def edit_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.files["image"]

        # Сохранение изображения на сервере
        image_filename = ad.image_filename  # Оставляем текущее, если новое не загружено
        if image:
            image_filename = image.filename
            image.save(app.config["UPLOAD_FOLDER"] / image_filename)

        ad.title = title
        ad.description = description
        ad.image_filename = image_filename

        db.session.commit()
        flash("Объявление успешно обновлено!", "success")
        return redirect(url_for("home.index"))

    return render_template("edit_ad.html", ad=ad)
