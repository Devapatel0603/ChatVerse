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
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/chatgpt"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # similar to url_for

#To send OTP
app.config["MAIL_SERVER"] = 'smtp.office365.com'
app.config["MAIL_PORT"] = '587'
app.config["MAIL_USERNAME"] = 'devapatel0603@outlook.com'
app.config["MAIL_PASSWORD"] = 'Devq@0603'
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail()
mail.init_app(app)

#For Google login
app.config["OAUTH2_CLIENT_ID"] = '736503430115-o5jv69g6t3col537fptrv51jno67a44s.apps.googleusercontent.com'
app.config["OAUTH2_CLIENT_SECRET"] = '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'
app.config["OAUTH2_META_URL"] = 'https://accounts.google.com/.well-known/openid-configuration'
appconf = {
    "OAUTH2_CLIENT_ID" : '736503430115-o5jv69g6t3col537fptrv51jno67a44s.apps.googleusercontent.com',
    "OAUTH2_CLIENT_SECRET" : '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',
    "OAUTH2_META_URL" : 'https://accounts.google.com/.well-known/openid-configuration'
}
oauth = OAuth(app)
oauth.register("ChatVerse",
               client_id = appconf.get("OAUTH2_CLIENT_ID"),
               client_server = appconf.get("OAUTH2_CLIENT_SECRET"),
               server_metadata_url = appconf.get("OAUTH2_META_URL"),
               client_kwargs = {
                   "scope" : "openid profile email"
               }
               )


from app import routes