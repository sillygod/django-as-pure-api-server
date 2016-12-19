# Django as Pure Api Server

a pure api server implemented by django


## DEVELOPMENT

#### INSTALL

```sh
pip install -r requirements/dev.txt # for dev 

```

and prepare your `env.ini` file. overwrite the settings you want and put it in the directory `settings`

ex.

```ini

DEBUG = False
INSTALLED_APPS = ('djangodebugtoolbar', ) ; note this will append new app in INSTALLED_APP

```

#### RUN SERVER

You can use django command `python manage.py runserver`. You can also use uwsgi to run server with the following command.

```sh
STATIC=/home/jing/Desktop/django-as-pure-api-server/static PORT=8000 /home/jing/miniconda2/envs/sun/bin/uwsgi --ini core/wsgi/uwsgi.ini
```

then open 127.0.0.1:8000 you will see it.

or you can use docker-compose to run server if you want docker a try.

```sh
docker-compose up # this will build image first time

docker-compose logs [service name] # can see the log for certain service
```


## DEPLOY


```sh
pip install -r requirements/prod.txt
```

also prepare your `env.ini` file.

```ini
DEBUG = False
```


# What we are done

 - [x] api versioning
 - [x] api swagger doc settings
 - [x] docker env simulate
 - [ ] member system bare bone structure
 - [ ] social auth
 - [ ] jwt authentication
 - [x] how to make all app under api directory foundable by import
 - [x] a tree structure for certain data
 - [ ] upgrade django to version 1.1x?
 
