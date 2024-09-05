from app.config import app, db, login_manager
from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц при первом запуске

    from app.handlers import home
    from app.handlers import auth
    from app.handlers import ad

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(ad.bp)
    app.run(debug=True)
