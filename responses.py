# -*- coding: utf-8 -*-
"""
@author: Yiğit GÜMÜŞ


This module provides a set of utility functions for generating JSON responses with different statuses and messages.

The `Responses` class provides static methods for generating JSON responses with different statuses and messages.
The statuses and messages can be customized according to the needs of the application.

The class provides methods for generating responses with the following statuses:

- OK!
- Internal Server Error!
- Service Unavailable!
- Already Exist!
- Too Large File Upload!
- Unauthorized!
- Page Not Found!
- Forbidden!

Each method takes a message and an optional error as arguments and returns a `Response` object.

Example usage:

```python
from flask import Flask, jsonify

from responses import Responses

app = Flask(__name__)

@app.route('/ok')
def ok_route():
    return Responses.ok('Everything is fine')

@app.route('/internal_server_error')
def internal_server_error_route():
    return Responses.internal_server_err('Something went wrong', Exception('Something went wrong'))

if __name__ == '__main__':
    app.run()
"""

from flask import (
    make_response,
    Response,
    jsonify
)
from typing import Any



class Responses:
    """
    A class that provides static methods for generating JSON responses with different statuses and messages.

    This class provides a set of static methods that can be used to generate JSON responses with different statuses
    and messages. The statuses and messages can be customized according to the needs of the application.

    The class provides methods for generating responses with the following statuses:

    - OK!
    - Internal Server Error!
    - Service Unavailable!
    - Already Exist!
    - Too Large File Upload!
    - Unauthorized!
    - Page Not Found!
    - Forbidden!

    Each method takes a message and an optional error as arguments and returns a `Response` object.

    Example usage:

    ```
    from flask import Flask, jsonify
    
    from responses import Responses # This file

    app = Flask(__name__)

    @app.route('/ok')
    def ok_route():
        return Responses.ok('Everything is fine')

    @app.route('/internal_server_error')
    def internal_server_error_route():
        return Responses.internal_server_err('Something went wrong', Exception('Something went wrong'))

    if __name__ == '__main__':
        app.run()
    ```
    """

    @staticmethod
    def ok(msg: str | dict[str, Any]) -> Response:
        """
        Creates a JSON response with a status of 'OK!' and the provided message.

        Args:
            msg (str or dict[str, Any]): The message to include in the response.

        Returns:
            Response: The JSON response with the provided message.
        """

        return make_response(
            jsonify({
                "status": 'OK!',
                "msg": msg,
            }),
            200
        )

    @staticmethod
    def internal_server_err(msg: str, err: Exception) -> Response:
        """
        Creates a JSON response with a status of 'Internal Server Error!' and the provided message and error.

        Args:
            msg (str): The message to include in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the provided message and error.
        """

        return make_response(
            jsonify({
                "status": 'Internal Server Error!',
                "msg": msg,
                "error": str(err)
            }),
            500
        )

    @staticmethod
    def OK(msg: str) -> Response:
        """
        Creates a JSON response with a status of 'OK!' and the provided message.

        Args:
            msg (str): The message to include in the response.

        Returns:
            Response: The JSON response with the provided message.
        """

        return Response.ok(msg)

    @staticmethod
    def iserr(msg: str, err: Exception) -> Response:
        """
        Shortcut for internal server error.

        Args:
            msg (str): The error message.
            err (Exception): The exception that occurred.

        Returns:
            Response: The response object representing the internal server error.
        """

        return Responses.internal_server_err(msg, err)

    @staticmethod
    def service_unavailable(msg: str, err: Exception) -> Response:
        """
        Returns a Flask Response object with a JSON payload containing the provided message and error,
        indicating that the service is unavailable.

        Args:
            msg (str): The message to include in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the provided message and error.
        """

        return make_response(
            jsonify({
                "status": 'Service Unavailable!',
                "msg": msg,
                "error": str(err)
            }),
            500
        )

    @staticmethod
    def already_exist(msg: str, err: Exception) -> Response:
        """
        Returns a Flask Response object with a JSON payload containing the provided message and error,
        indicating that the resource already exists.

        Args:
            msg (str): The message to include in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the provided message and error.
        """

        return make_response(
            jsonify({
                "status": 'Already Exist!',
                "msg": msg,
                "error": str(err)
            }),
            202
        )

    @staticmethod
    def too_large(msg: str, err: Exception) -> Response:
        """
        Generates a JSON response with a status of 'Too Large File Upload!', a message, and an error.

        Parameters:
            msg (str): The message to be included in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the specified status, message, and error.
        """

        return make_response(
            jsonify({
                "status": 'Too Large File Upload!',
                "msg": msg,
                "error": str(err)
            }),
            413
        )

    @staticmethod
    def unauthorized(msg: str, err: Exception) -> Response:
        """
        Generates a JSON response with a status of 'Unauthorized!', a message, and an error.

        Parameters:
            msg (str): The message to be included in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the specified status, message, and error.
        """

        return make_response(
            jsonify({
                "status": 'Unauthorized!',
                "msg": msg,
                "error": str(err)
            }),
            401
        )

    @staticmethod
    def not_found(msg: str, err: Exception) -> Response:
        """
        Generates a JSON response with a 'Not Found!' status, a custom message, and the error message.

        Parameters:
            msg (str): The custom message to be included in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the 'Not Found!' status, the custom message, and the error message.
        """

        return make_response(
            jsonify({
                "status": 'Not Found!',
                "msg": msg,
                "error": str(err)
            }),
            404
        )

    @staticmethod
    def forbidden(msg: str, err: Exception) -> Response:
        """
        Generates a JSON response with a status of 'Forbidden!', a custom message, and the error message.

        Parameters:
            msg (str): The custom message to be included in the response.
            err (Exception): The error that occurred.

        Returns:
            Response: The JSON response with the 'Forbidden!' status, the custom message, and the error message.
        """

        return make_response(
            jsonify({
                "status": 'Forbidden!',
                "msg": msg,
                "error": str(err)
            }),
            403
        )
