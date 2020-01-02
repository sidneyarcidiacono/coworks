import json
import requests

from coworks import Admin

from .microservice import *


class DoumentedMS(MS):

    def get(self):
        """Root access."""
        return "get"

    def post_content(self, value: int, other: str = "none"):
        """Add content."""
        return f"post_content {value}{other}"


def test_documentation(local_server_factory):
    ms = DoumentedMS()
    ms.register_blueprint(Admin(), url_prefix="/admin")
    local_server = local_server_factory(ms)
    response = local_server.make_call(requests.get, '/admin/routes', timeout=200.5)
    assert response.status_code == 200
    assert json.loads(response.text)["/"] == {
        "GET": {
            "doc": "Root access.",
            "signature": "(self)"
        }
    }
    assert json.loads(response.text)["/content/{value}"] == {
        "POST": {
            "doc": "Add content.",
            "signature": "(self, value: int, other: str = \'none\')"
        }
    }
    assert json.loads(response.text)["/admin/routes"] == {
        "GET": {
            "doc": '',
            "signature": "(self)"
        }
    }
