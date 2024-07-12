from app import app

import webbrowser
import os

webbrowser.open('http://localhost:8080')
app.run(host='0.0.0.0', port=8080, debug=os.getenv('IS_DEV'))
