# Welcome, contributors! :smiley:

- Please be mindful of the [code of conduct](CODE_OF_CONDUCT.md) while interacting or contributing!

- Do not hesitate to raise an [issue](https://github.com/HarshKapadia2/attendance_management/issues) if you have any problems!

- **Beginner contributors** can find issues to be fixed under the `good first issue` label in the [issues](https://github.com/HarshKapadia2/attendance_management/issues) section.

- If you make a contribution, please do not forget to add your personal details to the [CONTRIBUTORS.md](CONTRIBUTORS.md) file!

## Requirements / Dependencies
- [Python 3](https://www.python.org/) (Enable/add Python to path)
- pip (comes bundled with Python 3)
- virtualenv (`pip install virtualenv`)
- Packages
   - `pip install flask firebase-admin pyrebase gunicorn` or `pip install -r requirements.txt`.
   - Refer to `requirements.txt` for more information on packages.
   - Run this command after creating a virtual environment.

## Project dev instructions
- Fork this repo.
- [`clone` your forked repo using Git.](https://harshkapadia2.github.io/git_basics/#_git_clone)
- [Activate the virtual environment (scroll down for different terminals)](https://docs.python.org/3/library/venv.html#creating-virtual-environments) & keep it activated whenever you're working on/using this project.
- Run `pip install flask firebase-admin pyrebase gunicorn` or `pip install -r requirements.txt`.
- Create a new project in your [Firebase console](https://console.firebase.google.com/).
- Register the web app in the Firebase console project to get the `Firebase config` snippet. Add this snippet to `./app.py` and `./static/js/firebaseConfig.js`.
- A `key` snippet has to be generated from the project settings
   - The key snippet is the generated private key file of the **Python** Firebase Admin SDK found in `Project Settings/Service Accounts`.
   - Add the key snippet from the Firebase console project to `./key.json`.
- Add a random string to the `app.secret_key` variable at the start of the `./app.py` file.
- Enable Cloud Firestore and e-mail-password auth for the project in Firebase.
- To run the website: `python app.py`.
- To view running website: default: `localhost:5000` or `127.0.0.1:5000` (will be mentioned in the terminal as well)
- Make your contribution to the code base!
- Add your personal details to the [CONTRIBUTORS.md](CONTRIBUTORS.md) file.
- Push the code to your forked repo.
   - **NOTE** 
      - Please do not commit and upload (push) `key.json`, `firebaseConfig.json` without erasing your personal data from them and please leave the `app.secret_key` blank before committing and pushing.
      - [Use the correct commit message structure](https://harshkapadia2.github.io/git_basics/#_git_commit) Eg: `:bug: fix: Remove typo (#0)`, which renders like this ':bug: fix: Remove typo (#0)'.
- Make a pull request (PR)!

---

### Further help
If any further help is needed, do contact me on [Twitter (@harshgkapadia)](https://twitter.com/harshgkapadia) or via e-mail `harshgkapadia@gmail.com`.
