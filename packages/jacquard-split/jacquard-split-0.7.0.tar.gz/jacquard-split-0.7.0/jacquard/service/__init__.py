"""
Web service subsystem.

The primary means by which the Jacquard server is accessed in production is
an HTTP API, which is the domain of this subsystem. It presents a WSGI HTTP
application.

The only user-facing API from this subsystem is `get_wsgi_app`, which takes a
system configuration and returns a WSGI callable.
"""

from jacquard.service.wsgi import get_wsgi_app
from jacquard.service.endpoints import Endpoint

__all__ = ("get_wsgi_app", "Endpoint")
