"""
@author: Yiğit GÜMÜŞ

A simple desktop application that uses the `webview` library to display a Flask application.

This module creates a window using the `webview.create_window` function and starts the webview application.

The Flask application is imported from the `app.py` file.

The `webview` library is used to create a window and start the application.

"""

import webview
from app import app

window = webview.create_window('HEZARTECH DATA PREPROCESSING APP', app)
webview.start()
