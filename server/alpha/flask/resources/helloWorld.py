"""Test wether server is working."""
from flask_restful import Resource


class HelloWorld(Resource):
    """Test wether server is working by return of 'hello world'."""

    def get(self):
        """Return hello world in JSON."""
        return {'hello': 'world'}
