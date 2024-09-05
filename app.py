import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на свой секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)



class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Связь с пользователем




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка на существующего пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.', 'danger')
            return redirect(url_for('register'))

        # Хеширование пароля
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверные учетные данные. Пожалуйста, попробуйте снова.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    ads = Ad.query.all()  # Извлекаем все объявления из базы данных
    return render_template('index.html', ads=ads)

UPLOAD_FOLDER = 'static/uploads'  # Папка для сохранения загруженных изображений
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/add_ad', methods=['GET', 'POST'])
@login_required
def add_ad():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        # Сохранение изображения на сервере
        image_filename = None
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        new_ad = Ad(title=title, description=description, image_filename=image_filename, user_id=current_user.id)  # Сохраняем пользователя
        db.session.add(new_ad)
        db.session.commit()

        flash('Объявление успешно добавлено!', 'success')
        return redirect(url_for('index'))

    return render_template('add_ad.html')



@app.route('/edit_ad/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)

    # Проверка, что текущий пользователь является создателем объявления
    if ad.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого объявления.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        # Сохранение изображения на сервере
        image_filename = ad.image_filename  # Оставляем текущее, если новое не загружено
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        ad.title = title
        ad.description = description
        ad.image_filename = image_filename

        db.session.commit()
        flash('Объявление успешно обновлено!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_ad.html', ad=ad)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц при первом запуске
    app.run(debug=False)
    