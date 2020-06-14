from flask import Blueprint
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

init = Blueprint('init', __name__)

# Add the Firebase Python Admin SDK to interact with Firebase from privileged environments to perform actions
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)