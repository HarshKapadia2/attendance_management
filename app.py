from flask import Flask, render_template, url_for, request, redirect, session, flash
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
from init.init import init
from teacher.teacher import teacher
from student.student import student
from admin.admin import admin

app = Flask(__name__)

app.secret_key = '' # for flask session

# register blueprints (code splitting)
app.register_blueprint(init)
app.register_blueprint(teacher, url_prefix='/teacher')
app.register_blueprint(student, url_prefix='/student')
app.register_blueprint(admin, url_prefix='/admin')



@app.route('/', methods = ['GET'])
def home_page():
    if request.method == 'GET':
        return render_template('home-page.html')


if __name__ == '__main__':
    app.run(debug = True) # No parameters in production