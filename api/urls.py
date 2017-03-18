from urllib.parse import (
    urlparse,
    urljoin
)

from django.conf.urls import (
    url,
    include
)

from rest_framework.decorators import (
    api_view,
    renderer_classes,
    permission_classes
)

from rest_framework import (
    schemas,
    renderers,
    permissions,
    response
)

from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger import renderers as swagger_renderers

import coreapi
import yaml


class MySchemaGenerator(schemas.SchemaGenerator):

    def get_link(self, path, method, view):
        """custom the coreapi using the func.__doc__.
        """

        fields = self.get_path_fields(path, method, view)
        yaml_doc = None

        func = getattr(view, view.action) if getattr(view, 'action', None) else None
        if func and func.__doc__:
            try:
                func_doc, schema_doc = func.__doc__.split('--swagger schema--')
                yaml_doc = yaml.load(schema_doc)
            except:
                yaml_doc = None

        if yaml_doc:
            desc = yaml_doc.get('desc', func_doc)
            ret = yaml_doc.get('ret', '')
            err = yaml_doc.get('err', '')
            _method_desc = func_doc
            params = yaml_doc.get('params', [])
            for i in params:
                _name = i.get('name')
                _desc = i.get('desc', '')
                _required = i.get('required', True)
                _type = i .get('type', 'string')
                _location = i.get('location', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:
            _method_desc = func.__doc__ if func and func.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )


generator = MySchemaGenerator(title='sun api', url='/api/', urlconf='api.urls')

@api_view()
@permission_classes((permissions.AllowAny, ))
@renderer_classes([renderers.CoreJSONRenderer, swagger_renderers.OpenAPIRenderer, swagger_renderers.SwaggerUIRenderer])
def schema_view(request):
    schema = generator.get_schema(request)
    return response.Response(schema)


urlpatterns = [
    url(r'^$', schema_view),
    url(r'^(?P<version>v1|v2)/member/', include('api.member.urls', namespace='member')),

]
