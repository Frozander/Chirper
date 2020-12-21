# Chirper

![CodeQL](https://github.com/Frozander/Chirper/workflows/CodeQL/badge.svg)

This project is a simple social media app created using flask.

You are free to add into it as long as it makes sense, see the [CONTRIBUTING.md](CONTRIBUTING.md) for contributions.

## How to run
Create a ".env" file in the root of the repository and look into the "config.py" file. You can set the parameters there.

If you don't want to, the default values are set for a development environment, it will use SQLite as the project database.

To initialise the database run:
```
flask db init
flask db migrate
flask db upgrade
```

You can start a dev server by running:
```
flask run
```
However in Chromium based browsers the neccesary cookies are not stored without a domain name (or a psuedo one like localhost). Which means you need ssl keys to run it even in development mode as it stands.

To get a better server:
```
python serve.py
```

As it stands currently there is no set way to host the app as a WSGI application. However it should not be hard to write one yourself.
