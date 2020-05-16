from flask import Flask, render_template, url_for, request, redirect, session, flash, Blueprint
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

db = firestore.client()

# pyrebase init
# Your web app's Firebase configuration

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
 

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

student = Blueprint('student', __name__, static_folder='../static', template_folder='templates')



@student.route('/login', methods = ['GET', 'POST'])
def student_login():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('student_login_page.html')
        else:
            return redirect('/logout')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        division = request.form['division'].upper()

        # check e-mail, div & pass
        flag_1 = flag_2 = flag_3 = flag_4 = False
        div_ref = db.collection('division')
        divs = div_ref.stream()
        # check for div existence
        for div in divs:
            if div.id == division:
                flag_1 = True
                div_student_details = div_ref.document(division).collection('student').stream()
                # check for student existence in div
                for student in div_student_details:
                    if student.id == email:
                        flag_2 = True
                        # check pass
                        try:
                            st_user = auth.sign_in_with_email_and_password(email, password)
                            flag_3 = True
                            # e-mail verification check
                            acc_info = auth.get_account_info(st_user['idToken'])
                            if acc_info['users'][0]['emailVerified'] == True:
                                flag_4 = True
                        except:
                            flag_3 = False
                        break
                break

        if flag_1 == False or flag_2 == False or flag_3 == False or flag_4 == False:
            flash('Incorrect, unverified or non-existent e-mail, division or password...', 'error')
            return redirect('/student/login')

        session['division'] = division
        session['user'] = email
        session['person_type'] = 'student'
        return redirect('/student/dashboard')



@student.route('/signup', methods = ['GET', 'POST'])
def student_signup():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('student_signup_page.html')
        else:
            return redirect('/logout')

    elif request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        division = request.form['division'].upper()
        year = request.form['year']
        sem = request.form['sem']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # check for same roll no.
        students = db.collection('division').document(division).collection('student').stream()
        for student in students:
            st_dict = student.to_dict()
            if st_dict['roll_no'] == roll_no:
                flash(f'Roll no. {roll_no} is already registered for {division}...', 'error')
                return redirect('/student/signup')
        # check if passwords match
        if password != password2:
            flash('The passwords do not match...', 'error')
            return redirect('/student/signup')
        # check length of pass
        if len(password) < 6:
            flash('The password has to be more than 6 characters long...', 'error')
            return redirect('/student/signup')

        # auth user
        try:
            st_user = auth.create_user_with_email_and_password(email, password)
        except:
            flash('This e-mail has already been registered. Please use another e-mail...', 'error')
            return redirect('/student/signup')
        # e-mail verification
        auth.send_email_verification(st_user['idToken'])
        # check for div
        db.collection('division').document(division).set({
            'year': year,
            'sem': sem,
        }, merge = True)
        # add student to db
        db.collection('division').document(division).collection('student').document(email).set({
            'name': name,
            'roll_no': roll_no,
        })
        
        flash('Registration successful! Please check your e-mail for verification and then log in...', 'info')
        return redirect('/student/login')



@student.route('/dashboard', methods = ['GET'])
def student_dashboard():
    if 'user' in session and session['person_type'] == 'student':
        # get student data
        div_ref = db.collection('division').document(session['division'])
        div_details = div_ref.get().to_dict()
        student_details = div_ref.collection('student').document(session['user']).get()
        attendance = {}
        if 'teacher_email' in div_details:
            # get subject data
            for teacher_email in div_details['teacher_email']:
                teacher_ref = db.collection('teacher').document(teacher_email)
                lec_ref = teacher_ref.collection('lecture')
                teacher_details = teacher_ref.get().to_dict()
                lectures = lec_ref.stream()
                # conducted lec count & attendance calculation logic
                lec_conducted_count = 0
                lec_attended_count = 0
                for lecture in lectures:
                    lec_conducted_count += 1
                    lec_dict = lecture.to_dict()
                    if session['user'] in lec_dict['student_email']:
                        lec_attended_count += 1
                    lectures = lec_ref.stream() # needs to be streamed again after every use, reason unkonwn
                
                if lec_conducted_count != 0:
                    percentage = int((lec_attended_count/lec_conducted_count)*100)
                else:
                    percentage = 0
                
                attendance[teacher_email] = [teacher_details['subject'], teacher_details['name'], lec_attended_count, lec_conducted_count, percentage]
                lectures = lec_ref.stream() # needs to be streamed again after every use, reason unkonwn
        
        div_details = div_ref.get().to_dict() # needs to be streamed again after every use, reason unkonwn
        return render_template('student_dashboard_page.html', student_details = student_details.to_dict(), div_details = div_details, division = session['division'], attendance = attendance)
    else:
        return redirect('/logout')