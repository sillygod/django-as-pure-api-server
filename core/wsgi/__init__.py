import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# we can apply WSGI application here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
