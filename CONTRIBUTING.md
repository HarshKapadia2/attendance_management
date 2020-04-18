# Welcome, contributors! :smiley:

- Do not hesitate to raise an [issue](https://github.com/HarshKapadia2/attendance_management/issues) if you have any problems!

- **Beginner contributors** can find issues to be fixed under the `good first issue` label in the [issues](https://github.com/HarshKapadia2/attendance_management/issues) section.

- If you make a contribution, please do not forget to add your personal details to the [CONTRIBUTORS.md](https://github.com/HarshKapadia2/attendance_management/blob/master/CONTRIBUTORS.md) file!

## Requirements / Dependencies
- [Python 3](https://www.python.org/) (Enable/add Python to path)
- pip (comes bundled with Python 3)
- virtualenv (`pip install virtualenv`)
- Packages
   - `pip install flask firebase-admin pyrebase gunicorn` or `pip install -r requirements.txt`.
   - Refer to `requirements.txt` for more information on packages.
   - Run this command after creating a virtual environment.

## Local project setup
- Fork this repo.
- [`clone` it using Git (scroll down for the `git clone command`)](https://github.com/HarshKapadia2/git_basics#basic-git-commands).
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

---

### Further help
If any further help is needed, do contact me on [Twitter (@harshgkapadia)](https://twitter.com/harshgkapadia) or via e-mail `harshgkapadia@gmail.com`.
