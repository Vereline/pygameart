# PyGameArt!

## Installation

### React app

```sh
$ create-react-app my-app
$ cd my-app/
$ npm start
```
Inside that directory, you can run several commands:

  ```npm start```
    Starts the development server.

  ```npm run build```
    Bundles the app into static files for production.

  ```npm test```
    Starts the test runner.

  ```npm run eject```
    Removes this tool and copies build dependencies, configuration files and scripts into the app directory. If you do this, you can’t go back!

We suggest that you begin by typing:

  ```cd frontend```
  ```npm start```

Happy hacking!

Note: the project was boostrapped with an old unsupported version of tools.
Please update to Node >=6 and npm >=3 to get supported tools in new projects.

### Install latest version of code and libraries

```sh
sudo npm install -g n
sudo n latest
```
 It's important to get the latest version of nodejs or at least 6<= and get the latest version of npm 

## Install and run Django server

```sh
virtualenv venv
```
or
```sh
python3 -m venv venv
```
Then do:
```sh
source venv/bin/activate
pip install -r requirements.txt
```

### PIP: adding new packages
```
pip freeze --all > requirements.txt
```

### Making migrations and running server
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

### Create a new django app 
```sh
django-admin startproject the_whole_new_project
python manage.py startapp an_app_in_the_project
```

### Apply migrations
```sh
./manage.py makemigrations
./manage.py showmigrations
./manage.py migrate
```

### Create superuser
```sh
python manage.py createsuperuser
```

#### Admin:
login: vereline
pass: victoria1234

#### Users
User are registered as usual in the sign up view

User:Test_user
Pass:testpassword1

User:non_admin
Pass:12345678a

User:second_user
Pass:123second

User:user_to_delete
Pass:12345qwe

### Django shell
Aftre runing server:
```sh
python manage.py shell
```
Django debug toolbar:
```sh
python manage.py debugsqlshell
```

### Run tests
```sh
./manage.py test module_name
./manage.py test --help
./manage.py --verbosity=2
```

### Collect static files
```sh
./manage.py collectstaticfiles
```

[Custom sql queries](https://docs.djangoproject.com/en/2.0/topics/db/sql/)

### Test authentication with JWT-token
```sh
http://127.0.0.1:8000
http://127.0.0.1:8000/api/auth/token/obtain/ -- check here by entering existing account

http://127.0.0.1:8000/api/echo -- echo message to check authentication
Content: {"message" : "kek"}

```
