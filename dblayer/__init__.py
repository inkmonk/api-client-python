from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

__version__ = '1.0'

app = Flask(__name__)
app.config.from_object('dblayer.config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.DB_USERNAME + ':' + config.DB_PASSWORD + '@' + config.DB_SERVER + '/' + config.DB_NAME
db = SQLAlchemy(app)
