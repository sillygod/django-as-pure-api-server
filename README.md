[![Build Status](https://travis-ci.org/sillygod/django-as-pure-api-server.svg?branch=master)](https://travis-ci.org/sillygod/django-as-pure-api-server)
[![GitHub license](https://img.shields.io/github/license/sillygod/django-as-pure-api-server.svg)](https://github.com/sillygod/django-as-pure-api-server/blob/master/LICENSE)  

# Django as Pure API Server

A pure api server implemented by django and django rest framework. This combines some development tools like, pytest, django-debug-toolbar, etc.


# DEVELOPMENT

## INSTALL

```sh
pip install -r requirements/dev.txt # for dev 
```

or use pipenv install

```sh
pipenv install -d (including dev dependencies)
```

to start the interactive virtualenv to use `pipenv shell --anyway` if you use pipenv.


> I encounter a problem when I use pipenv. I need to add the folowing variable in the ~/.bash_profile
> export LC_ALL=en_US.UTF-8
> export LANG=en_US.UTF-8

## Customize

adjust the `settings.dev.py` or `settings.prod.py` for your need. We will grab the environment variable `env` to decide to use `dev.py` or `prod.py`'s settings. By Default, we use dev.py.

## Create a new app

```sh
python manage.py startapp [your app name]
```

## Migration

Note! you should run `python manage.py makemigrations member` first and then run all migrations

If you want to without specifying the app name to run migrate, you have to add an empty `migrations` module in the app directory.

## RUN SERVER

You can use django command `python manage.py runserver`. You can also use uwsgi to run server with the following command.

```sh
STATIC=/your absolute project path/static PORT=8000 /your path of uwsgi --ini core/wsgi/uwsgi.ini
```

then open http://127.0.0.1:8000 you will see it.

or you can use docker-compose to run server if you want docker a try.

```sh
docker-compose up # this will build image first time
docker-compose run app python manage.py collectstatic
docker-compose run app python makemigrations or migrate
#.. it seems that you need to specify the app to perform makemigrations 
# ex. python makemigrations member
docker-compose run app python manage.py createsuperuser
docker-compose logs [service name] # can see the log for certain service
```

## pylint

we can see pylint setting by run the following script

```sh
pylint --generate-rcfile > .pylintrc
```


## Run Test

we use `pytest` with django.

coverage?

# DEPLOY


```sh
pip install -r requirements/prod.txt # or

pipenv install
```

prod.py

```py
DEBUG = False
```

# Preview

### admin page

![admin page](https://i.imgur.com/mzHUSoM.png)

### swagger api

![swagger api](https://i.imgur.com/R1XrVY3.png)

### django debug tool bar

![django debug tool bar](https://i.imgur.com/0T4DNAn.png)

# What we are done

 - [ ] functional test
