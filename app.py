from flask import Flask 
from flask import render_template 
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy

from models.DBase import connection 

app = Flask(__name__)
Bootstrap(app)


# Custom class imports
from models.objects import User, Base
from models.Connection import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'url'
db = SQLAlchemy(app)



@app.route('/')
def index():
    return render_template('index.html')
