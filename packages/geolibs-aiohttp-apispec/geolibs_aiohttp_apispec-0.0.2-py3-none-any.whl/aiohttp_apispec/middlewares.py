import json

from aiohttp import web
from marshmallow import ValidationError

from .utils import issubclass_py37fix


def get_apispec_schemas(request, handler, schemas_type):
    orig_handler = request.match_info.handler

    if hasattr(orig_handler, schemas_type):
        return getattr(orig_handler, schemas_type)

    if not issubclass_py37fix(orig_handler, web.View):
        return None

    # Keep looking
    method_handler = getattr(orig_handler, request.method.lower(), None)
    if method_handler and hasattr(method_handler, schemas_type):
        return getattr(method_handler, schemas_type)

    return None  # Give up :(


@web.middleware
async def validate_request_middleware(request, handler):
    # data = await request.json()  # application/json -> body
    # data = await request.post()  # form-data -> form
    # data = await request.multipart()  # multipart -> NO
    # data = request.query  # query string -> query
    # data = request.headers  # headers -> headers
    # data = request.match_info  # variable paths -> path

    schemas = get_apispec_schemas(request, handler, '__request_schemas__')
    if not schemas:
        return await handler(request)

    validation_errors = {}

    for location, schema in schemas.items():
        if location == 'body':
            data = await request.json()

        elif location == 'form':
            data = await request.post()

        elif location == 'query':
            data = request.query

        elif location == 'headers':
            data = request.headers

        elif location == 'path':
            data = request.match_info

        else:
            continue

        prefix = request.app['_apispec_request_data_prefix']

        try:
            validation = schemas[location].load(data)
            request[f'{prefix}{location}'] = validation.data

        except ValidationError as exc:
            validation_errors[location] = exc.messages

    if validation_errors:
        raise ValidationError({'request_validation_errors': validation_errors})

    return await handler(request)


@web.middleware
async def validate_response_middleware(request, handler):
    response = await handler(request)

    schemas = get_apispec_schemas(request, handler, '__response_schemas__')
    if not schemas or not schemas.get(response.status):
        return response

    schema = schemas.get(response.status)

    try:
        body = response.body.decode()
        validation = schema['schema'].loads(body)

        if schema['clean']:
            validated_body = json.dumps(validation.data)
            response.body = validated_body.encode()

    except ValidationError as exc:
        raise ValidationError({'response_validation_errors': exc.messages})

    return response
