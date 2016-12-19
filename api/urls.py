from django.conf.urls import (
    url,
    include
)

from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger import renderers as swagger_renderers
from rest_framework.decorators import (
    api_view,
    renderer_classes
)

from rest_framework import (
    schemas,
    renderers,
    response
)


generator = schemas.SchemaGenerator(title='sun api', url='/api/', urlconf='api.urls')

@api_view()
@renderer_classes([renderers.CoreJSONRenderer, swagger_renderers.OpenAPIRenderer, swagger_renderers.SwaggerUIRenderer])
def schema_view(request):
    schema = generator.get_schema(request)
    return response.Response(schema)


urlpatterns = [
    url(r'^$', schema_view),
    url(r'^(?P<version>v1|v2)/member/', include('api.member.urls', namespace='member')),
]
