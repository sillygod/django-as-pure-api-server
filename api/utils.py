from contextlib import contextmanager
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.serializers import ValidationError


def format_response(status, message='', data=None, errors=None, **kwargs):

    """An util function unify the api response format
    """

    status_map = {
        200: 'Success',
        400: 'Invalid Parameters',
        404: 'Not Found',
        500: 'Internal Error'
    }

    wrapper = {
        'status': status,
        'message': message or status_map.get(status, message),
        'data': data if data is not None else {}
    }

    if errors is not None:
        wrapper['errors'] = errors

    wrapper.update(**kwargs)

    return wrapper


def api_error_handler(exc, context):
    """handle error response format

    the class APIException has the following attributes

     - status_code
     - default_detail
       a description for error message, Note you can send a serialize json obj string,
       we will unserialize it
     - default_code: we can use it as status code

    """
    response = exception_handler(exc, context)

    return response
