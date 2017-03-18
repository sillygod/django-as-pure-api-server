# Django as Pure API Server

a pure api server implemented by django and django rest framework


## DEVELOPMENT

#### INSTALL

```sh
pip install -r requirements/dev.txt # for dev 

```

and prepare your `env.ini` file. overwrite the settings you want and put it in the directory `settings`

ex.

```ini

[django settings]
DEBUG=True
INSTALLED_APPS=('debug_toolbar', )
MIDDLEWARE_CLASSES=('debug_toolbar.middleware.DebugToolbarMiddleware', )
DATABASES={'default':{'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'weis', 'USER': 'jing', 'PASSWORD': '123456', 'HOST': 'postgres'}}

```

#### RUN SERVER

You can use django command `python manage.py runserver`. You can also use uwsgi to run server with the following command.

```sh
STATIC=/home/jing/Desktop/sun-practice/static PORT=8000 /home/jing/miniconda2/envs/sun/bin/uwsgi --ini core/wsgi/uwsgi.ini
```

then open http://127.0.0.1:8000 you will see it.

or you can use docker-compose to run server if you want docker a try.

You can use above example env.ini if you want to use docker-compose as a developer server. the env in docker-compose is more closer to the formal server.


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

### deploy with heroku



# What we are done

 - [x] django debug toolbar enable ajax -- https://github.com/djsutho/django-debug-toolbar-request-history/tree/master/ddt_request_history
 - [x] update django-rest-framework, django
 - [ ] jwt authentication
 - [ ] unit test
 - [ ] functional test
 - [ ] update [docker-compose](https://docs.docker.com/compose/compose-file/compose-versioning/)
 - [ ] add doc with readthedoc, write some keyontes or tutorial?
