"""
app setup prtio.com.
"""


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from flask.ext.login import LoginManager

app = Flask(__name__)
app.debug = True
# app.debug = os.getenv["DEBUG"] in ('True', 'true')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'splash.home'

# for flaskext.auth -- secret key needed to use sessions
# app.secret_key = os.environ['USER_AUTH_SECRET_KEY']
