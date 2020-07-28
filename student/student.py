from flask import Flask, render_template, url_for, request, redirect, session, flash, Blueprint
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

db = firestore.client()

# The web app's Firebase configuration
firebaseConfig = {
  'apiKey': "",
  'authDomain': "",
  'databaseURL': "",
  'projectId': "",
  'storageBucket': "",
  'messagingSenderId': "",
  'appId': "",
  'measurementId': ""
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

student = Blueprint('student', __name__, static_folder='static', template_folder='templates')



@student.route('/login', methods=['GET'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

@student.route('/signup', methods=['GET'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')

@student.route('/forgot_password', methods=['GET'])
def forgotPassword():
	if request.method == 'GET':
		return render_template('forgot-password.html')

@student.route('/dashboard', methods=['GET'])
def dashboard():
  if request.method == 'GET':
    return render_template('dashboard.html')

@student.route('/lectures', methods=['GET'])
def lectures():
  if request.method == 'GET':
    return render_template('lectures.html')

@student.route('/practicals', methods=['GET'])
def practicals():
  if request.method == 'GET':
    return render_template('practicals.html')

@student.route('/lectures_and_practicals', methods=['GET'])
def lecturesAndPracticals():
  if request.method == 'GET':
    return render_template('lectures-and-practicals.html')