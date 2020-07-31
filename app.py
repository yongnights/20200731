from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
from models import User
from forms import LoginForm, RegistrationForm
import config

app = Flask(__name__)
app.secret_key = "flask rocks!"
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()
