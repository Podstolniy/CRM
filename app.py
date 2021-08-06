from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, current_user, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'iTs_very/ver*secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:111@localhost/domclick'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'


# for_Statuses
class Statuses(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Statuses %r>' % self.id


# for_Application_tips
class Tips(db.Model):
    __tablename__ = 'tips'
    id = db.Column(db.Integer, primary_key=True)
    tips = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return '<Tips %r>' % self.id


# for_Application_Department
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    otd = db.Column(db.String(40), nullable=False, unique=True)
    #pr = db.relationship('Peer', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department %r>' % self.otd


# for_applications
class Aplicat(db.Model):
    __tablename__ = 'aplicat'
    id = db.Column(db.Integer, primary_key=True)
    tips_aplic = db.Column(db.String(40), nullable=False, default='Not')  # fk
    description = db.Column(db.String(400), nullable=False, default='Not')
    contacts = db.Column(db.String(100), nullable=False, default='Not')
    com_works = db.Column(db.String(400), nullable=False, default='Not')
    lf_worker = db.Column(db.String(40), nullable=False, default='Not')  # fk
    status_work = db.Column(db.String(20), nullable=False, default='Not')  # fk
    data_complit = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Aplicat %r>' % self.id


# for_Application_register
class Register(UserMixin, db.Model):
    __tablename__ = 'register'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    otd = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(300))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return Register.query.get(int(id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        user = Register.query.filter_by(name=name).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')

    return render_template('login.html')


@app.route('/register')
def regs():
    regis = Department.query.order_by(Department.otd).all()
    return render_template("register.html", regis=regis)


@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        otd = request.form['otd']
        password = request.form['password']
        user = Register(name=name, username=username, otd=otd)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/admin-otd')
@login_required
def admin_otd():
    return render_template("admin-otd.html")


@app.route('/create-tips')
def tips():
    tips = Tips.query.order_by(Tips.tips).all()
    return render_template("create-tips.html", tips=tips)


# for_upDate_create-tips
@app.route('/create-tips/<int:id>')
@login_required
def tips_detail(id):
    detail_tips = Tips.query.get(id)
    return render_template("tips_detail.html", detail_tips=detail_tips)


@app.route('/create-tips/<int:id>/del')
def tips_delete(id):
    tips_del = Tips.query.get_or_404(id)
    try:
        db.session.delete(tips_del)
        db.session.commit()
        return redirect('/create-tips')
    except:
        return "При удалении заявки аозникла ошибка!"


@app.route('/create-tips/<int:id>/update', methods=['POST', 'GET'])
@login_required
def tips_update(id):
    tips_up = Tips.query.get(id)
    if request.method == 'POST':
        tips_up.tips = request.form['tips']
        try:
            db.session.commit()
            return redirect('/create-tips')
        except:
            return "При добавлении данных возникла ошибка!"
    else:
        return render_template("/create-tips.html", tips_up=tips_up)


@app.route('/create-tips', methods=['POST', 'GET'])
@login_required
def create_tips():
    if request.method == 'POST':
        tips = request.form['tips']
        t = Tips(tips=tips)
        try:
            db.session.add(t)
            db.session.commit()
            return redirect('/create-tips')
        except:
            return "При добавлении данных возникла ошибка!"

    else:
        return render_template("create-tips.html")


@app.route('/create-statuses')
def status():
    status = Statuses.query.order_by(Statuses.status).all()
    return render_template("create-statuses.html", status=status)


# for_upDate_create-statuses
@app.route('/create-statuses/<int:id>')
@login_required
def statuses_detail(id):
    detail_statuses = Statuses.query.get(id)
    return render_template("statuses_detail.html", detail_statuses=detail_statuses)


@app.route('/create-statuses/<int:id>/del')
def statuses_delete(id):
    statuses_del = Statuses.query.get_or_404(id)
    try:
        db.session.delete(statuses_del)
        db.session.commit()
        return redirect('/create-statuses')
    except:
        return "При удалении заявки аозникла ошибка!"


@app.route('/create-statuses/<int:id>/update', methods=['POST', 'GET'])
@login_required
def statuses_update(id):
    statuses_up = Statuses.query.get(id)
    if request.method == 'POST':
        statuses_up.status = request.form['statuses']
        try:
            db.session.commit()
            return redirect('/create-statuses')
        except:
            return "При добавлении данных возникла ошибка!"
    else:
        return render_template("create-statuses.html", statuses_up=statuses_up)


@app.route('/create-statuses', methods=['POST', 'GET'])
@login_required
def create_statuses():
    if request.method == 'POST':
        status = request.form['statuses']
        s = Statuses(status=status)
        try:
            db.session.add(s)
            db.session.commit()
            return redirect('/create-statuses')
        except:
            return "При добавлении данных возникла ошибка!"

    else:
        return render_template("create-statuses.html")


@app.route('/create-otd')
def department():
    otds = Department.query.order_by(Department.otd).all()
    return render_template("create-otd.html", otds=otds)


# for_upDate_create-otd
@app.route('/create-otd/<int:id>')
@login_required
def otd_detail(id):
    detail_otd = Department.query.get(id)
    return render_template("department_detail.html", detail_otd=detail_otd)


@app.route('/create-otd/<int:id>/del')
def otd_delete(id):
    detail_del = Department.query.get_or_404(id)
    try:
        db.session.delete(detail_del)
        db.session.commit()
        return redirect('/create-otd')
    except:
        return "При удалении заявки аозникла ошибка!"


@app.route('/create-otd/<int:id>/update', methods=['POST', 'GET'])
@login_required
def otd_update(id):
    otd_up = Department.query.get(id)
    if request.method == 'POST':
        otd_up.otd = request.form['otd']
        try:
            db.session.commit()
            return redirect('/create-otd')
        except:
            return "При добавлении данных возникла ошибка!"
    else:
        return render_template("create-otd.html", otd_up=otd_up)


@app.route('/create-otd', methods=['POST', 'GET'])
@login_required
def create_department():
    if request.method == 'POST':
        otd = request.form['otd']
        o = Department(otd=otd)
        try:
            db.session.add(o)
            db.session.commit()
            return redirect('/create-otd')
        except:
            return "При добавлении данных возникла ошибка!"

    else:
        return render_template("create-otd.html")


#  for_Aplications_
@app.route('/create-application')
def tips_up():
    tips_re = Tips.query.order_by(Tips.tips).all()
    return render_template("create-application.html", tips_re=tips_re)


@app.route('/create-application', methods=['POST', 'GET'])
def create_tips_up():
    if request.method == 'POST':
        tips_aplic = request.form['tips_aplic']
        description = request.form['description']
        contacts = request.form['contacts']
        se = Aplicat(tips_aplic=tips_aplic, description=description, contacts=contacts)
        try:
            db.session.add(se)
            db.session.commit()
            return redirect('/applications')
        except:
            return "При создании заявки возникла ошибка!"
    else:
        return render_template("create-application.html")


@app.route('/applications')
@login_required
def applications():
    applicates_all = Aplicat.query.all()
    return render_template("applications.html", applicates_all=applicates_all)


#  for_applications_details
@app.route('/applications/<int:id>')
@login_required
def application_detail(id):
    application_detail = Aplicat.query.get(id)
    return render_template("application_detail.html", application_detail=application_detail)


# for_upDate_application
@app.route('/applications/<int:id>/del')
def application_delete(id):
    application_del = Aplicat.query.get_or_404(id)
    try:
        db.session.delete(application_del)
        db.session.commit()
        return redirect('/applications')
    except:
        return "При удалении заявки возникла ошибка!"


@app.route('/applications/<int:id>/update')
@login_required
def status_app(id):
    statuses_app = Statuses.query.all()
    return render_template("applications_update.html", statuses_app=statuses_app)


@app.route('/applications/<int:id>/update', methods=['POST', 'GET'])
@login_required
def applications_update(id):
    app_up = Aplicat.query.get(id)
    if request.method == 'POST':
        app_up.com_works = request.form['com_works']
        app_up.lf_worker = request.form['lf_worker']
        app_up.status_work = request.form['status_work']
        try:
            db.session.commit()
            return redirect('/applications')
        except:
            return "При добавлении данных возникла ошибка!"
    else:
        return render_template("applications_update.html", app_up=app_up)


# for_filters_all
@app.route('/applications_close')
def applications_close():
    aplic_close = Aplicat.query.filter_by(status_work="Закрыта").all()
    return render_template("applications_close.html", aplic_close=aplic_close)


# for_filters_all
@app.route('/applications_open')
def applications_open():
    aplic_open = Aplicat.query.filter_by(status_work="Открыта").all()
    return render_template("applications_open.html", aplic_open=aplic_open)


# for_filters_all
@app.route('/applications_in_works')
def applications_in_works():
    aplic_in_works = Aplicat.query.filter_by(status_work="В работе").all()
    return render_template("applications_in_works.html", aplic_in_works=aplic_in_works)


if __name__ == "__main__":
    app.run(debug=True)

