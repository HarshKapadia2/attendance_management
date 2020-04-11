# ***Attendance Management***
<p align="center">
   <a href="https://attendance-management-flask.herokuapp.com/"><b>https://attendance-management-flask.herokuapp.com/</b></a>
   <br />
   <br />
   <a href="#contributing"><img alt="Contributions Welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen?style=flat-square"></a>
   <img alt="Git MIT license" src="https://img.shields.io/github/license/HarshKapadia2/git_basics?style=flat-square">
   <br />
   <br />
   <b>A web app for teachers and students.</b>
</p>

## ***Functionalities***
- Teacher's functionalities
   - Give attendance to all students as per entered date.
   - On the dashboard, see the number of lectures conducted (by the teacher) and all students in the division in a table with their
      - Roll number
      - Name
      - Attendance percentage
      - Number of lectures attended by the student
      - Dates on which the student attended and didn't attend the lectures
- Student's functionalities
   - View attendance for all the teachers in the division in a table with the
      - Teacher's subject
      - Teacher's name
      - Number of lectures attended by the student
      - Number of lectures conducted by the teacher
      - Attendance percentage
      
## ***Technologies Used***
- Back end
   - Flask
- DB and Auth
   - Firebase
      - Cloud Firestore
      - e-mail-password authentication
- Front end
   - Templates from [Creative Tim](https://www.creative-tim.com/) Material Kit PRO - v2.2.0
      - HTML
      - CSS
      - JS

## ***Requirements***
- [Python 3](https://www.python.org/) (Enable/add Python to path)
- pip (comes bundled with Python 3)
- virtualenv (`pip install virtualenv`)
- Packages
   - `pip install flask firebase-admin pyrebase gunicorn` or `pip install -r requirements.txt`.
   - Refer to `requirements.txt` for more information on packages.
   - Run this command after creating a virtual environment.
   
## ***Run Instructions***
- Download the above code base ([or `clone` it using Git](https://github.com/HarshKapadia2/git_basics#basic-git-commands)).
- Create a virtual environment using `virtualenv <environment_name>`.
- [Activate the virtual environment (scroll down for different terminals)](https://docs.python.org/3/library/venv.html#creating-virtual-environments) & keep it activated whenever you're working on/using this project.
- Run `pip install flask firebase-admin pyrebase gunicorn` or `pip install -r requirements.txt`.
- Create a new project in your [Firebase console](https://console.firebase.google.com/).
- Add the config snippet from the project in the Firebase console to `app.py` and `templates/base.html`.
   - Register the web app in the project to get this snippet.
- Add the key snippet from the project in theFirebase console to `key.json`.
   - The key snippet is the generated private key file of the `Python` Firebase Admin SDK found in `Project Settings/Service Accounts`.
- Add a random string to `app.secret_key` variable at the start of the `app.py` file.
- Enable Cloud Firestore and e-mail-password auth for the project in Firebase.
- To run the website: `python app.py`.
- To view running website: default: `localhost:5000` or `127.0.0.1:5000`

## ***Creators***
- Harsh Kapadia
   - [LinkedIn](https://www.linkedin.com/in/harsh-kapadia-426999175/)
   - [Twitter](https://twitter.com/harshgkapadia)
- Saikiran Jakkan
   - [LinkedIn](https://www.linkedin.com/in/saikiran-jakkan-939b2a190/)
