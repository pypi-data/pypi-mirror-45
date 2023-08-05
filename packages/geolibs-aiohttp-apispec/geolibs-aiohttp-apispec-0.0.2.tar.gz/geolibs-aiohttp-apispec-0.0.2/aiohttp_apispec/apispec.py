import copy

from pathlib import Path

from aiohttp import web
from aiohttp.hdrs import METH_ANY, METH_ALL
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from jinja2 import Template

from .utils import get_path, get_path_keys, issubclass_py37fix

PATHS = {'get', 'put', 'post', 'delete', 'patch'}
VALID_RESPONSE_FIELDS = {'description', 'headers', 'examples'}
VALID_RESPONSE_FULL_FIELDS = VALID_RESPONSE_FIELDS.union({'schema'})


class AIOHTTP_APISpec:
    def __init__(self, app, title, version, url='/api_docs/swagger.json',
                 swagger_path='/api_docs', static_path='/static/swagger',
                 request_data_prefix='validated_body', **kwargs):
        self.plugin = MarshmallowPlugin()
        self.spec = APISpec(plugins=[self.plugin], openapi_version='2.0',
                            title=title, version=version, **kwargs)

        self.url = url
        self.swagger_path = swagger_path
        self.static_path = static_path
        self._registered = False
        self._request_data_prefix = request_data_prefix

        if app is not None:
            self.register(app)

    def swagger_dict(self):
        return self.spec.to_dict()

    def register(self, app):
        if self._registered is True:
            return

        app['_apispec_request_data_prefix'] = self._request_data_prefix

        async def doc_routes(app_):
            self._register(app_)

        app.on_startup.append(doc_routes)
        self._registered = True

        async def swagger_handler(request):
            return web.json_response(request.app['swagger_dict'])

        app.router.add_routes([web.get(self.url, swagger_handler)])

        if self.swagger_path is not None:
            self.add_swagger_web_page(app, self.static_path, self.swagger_path)

    def add_swagger_web_page(self, app, static_path, view_path):
        static_files = Path(__file__).parent / 'static'
        app.router.add_static(static_path, static_files)

        with open(str(static_files / 'index.html')) as swagger_template:
            template = Template(swagger_template.read())
            template = template.render(path=self.url, static=static_path)

        async def swagger_view(_):
            return web.Response(
                text=template, content_type='text/html'
            )

        app.router.add_route('GET', view_path, swagger_view)

    def _register(self, app):
        for route in app.router.routes():
            if issubclass_py37fix(route.handler, web.View) and route.method == METH_ANY:
                for attr in dir(route.handler):
                    if attr.upper() in METH_ALL:
                        view = getattr(route.handler, attr)
                        method = attr
                        self._register_route(route, method, view)

            else:
                method = route.method.lower()
                view = route.handler
                self._register_route(route, method, view)

        app['swagger_dict'] = self.swagger_dict()

    def _register_route(self, route, method, view):
        if not hasattr(view, '__apispec__'):
            return None

        url_path = get_path(route)
        if not url_path:
            return None

        self._update_paths(view.__apispec__, method, url_path)

    def _update_paths(self, data, method, url_path):
        if method not in PATHS:
            return

        # Requests
        if 'requests' in data:
            for location, params in data['requests'].items():
                parameters = self.plugin.openapi.schema2parameters(
                    params['schema'], **params['options']
                )
                data['parameters'].extend(parameters)

            del data['requests']

        # Parameters
        existing = [p['name'] for p in data['parameters'] if p['in'] == 'path']
        data['parameters'].extend(
            {'in': 'path', 'name': path_key, 'required': True, 'type': 'string'}
            for path_key in get_path_keys(url_path)
            if path_key not in existing
        )

        # Responses
        if 'responses' in data:
            responses = {}
            for code, params in data['responses'].items():
                if 'schema' in params:
                    raw_parameters = self.plugin.openapi.schema2parameters(
                        params['schema'], required=params.get('required', False)
                    )[0]
                    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#responseObject
                    parameters = {
                        k: v
                        for k, v in raw_parameters.items()
                        if k in VALID_RESPONSE_FULL_FIELDS
                    }
                    for extra_info in VALID_RESPONSE_FIELDS:
                        if extra_info in params:
                            parameters[extra_info] = params[extra_info]
                    responses[code] = parameters

                else:
                    responses[code] = params

            data['responses'] = responses

        operations = copy.deepcopy(data)
        self.spec.path(path=url_path, operations={method: operations})


def setup_apispec(
        app, title='API documentation', version='0.0.1',
        url='/api_docs/swagger.json', swagger_path='/api_docs',
        static_path='/static/swagger', request_data_prefix='validated_',
        **kwargs):
    AIOHTTP_APISpec(app, title, version, url, swagger_path, static_path, request_data_prefix,
                    **kwargs)
