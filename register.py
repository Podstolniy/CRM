from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'iTs_very/ver*secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:111@localhost/domclick'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


def set_password(self, password):
    self.password_hash = generate_password_hash(password)


def create_peer():
    reg = Register()
    reg.name = 'admin'
    reg.username = 'admin'
    reg.otd = ' '
    reg.password_hash = '111'

    reg.set_password(reg.password_hash)
    db.session.add(reg)
    db.session.commit()

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


if __name__ == "__main__":
    create_peer()

