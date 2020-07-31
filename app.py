from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from exts import db
from models import User, Receipes, Contributors
from forms import LoginForm, RegistrationForm, ReceipesForm
from werkzeug.utils import secure_filename
import config
import os
import datetime

app = Flask(__name__)
app.secret_key = "flask rocks!"
app.config.from_object(config)
db.init_app(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])


def to_json(all_vendors):
    v = [ven.dobule_to_dict() for ven in all_vendors]
    return v


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # if request.method == "POST":
    #     return redirect(url_for('search_results'))
    return render_template('search.html')


@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html')


@app.route('/create')
def create():
    req = request.args
    id = int(req.get("id", 0))
    if id != 0:
        receipes_get = Receipes.query.filter_by(id=id).first()

        content = {
            'id': receipes_get.id,
            'title': receipes_get.title,
            'type': receipes_get.type,
            'ingredients': receipes_get.ingredients,
            'content': receipes_get.content,
        }
        return render_template('create.html', **content)
    return render_template('create.html')


@app.route('/create_save', methods=['GET', 'POST'])
def create_save():
    if request.method == "POST":
        id = request.form['id']
        if id:
            receipes_edit = Receipes.query.filter_by(id=id).first()
            receipes = ReceipesForm(request.form)
            receipes_edit.title = receipes.title.data
            receipes_edit.type = receipes.type.data
            receipes_edit.ingredients = receipes.ingredients.data
            receipes_edit.content = receipes.content.data
            receipes_edit.release_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            f = request.files['file']
            if not (f and allowed_file(f.filename)):
                return jsonify(
                    {"error": 1001, "msg": "Please check the type of image uploaded, only for png、PNG、jpg、JPG、bmp"})

            basepath = os.path.dirname(__file__)

            upload_path = os.path.join(basepath, 'static/pictures', secure_filename(f.filename))
            f.save(upload_path)

            receipes_edit.images = f.filename
            # db.session.update(receipes_edit)
            db.session.commit()

            return redirect(url_for('account'))
        else:
            receipes = ReceipesForm(request.form)
            title = receipes.title.data
            type = receipes.type.data
            ingredients = receipes.ingredients.data
            content = receipes.content.data
            release_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            f = request.files['file']
            if not (f and allowed_file(f.filename)):
                return jsonify(
                    {"error": 1001, "msg": "Please check the type of image uploaded, only for png、PNG、jpg、JPG、bmp"})

            basepath = os.path.dirname(__file__)

            upload_path = os.path.join(basepath, 'static/pictures', secure_filename(f.filename))
            f.save(upload_path)

            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            receipes_add = Receipes(title=title, type=type, ingredients=ingredients, content=content,
                                    release_date=release_date, images=f.filename, contributor_id=user.id,
                                    contributor_name=user.username)

            db.session.add(receipes_add)
            db.session.commit()

            return redirect(url_for('account'))

    return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm(request.form)
    if request.method == "POST":
        username = login.username.data
        password = login.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if username and password and email:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    receipes_query = Receipes.query.filter_by(contributor_id=user.id)
    receipes_num = receipes_query.count()
    data = to_json(receipes_query.all())
    # print(data)

    content = {
        'username': user.username,
        'email': user.email,
        'receipes_num': receipes_num,
        'list': data
    }

    return render_template('account.html', **content)


@app.route('/account_delete')
def account_delete():
    req = request.args
    id = int(req.get("id", 0))
    receipes = Receipes.query.filter_by(id=id).first()
    db.session.delete(receipes)
    db.session.commit()
    return redirect(url_for('account'))


if __name__ == '__main__':
    app.run()
