from .core import create_component_settings


SCHEMA = {
    'env': {
        'type': 'string',
        'allowed': ['production', 'development', 'testing'],
        'required': True
    },
    'components': {
        'type': 'list',
        'empty': True,
        'schema': {'type': 'string'},
        'required': True
    }
}

DEFAULTS = {
    'env': 'development',
    'components': [],
}

SETTINGS = create_component_settings('app', DEFAULTS, SCHEMA)

IS_DEBUG = IS_DEVELOPMENT = SETTINGS['env'] == 'development'
IS_PRODUCTION = SETTINGS['env'] == 'production'
IS_TESTING = SETTINGS['env'] == 'testing'
