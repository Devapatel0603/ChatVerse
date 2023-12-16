from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from authlib.integrations.flask_client import OAuth

local_server = True
app = Flask(__name__)
app.config['SECRET_KEY'] = '63dde047970e7b76e653'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:yWr4pYx6Mzju@ep-dry-bread-81783153.us-east-1.postgres.vercel-storage.com:5432/verceldb"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # similar to url_for

#To send OTP
app.config["MAIL_SERVER"] = 'smtp.office365.com'
app.config["MAIL_PORT"] = '587'
app.config["MAIL_USERNAME"] = 'chatverse@outlook.com'
app.config["MAIL_PASSWORD"] = 'Devq@0603'
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail()
mail.init_app(app)

import routes