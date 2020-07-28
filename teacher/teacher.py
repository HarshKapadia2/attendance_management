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

teacher = Blueprint('teacher', __name__, static_folder='static', template_folder='templates')



@teacher.route('/login', methods=['GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

@teacher.route('/signup', methods=['GET'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')

@teacher.route('/forgot_password', methods=['GET'])
def forgotPassword():
	if request.method == 'GET':
		return render_template('forgot-password.html')

@teacher.route('/class_dashboard', methods=['GET'])
def classDashboard():
  if request.method == 'GET':
    return render_template('class-dashboard.html')

@teacher.route('/division_dashboard', methods=['GET'])
def divisionDashboard():
  if request.method == 'GET':
    return render_template('division-dashboard.html')

@teacher.route('/defaulter_calculation', methods=['GET'])
def defaulterCalculation():
  if request.method == 'GET':
    return render_template('defaulter-calculation.html')

@teacher.route('/defaulter_list', methods=['GET'])
def defaulterList():
  if request.method == 'GET':
    return render_template('defaulter-list.html')

@teacher.route('/add_edit_lecture', methods=['GET'])
def add_editLecture():
  if request.method == 'GET':
    return render_template('add-edit-lecture.html')