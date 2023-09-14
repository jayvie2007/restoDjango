# RestoDjango

<h2> To run the system first install Python 3.10 </h2>
<p> Open your VS Code then open this folder <p>

do not clone the .env folder except the dev.env instead create a new virtual environment

<h3>Installing new virtual environment</h3>

```bash
  python -m venv .env
```

Then install the prequisite data

<h3>Installing the necessary files</h3>

```bash
  pip3 install -r .\requirements.txt
```

<h3>Activate the virtual environment</h3>

```bash
  .env\scripts\activate
```

<p> Make sure you are in the AuthDjango Folder </p>

<h3>change folder directory</h3>

```bash
  cd base
```

<p>After entering the base folder you may now run the server</p>

<p> in order to run the system first you must the data </p>

```bash
  python manage.py makemigrations
  python manage.py migrate
```

check settings.py 

comment the postgre database and uncomment the sql database
comment caches

<p>After migrating you may now run the server</p>

<h3>Running Localhost server</h3>

```
  python manage.py runserver
```

<h2> To run the system using docker, you must have a docker installed </h2>
<p> Open your VS Code <p>

check settings.py 

uncomment the postgre database and comment the sql database
uncomment caches

On your terminal type 

```
docker compose run

```

Docker would setup the system for you. 
To access the website once docker is running, type the link below on the browser you are using

```
127.0.0.1

```


