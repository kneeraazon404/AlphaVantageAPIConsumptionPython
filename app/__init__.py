from flask import Flask, session
from flask_session import Session
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('app.config.Config')
Session(app)
lm = LoginManager(app)
lm.login_view = 'login'

from app import routes

app.run(debug=True)