from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///curso_flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '345j3n5ltlknlknl345345345mnhcgf'

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from estudo.view import homepage
from estudo.models import Contatos