from flask import Blueprint
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

init = Blueprint('init', __name__)

# Use a service account
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)