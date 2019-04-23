from datetime import datetime
import pyrebase
from flask import Flask, render_template, url_for, flash, redirect

from forms import RegistrationForm, LoginForm, Reset, Grades

app = Flask(__name__)
app.config['SECRET_KEY'] = '3009a067019ca7c004d7e5a0133431ac'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(20),unique=True,nullable=False)
#     email = db.Column(db.String(120),unique=True,nullable=False)
#     password = db.Column(db.String(60),nullable=False,)
#     image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
#     posts = db.relationship('Post', backref='author',lazy = True)
#
#     def __repr__(self):
#         return f"user('{self.username}','{self.email}','{self.image_file}')"
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text,nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#
#     def __repr__(self):
#         return f"Post('{self.title}','{self.date_posted}')"


config = {
    "apiKey": "AIzaSyCRzd6sn8VdyBdl5adv1qHlsVtdZRfTm14",
    "authDomain": "botfirebaseproject-37c64.firebaseapp.com",
    "databaseURL": "https://botfirebaseproject-37c64.firebaseio.com",
    "projectId": "botfirebaseproject-37c64",
    "storageBucket": "botfirebaseproject-37c64.appspot.com",
    "messagingSenderId": "641101491410"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
#
# posts = [
#     {'author': "Koushik Deb",
#      'title' : "Blog Post 1",
#      'content': "First post content",
#      'date_posted': "April 20,2018"
#     },
#     {'author': "Mobin",
#      'title' : "Blog Post 2",
#      'content': "First post content",
#      'date_posted': "April 20,2018"
#     }
# ]
@app.route('/')
def startpage():
    return render_template('startpage.html',auth=auth)

@app.route('/home')
def home():
    # if auth.current_user is None:
    #     flash(f'You have to login first!!!','info')
    #     print("whaaaaaaaa")
    #     return redirect(url_for('login'))
    # else:
    return render_template("home.html", auth=auth)
@app.route('/about')
def about():
    if auth.current_user is None:
        flash(f'You have to login first!!!','info')
        print("whaaaaaaaa")
        return redirect(url_for('login'))
    else:
        return render_template('about.html', title = 'Damn',auth=auth)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!!','success')
        email = form.email.data
        password = form.password.data
        auth.create_user_with_email_and_password(email, password)
        #auth.get_account_info(['idToken'])
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form=form,auth=auth)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            auth.sign_in_with_email_and_password(email,password)
            flash(f'You have been logged in!!','success')
            return redirect(url_for('home'))
        except:
            flash(f'Log In unsuccessful!!','danger')
    return render_template('login.html', title = 'Login', form=form,auth=auth)

@app.route('/passwordreset', methods=['GET','POST'])
def passwordreset():
    form = Reset()
    if form.validate_on_submit():
        email = form.email.data
        auth.send_password_reset_email(email)
        return redirect('login')
    return render_template('ResetPassword.html',title = 'Reset Password',form=form,auth=auth)


@app.route('/link',methods=['GET','POST'])
def link():
    return render_template('link.html', title = 'Link',auth=auth)


@app.route('/grades',methods=['GET','POST'])
def grades():
    if auth.current_user is None:
        flash(f'You have to login first!!!', 'info')
        print("whaaaaaaaa")
        return redirect(url_for('login'))
    else:
        form = Grades()
        if form.validate_on_submit():
            du = 'No'
            ju = []
            bangla = form.bangla.data
            english = form.english.data
            math = form.math.data
            physics = form.physics.data
            chemistry = form.chemistry.data
            biology = form.biology.data
            ssc = form.ssc.data
            hsc = form.hsc.data
            total = ssc + hsc
            if ssc >= 3.5 and hsc >= 3.5:
                if total >= 8.0:
                    du = 'Yes'
            if total >= 7.5:
                ju.append('A')
            if total >= 8.0:
                ju.append('D')

                if physics >= 4.75 and math >= 4.75:
                    ju.append('H')
            if not ju:
                ju.append('No')
            return render_template('result.html', du=du, ju=ju,auth=auth)

    return render_template('grades.html', title = 'Grades', form=form,auth=auth)

@app.route('/index')
def index():
    if auth.current_user is None:
        flash(f'You have to login first!!!','info')
        print("whaaaaaaaa")
        return redirect(url_for('login'))
    else:
        return render_template('index.html',auth=auth)

@app.route('/logout')
def logout():
    auth.current_user = None
    return render_template('startpage.html')
if __name__ == '__main__':
    app.run(debug = True)
