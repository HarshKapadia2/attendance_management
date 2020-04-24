from flask import Flask, render_template, url_for, request, redirect, session, flash
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

app = Flask(__name__)

app.secret_key = '' # for flask session


# Use a service account
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

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



@app.route('/', methods = ['GET'])
def home_page():
    if 'user' not in session:
        return render_template('home_page.html')
    else:
        return redirect('/logout')










@app.route('/teacher_login', methods = ['GET', 'POST'])
def teacher_login():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('teacher_login_page.html')
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
                div_details = div_ref.document(division).get().to_dict()
                # check for teacher existence in div
                for teacher_email in div_details['teacher_email']:
                    if teacher_email == email:
                        flag_2 = True
                        # check pass
                        try:
                            teacher_user = auth.sign_in_with_email_and_password(email, password)
                            # print(teacher_user) # get back details
                            flag_3 = True
                            # e-mail verification check
                            acc_info = auth.get_account_info(teacher_user['idToken'])
                            if acc_info['users'][0]['emailVerified'] == True:
                                flag_4 = True
                        except:
                            flag_3 = False
                        break
                break
        
        if flag_1 == False or flag_2 == False or flag_3 == False or flag_4 == False:
            flash('Incorrect, unverified or non-existent e-mail, division or password...', 'error')
            return redirect('/teacher_login')
    
        session['division'] = division
        session['user'] = email
        session['person_type'] = 'teacher'
        return redirect('/teacher_dashboard')



@app.route('/teacher_signup', methods = ['GET', 'POST'])
def teacher_signup():
    if request.method == 'GET':
        if 'user' not in session:
            return render_template('teacher_signup_page.html')
        else:
            return redirect('/logout')

    elif request.method == 'POST':
        name = request.form['name']
        division = request.form['division'].upper()
        sub = request.form['sub']
        year = request.form['year']
        sem = request.form['sem']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        # check if passwords match
        if password != password2:
            flash('The passwords do not match...', 'error')
            return redirect('/teacher_signup')
        # check length of pass
        if len(password) < 6:
            flash('The password has to be more than 5 characters long...', 'error')
            return redirect('/teacher_signup')
        
        # auth user
        try:
            teacher_user = auth.create_user_with_email_and_password(email, password)
        except:
            flash('This e-mail has already been registered. Please use another e-mail...', 'error')
            return redirect('/teacher_signup')
        # e-mail verification
        auth.send_email_verification(teacher_user['idToken'])
        # add teacher to db
        db.collection('teacher').document(email).set({
            'name': name,
            'division': division,
            'subject': sub,
            'year': year,
            'sem': sem,
            'password': password # firebase auth
        })
        # check for div
        db.collection('division').document(division).set({
            'year': year,
            'sem': sem
        }, merge = True)
        db.collection('division').document(division).update({
            'teacher_email': firestore.ArrayUnion([email])
        })

        flash('Registration successful! Please check your e-mail for verification and then log in...', 'info')
        return redirect('/teacher_login')



@app.route('/teacher_dashboard', methods = ['GET'])
def teacher_dashboard():
    if 'user' in session and session['person_type'] == 'teacher':
        # get teacher details
        teacher_details = db.collection('teacher').document(session['user']).get()
        # conducted lec count
        lectures = db.collection('teacher').document(session['user']).collection('lecture').stream()
        lec_conducted_count = 0
        for lecture in lectures:
            lec_conducted_count += 1
        # get all students & lecs
        student_ref = db.collection('division').document(session['division']).collection('student').order_by('roll_no')
        lecture_ref = db.collection('teacher').document(session['user']).collection('lecture').order_by('date')
        students = student_ref.stream()
        lectures = lecture_ref.stream()
        # attendance calculation logic
        attendance = {}
        for student in students:
            attended_bool = []
            lec_attended_count = 0
            for lecture in lectures:
                lec_dict = lecture.to_dict()
                if student.id in lec_dict['student_email']:
                    attended_bool.append(True)
                    lec_attended_count += 1
                else:
                    attended_bool.append(False)
            if lec_conducted_count != 0:
                percentage = int((lec_attended_count/lec_conducted_count)*100)
            else:
                percentage = 0
            attendance[student.id] = [lec_attended_count, percentage, attended_bool]
            lectures = lecture_ref.stream() # needs to be streamed again after every use, reason unkonwn

        students = student_ref.stream() # needs to be streamed again after every use, reason unkonwn
        lectures = lecture_ref.stream() # needs to be streamed again after every use, reason unkonwn
        return render_template('teacher_dashboard_page.html', teacher_details = teacher_details.to_dict(), lec_conducted_count = lec_conducted_count, attendance = attendance, students = students, lectures = lectures)
    else:
        return redirect('/logout')



@app.route('/add_edit_lecture', methods = ['GET', 'POST'])
def add_edit_lecture():
    if request.method == 'GET':
        if 'user' in session and session['person_type'] == 'teacher':
            # get teacher details
            teacher_details = db.collection('teacher').document(session['user']).get()
            # get students
            students = db.collection('division').document(session['division']).collection('student').order_by('roll_no').stream()
            count = 0
            for student in students:
                count += 1
            if count == 0:
                flash('No students in division to add lecture...', 'info')
                return redirect('/teacher_dashboard')
            
            students = db.collection('division').document(session['division']).collection('student').order_by('roll_no').stream()
            return render_template('add_edit_lecture_page.html', students = students, teacher_details = teacher_details.to_dict())
        else:
            return redirect('/logout')

    elif request.method == 'POST':
        # get date and attendance
        date = request.form['date']
        student_emails = request.form.getlist('check-box')
        # edit lecture functionality (delete prev doc)
        lectures = db.collection('teacher').document(session['user']).collection('lecture').stream()
        for lecture in lectures:
            lec_dict = lecture.to_dict()
            if date == lec_dict['date']:
                db.collection('teacher').document(session['user']).collection('lecture').document(lecture.id).delete()
                break
        
        lec_doc_ref = db.collection('teacher').document(session['user']).collection('lecture').document()
        lec_doc_ref.set({
            'date': date,
            'student_email': []
        })
        
        for student_email in student_emails:
            lec_doc_ref.update({
            'student_email': firestore.ArrayUnion([student_email])
            })

        flash('Lecture added/edited successfully...', 'info')
        return redirect('/teacher_dashboard')










@app.route('/student_login', methods = ['GET', 'POST'])
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
            return redirect('/student_login')

        session['division'] = division
        session['user'] = email
        session['person_type'] = 'student'
        return redirect('/student_dashboard')



@app.route('/student_signup', methods = ['GET', 'POST'])
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
                return redirect('/student_signup')
        # check if passwords match
        if password != password2:
            flash('The passwords do not match...', 'error')
            return redirect('/student_signup')
        # check length of pass
        if len(password) < 6:
            flash('The password has to be more than 6 characters long...', 'error')
            return redirect('/student_signup')

        # auth user
        try:
            st_user = auth.create_user_with_email_and_password(email, password)
        except:
            flash('This e-mail has already been registered. Please use another e-mail...', 'error')
            return redirect('/teacher_signup')
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
        return redirect('/student_login')



@app.route('/student_dashboard', methods = ['GET'])
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