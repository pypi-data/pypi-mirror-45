def docs(**kwargs):
    def wrapper(func):
        kwargs['produces'] = ['application/json']
        if not hasattr(func, '__apispec__'):
            func.__apispec__ = {'parameters': [], 'requests': {}, 'responses': {}}
        extra_parameters = kwargs.pop('parameters', [])
        extra_responses = kwargs.pop('responses', {})
        func.__apispec__['parameters'].extend(extra_parameters)
        func.__apispec__['responses'].update(extra_responses)
        func.__apispec__.update(kwargs)
        return func

    return wrapper


# @request_schema(IndexSchema(strict=True), location='body')
# @request_schema(IndexSchema(strict=True), location='form')
# @request_schema(IndexSchema(strict=True), location='query')
# @request_schema(IndexSchema(strict=True), location='headers')
# @request_schema(IndexSchema(strict=True), location='path')
def request_schema(schema, location, validate=True):
    if callable(schema):
        schema = schema()

    if not location:
        location = 'body'

    apispec_options = {
        'default_in': location
    }

    def wrapper(func):
        if not hasattr(func, '__apispec__'):
            func.__apispec__ = {'parameters': [], 'requests': {}, 'responses': {}}

        func.__apispec__['requests'][location] = {
            'schema': schema,
            'options': apispec_options
        }

        if validate:
            if not hasattr(func, '__request_schemas__'):
                func.__request_schemas__ = {}
            func.__request_schemas__[location] = schema

        return func

    return wrapper


use_kwargs = request_schema


# @response_schema(IndexSchema(), 200, description='Standard response', clean=True)
def response_schema(schema, code=200, description=None, validate=True, clean=False):
    if callable(schema):
        schema = schema()

    def wrapper(func):
        if not hasattr(func, '__apispec__'):
            func.__apispec__ = {'parameters': [], 'requests': {}, 'responses': {}}

        func.__apispec__['responses'][code] = {
            'schema': schema,
            'description': description,
        }

        if validate:
            if not hasattr(func, '__response_schemas__'):
                func.__response_schemas__ = {}
            func.__response_schemas__[code] = {
                'schema': schema,
                'clean': clean
            }

        return func

    return wrapper


marshal_with = response_schema
