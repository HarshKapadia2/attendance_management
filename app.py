from flask import Flask, render_template, url_for, request, redirect, session, flash
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from init.init import init
from teacher.teacher import teacher
from student.student import student

app = Flask(__name__)

app.secret_key = '' # for flask session.

app.register_blueprint(init)
app.register_blueprint(teacher, url_prefix='/teacher')
app.register_blueprint(student, url_prefix='/student')


@app.route('/', methods = ['GET'])
def home_page():
    if 'user' not in session:
        return render_template('home-page.html')
    else:
        return redirect('/logout')


@app.route('/logout', methods = ['GET'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('person_type', None)
        session.pop('division', None)

        flash('You have been logged out...', 'warning')
        return redirect('/')
    else:
        return redirect('/')


@app.route('/forgot_password', methods = ['GET', 'POST'])
def forgotPassword():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('forgot_password_page.html')
        else:
            return redirect('/logout')
    elif request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
        except:
            flash('That e-mail ID is not registered...', 'error')
            return redirect('/')
        flash('Check your e-mail to set new password...', 'info')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)