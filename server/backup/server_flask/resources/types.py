"""Types for type validation during flask_restful argument parsing."""
from jsonschema import validate

schemas = {
    'applicationSchema': {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'version': {'type': 'string'}
        }
    },

    'systemInfoSchema': {
        'type': 'object',
        'properties': {
            'version': {'type': 'string'}
        }
    },

    'inputCrashReportSchema': {
        "type": "object",
        'properties': {
            'application': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'version': {'type': 'string'}
                }
            },
            "system_info": {
                'type': 'object',
                'properties': {
                    'version': {'type': 'string'}
                }
            },
        }
    }
}


def useSchema(schema):
    """Universal type checker generator."""
    def temp(value, name):
        """Function returned as type checker."""
        validate(value, schemas[schema])
        return value
    return temp
