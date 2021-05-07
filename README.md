# Chirper

![CodeQL](https://github.com/Frozander/Chirper/workflows/CodeQL/badge.svg)

This project is a simple social media app created using flask.

You are free to add into it as long as it makes sense, see the [CONTRIBUTING.md](CONTRIBUTING.md) for contributions.

## To see a working version of the project, check out [chirper.frozander.xyz](https://chirper.frozander.xyz)

## Caution
At this current stage, there probably are multiple security problems and possible exploits with the application. So do not use it apart from developing it further or do if you dare...

## TODO
Deployment to a WSGI environment is not straightforward, so I might need to fix that in the future. But with a bit of fumbling around it can be deployed without any problems.

## How to run
I advise you to create a virtual environment for this app with:
```
python -m venv venv
```
Then on Windows:
```
venv\Scripts\activate.bat
```

On Linux or MacOS:
```
source venv/bin/activate
```

Install the [requirements](requirements.txt) with:
```
python -m pip install -r requirements.txt
```

Create a ".env" file in the root of the repository and look into the [config.py](chirper/config.py) file. You can set the parameters there. Or even add more into the [config.py](chirper/config.py) if you want.

.env:
```
...
FLASK_APP=chirper
SECRET_KEY=super_secret_key
SERVER_NAME=localhost
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/db_name
...
```

**IMPORTANT:** If you don't want to, the default values are set for a development environment, it will use SQLite as the project database. (Just don't forget to rename/delete the migrations folder. Since inter-DBMS migrations are not possible as it stands. The included migrations are for PostgreSQL)

To initialise the database run:
```
flask db init
flask db upgrade
```

You can start a dev server by running:
```
flask run
```
However since almost any browser forces https connections you might need ssl key pairs.
If you do, you can use:
```
python serve.py
```
to serve the app in best possible way.

But if you don't, you can use ad-hoc certificates provided by flask (for development only ofc) by installing PyOpenSSL:
```
pip install pyopenssl
```
and then running the development server with:
```
flask run --cert=adhoc
```


### Using something other than PSQL
If you want to use SQLite or any other RDBMS, you need to delete migrations folder and create the new migrations folder. Just make sure you have a driver for your RDBMS.

**Example**: 

.env:
```
...
SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/db_name
...
```

and then run

```
flask db init
flask db migrate
flask db upgrade
```
