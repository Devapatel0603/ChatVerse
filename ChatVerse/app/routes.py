from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt, mail, oauth
from app.models import Users
from app.form import RegistrationForm, LoginForm, ForgotEmailForm, NewPasswordForm, MessageForm
from flask_login import login_user, current_user, logout_user, login_required
from bardapi import SESSION_HEADERS, Bard, BardCookies
from random import randint
from flask_mail import Message


cookie_dict = {
    "__Secure-1PSID": "dwiSAnJPsk7GpAVJfDFx8ZYR8pdiz6XFdcECmWCDhnd8RA2D2WqyKiUJI2O38Wml6FfsxA.",
    "__Secure-1PSIDTS": "sidts-CjEBPVxjSgL7OmpJWXE6xrBRSnCohtVW2gQIw1EJcmLwnHq2ostfqSjYXoqMTkgh7r-IEAA",
    "__Secure-1PSIDCC": "ABTWhQE8a3pG2OlzXYbDLMSUo4K0tu_sBGtpqbSqeibpGjvSc6yJTbE_uqjpxLv-2z6s7zea4ck"
}



bard = BardCookies(cookie_dict=cookie_dict)

def get_response(prompt):
    response = bard.get_answer(prompt)['content']
    return response


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/register', methods = ['GET', 'POST'])
def register():
    # if user is already logged in than we need to deactivate login link
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()

    #To take user details from register page if it is valid
    if request.method == 'POST' and form.validate_on_submit():
        global username
        username = request.form.get('username')
        global email
        email = request.form.get('email')
        global password
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')         

        global otp
        otp = randint(100000,999999)
        msg = Message("Email Verification", sender='devapatel0603@outlook.com', recipients=[email])
        msg.body = f"Hello {username}, \nWelcome to ChatVerse Your OTP is {str(otp)}"
        mail.send(msg)

        return redirect(url_for('email_verify'))
    return render_template("register.html", form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    # if user is already logged in than we need to deactivate register link
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        # get that user's data from database
        user = Users.query.filter_by(email=form.email.data).first()

        # check if user's password is equal to the database password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)

            # if next page exist like user want to access account page than he must first login
            # so after lgin user can direct see account page instead of home page
            next_page = request.args.get('next')

            flash("You have been logged in")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Please enter valid email or password.")
            return redirect(url_for('login'))
        
    return render_template("login.html", form=form)


    
@app.route('/email_verify', methods = ['GET', 'POST'])
def email_verify():
    if request.method == 'POST':
        user_otp = request.form.get('oth')
        if str(user_otp) == str(otp):
            entry = Users(username=username, email=email, password=password)
            db.session.add(entry)
            db.session.commit()
            flash(f'{username} Account created successfully!')
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP, please enter valid OTP.')
            return redirect(url_for('email_verify'))
            # return redirect(url_for('register'))
    return render_template("email_verify.html")


@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = MessageForm()
    return render_template("contact.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/clone', methods = ['GET', 'POST'])
@login_required
def clone():
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = get_response(prompt)
        return render_template("clone.html", prompt=prompt, response=response)
    else:
        return render_template("clone.html")


@app.route('/forgot_email_verify', methods = ['GET', 'POST'])
def forgot_email_verify():
    if request.method == 'POST':
        user_otp = request.form.get('oth2')
        if str(user_otp) == str(otp2): 
            return redirect(url_for('new_pass'))
        else:
            flash('Invalid OTP, please enter valid OTP.')
            return redirect(url_for('forgot_email_verify'))
            # return redirect(url_for('login'))
    return render_template("forgot_email_verify.html")


@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    form = ForgotEmailForm()
    if request.method == 'POST' and form.validate_on_submit():
        global emails
        emails = request.form.get('email')
        user = Users.query.filter_by(email=emails).first()
        if user:
            global otp2
            otp2 = randint(100000,999999)
            msg = Message("Email Verification", sender='devapatel0603@outlook.com', recipients=[emails])
            msg.body = f"Hello, \nWelcome to ChatVerse Your OTP is {str(otp2)}"
            mail.send(msg)
            return redirect(url_for('forgot_email_verify'))
        else:
            flash('Your email is not register, so please register yourself first')
            return redirect(url_for('register'))

    return render_template("forgot.html", form=form)


@app.route('/new_pass', methods = ['GET', 'POST'])
def new_pass():
    form = NewPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        update_password = Users.query.filter_by(email=emails).first()
        update_password.password = new_password
        db.session.commit()
        flash('New Password has been set successfully! Please login now')
        return redirect(url_for('login'))
    return render_template("new_pass.html",form=form)