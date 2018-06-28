### Create react app
npm install -g create-react-app

create-react-app my-app
cd my-app/
npm start

Success! Created frontend at /home/wsc-194a/workspace/OpenGameArt/opengameart/frontend
Inside that directory, you can run several commands:

  npm start
    Starts the development server.

  npm run build
    Bundles the app into static files for production.

  npm test
    Starts the test runner.

  npm run eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

We suggest that you begin by typing:

  cd frontend
  npm start

Happy hacking!

Note: the project was boostrapped with an old unsupported version of tools.
Please update to Node >=6 and npm >=3 to get supported tools in new projects.


### Install latest node

sudo npm install -g n
sudo n latest
## it's important to get the latest version of nodejs or at least 6<=
## and get the latest version of npm 

### Install and run django server

virtualenv venv
## OR
python3 -m venv venv

source venv/bin/activate
pip install -r requirements.txt

### pip add new packages
pip freeze --all > requirements.txt

python manage.py migrate
python manage.py runserver 127.0.0.1:8000


### Create django app
django-admin startproject todo_api .
python manage.py startapp todos

##AFTER
./manage.py makemigrations
./manage.py showmigrations
./manage.py migrate


### Create super user
python manage.py createsuperuser

Admin:
login: vereline
pass: victoria1234

User:
Test_user
testpassword

### Django shell
python manage.py shell


### Run test
1. Come into the directory with tests
2. ./manage.py test

### Collect static files
./manage.py collectstaticfiles

### Custom sql queries
https://docs.djangoproject.com/en/2.0/topics/db/sql/



### Test authentication
http://127.0.0.1:8000
http://127.0.0.1:8000/api/auth/token/obtain/ -- check here by entering existing account

http://127.0.0.1:8000/api/echo -- echo message to check authentication
Content: {"message" : "kek"}



