#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yiğit GÜMÜŞ

A Flask application for a data labeling tool.

This module defines the routes and endpoints for the application.

The application uses the `Flask` framework to handle HTTP requests.

The routes and endpoints include:

- '/': The root route, which redirects to the '/index' route.
- '/index': The index route, which renders the index page if the user is logged in.
- '/login': The login route, which renders the login page.
- '/logout': The logout route, which removes the user_id from the session.
- '/uploadData': The upload data route, which retrieves a list of files from the 'UPLOAD_FOLDER' directory that do not have the '.gitkeep' extension.
- '/labelData': The label data route, which retrieves a list of cleaned data files from the 'CLEANED_DATA_FOLDER' directory that do not have the '.gitkeep' or '.xlsx' extensions.
- '/labelData/<string:filename>': The label data editor route, which retrieves cleaned data from the specified file.
- '/cleanData': The clean data route, which retrieves a list of files from the 'UPLOAD_FOLDER' directory that do not have the '.gitkeep' extension.
- '/exportData/<string:ftype>/<string:filename>': The export data route, which returns a file from the 'CLEANED_DATA_FOLDER' directory.

The application also defines utility functions for finding a user via email, setting the session user, and handling cross-origin resource sharing.

"""
from flask import (
    Flask,

    request,
    Response,

    render_template,
    send_file,

    flash,
    redirect,
    url_for,

    make_response
)
# For cross-origin resource sharing
from flask_cors import CORS

# For file upload
from werkzeug.utils import secure_filename

# For Request Responses
from responses import Responses as res

# For utility functions of this project.
from utils import (
    login_required_render_template,
    find_user_via_email,
    set_session_user,
    session,
    get_session_property,
    allowed_file,
    cleaned_data_folder_is_file,
    set_folders,
    set_template_names,
    get_template_name,
    json_to_csv,
    extract_text_and_ids_from_dataset,
    remove_file_extensions,
    data_cleaner,
    save_to_db
)

# For access to the .env file
__import__('dotenv').load_dotenv()

# For hashing passwords
import bcrypt

# Default libraries for general purpose uses
import os
import json
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')

# Add CORS to allow cross-origin resource sharing
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['CLEANED_DATA_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'clean_data')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB for maximum file upload
app.config['DROPZONE_MAX_FILES'] = 1,
app.config['DROPZONE_DEFAULT_MESSAGE'] = 'Dosyaları yüklemek için buraya bırakınız..'

templates = {
    'index': 'index.html',
    'login': 'login.html',
    'upload_data': 'upload_dataset.html',
    'label_data': 'label_dataset.html',
    'label_data_editor': 'label_dataset_editor.html',
    'clean_data': 'clean_dataset.html',
    'export_data': 'export_dataset.html',
}

set_template_names(templates)
set_folders(app.config['UPLOAD_FOLDER'], app.config['CLEANED_DATA_FOLDER'])

#----------------------------
# General site skeleton.
#----------------------------
@app.get('/')
@app.get('/index')
def index() -> Response:
    """
    Render the index page if the user is logged in.

    Returns:
        Response: The rendered index page if the user is logged in,
                  otherwise a redirect to the login page.
    """
    if get_session_property('user_id') is None:
        return redirect(url_for('login'))

    return render_template(get_template_name('index'), session_user=session)

# For favicon.ico service.
@app.route('/favicon.ico')
def favicon() -> Response:
    """
    Route for serving the favicon.ico file.

    Returns:
        Response: The response object containing the favicon.ico file.

    """

    return make_response(send_file(os.path.join(
        app.root_path,
        app.static_folder + '/HEZARTECH.png'  # or /favicon.ico | I prefer this.
    )),
        200
    )


@app.get('/robots.txt')
def robots_txt() -> tuple[Response, int]:
    """
    A route that serves the robots.txt file.

    Returns:
        tuple[Response, int]: A tuple containing the response object and the HTTP status code.
    """

    return send_file(os.path.join(
        app.root_path,
        app.static_folder
    ) + '/robots.txt'), 200


@app.errorhandler(404)
def not_found(err) -> Response:
    """
    Handle the HTTP 404 Not Found error.

    Args:
        err (Exception): The exception that occurred.

    Returns:
        Response: The response object with the error message.
    """
    return res.not_found('Page not found in this Hezartech Project.', err)

@app.errorhandler(413)
def too_large(err):
    """
    Handles the error when the file size is too large.

    Args:
        err (Exception): The error that occurred.

    Returns:
        Response: The response object with the error message.

    Raises:
        None.
    """
    return res.too_large("Dosya boyutu 50MB'a tan fazla!", err)

@app.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    """
    A route that handles the login functionality.

    Parameters:
        None

    Returns:
        Response: The response object containing the result of the login process.

    Raises:
        None

    Notes:
        - This route is accessible via the '/login' URL and the HTTP POST method.
        - The route expects a JSON payload in the request body with the 'email' and 'password' fields.
        - If the 'email' or 'password' fields are missing, the route returns a 401 Unauthorized response.
        - If the user with the given email does not exist in the database, the route returns a 401 Unauthorized response.
        - If the password provided in the request does not match the stored password for the user, the route returns a 403 Forbidden response.
        - If the login is successful, the route generates a JSON Web Token (JWT) and returns a 201 Created response with the token.
    """

    if request.method == 'GET':
        return render_template(get_template_name('login'))
    elif request.method == 'POST':
        # Get the user's information from the request
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user from the database
        user = find_user_via_email(email)

        # Check that the user exists and the password is correct
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Add the user's id to the session
            set_session_user(user['_id'], email, user['name'])

            return redirect(url_for('index'))

        # When login failure.
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    """
    Remove the user_id from the session and redirect to the index page.

    Returns:
        Response: A redirect response to the index page.

    """
    session.pop('user_id', None)
    return redirect(url_for('index'))

#--------

@app.route('/uploadData', methods=['GET', 'POST'])
def upload_data() -> Response:
    """
    Route for handling file uploads.

    This function is responsible for handling the '/uploadData' route. It accepts both GET and POST requests.

    Parameters:
        None

    Returns:
        Response: The response object.

    Raises:
        None

    Notes:
        1. If the request method is GET, the function returns the result of the `login_required_render_template` function,
          which renders the template specified by the `get_template_name` function.

        2. If the request method is POST, the function checks if the 'file' field is present in the request.files.

            2.1 If the 'file' field is not present, a flash message is displayed indicating that no file was selected,
            and the function redirects the user to the current URL.

            2.2 If the 'file' field is present, the function retrieves the file object and checks if the filename is empty.

                2.2.1 If the filename is empty, a flash message is displayed indicating that no file was selected,
                and the function redirects the user to the current URL.

                2.2.2 If the filename is not empty, the function checks if the file type is allowed.

                    2.2.2.1 If the file type is allowed, the function generates a secure filename, saves the file to the
                    specified upload folder, and redirects the user to the 'upload_data' route.

                    2.2.2.2  If the file type is not allowed, a forbidden response is returned with a message indicating that
                    the file type is not allowed. Only .csv and .xlsx files are allowed.
    """

    if request.method == 'GET':
        return login_required_render_template(
            get_template_name('upload_data')
        )
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files.get('file')
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                        datetime.now().strftime('%Y%m%d%H%M%S') + '_' + filename))

                return redirect(url_for('upload_data'))

            return res.forbidden('File type not allowed. Only .csv and .xlsx files are allowed.')

        flash('No selected file')
        return redirect(request.url)


@app.route('/annotateData')
@app.route('/labelData', methods=['GET'])
def label_data() -> Response:
    """
    Route for the '/annotateData' and '/labelData' endpoints.
    Retrieves a list of files from the 'CLEANED_DATA_FOLDER' directory
    that do not have the '.gitkeep' or '.xlsx' extensions.
    Returns a rendered template with the list of files.

    Returns:
        Response: The rendered template with the list of files.
    """

    files: list[str] = []
    for file in os.listdir(app.config['CLEANED_DATA_FOLDER']):
        if cleaned_data_folder_is_file(file) \
         and ('.gitkeep' not in file) and ('.xlsx' not in file) and ('.json' not in file):
            files.append(file)


    return login_required_render_template(
        get_template_name('label_data'),
        files = files
    )

@app.route('/annotateData/<string:filename>', methods=['GET'])
@app.route('/labelData/<string:filename>', methods=['GET', 'POST'])
def label_data_editor(filename: str) -> Response:
    """
    Route for handling the '/annotateData/<string:filename>' and '/labelData/<string:filename>' endpoints.

    Args:
        filename (str): The name of the dataset file.

    Returns:
        Response: The rendered template with the dataset and filename.
    """

    if request.method == 'GET':
        dataset = []
        _nested_dataset_list = extract_text_and_ids_from_dataset(filename)
        for data in _nested_dataset_list:
            dataset.append({
                'id': data[0],
                'text': data[1]
            })

        del _nested_dataset_list

        return login_required_render_template(
            get_template_name('label_data_editor'),
            dataset=dataset,
            filename=filename
        )


@app.route('/cleanData', methods=['GET'])
def clean_data() -> Response:
    """
    Route for the '/cleanData' endpoint. Retrieves a list of files from the 'UPLOAD_FOLDER' directory
    that do not have the '.gitkeep' extension. Returns a rendered template with the list of files.

    Returns:
        Response: The rendered template with the list of files.
    """

    if request.method == 'GET':
        items: list[str] = []
        for item in os.listdir(app.config['UPLOAD_FOLDER']):
            if os.path.isfile(app.config['UPLOAD_FOLDER'] + '/' + item) and '.gitkeep' not in item:
                items.append(item)

        return login_required_render_template(
            get_template_name('clean_data'),
            items = items
        )

@app.route('/cleanData/<string:filename>', methods=['GET'])
def get_clean_data(filename: str) -> Response:
    """
    Route for the '/cleanData/<string:filename>' endpoint.

    Retrieves cleaned data from the specified file.

    Args:
        filename (str): The name of the file to retrieve cleaned data from.

    Returns:
        Response: The response object containing the cleaned data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    return data_cleaner(filename)

@app.route('/exportData', methods=['GET'])
def export_data() -> Response:
    """
    Route for the '/exportData' endpoint.

    Retrieves a list of cleaned data files from the 'CLEANED_DATA_FOLDER' directory
    and returns a rendered template with the list of cleaned data files.

    Returns:
        Response: The rendered template with the list of cleaned data files.
    """

    files: list[str] = [] # List of cleaned data of .xlsx and .csv files
    json_files: list[str] = [] # List of cleaned data of .json files

    for file in os.listdir(app.config['CLEANED_DATA_FOLDER']):
        if cleaned_data_folder_is_file(file) and '.gitkeep' not in file \
            and (file[-5:] != '.json'):
            files.append(file)

        if cleaned_data_folder_is_file(file) and file[-5:] == '.json':
            json_files.append(file)


    files = remove_file_extensions(files)
    files = list(set(files))

    json_files = remove_file_extensions(json_files)

    return login_required_render_template(
        get_template_name('export_data'),
        files = files,
        json_files = json_files
    )


@app.route('/exportData/<string:ftype>/<string:filename>', methods=['GET'])
def export_data_file(ftype: str, filename: str) -> Response:
    """
    Route for the '/exportData' endpoint.

    Retrieves a list of cleaned data files from the 'CLEANED_DATA_FOLDER' directory
    and returns a rendered template with the list of cleaned data files.

    Returns:
        Response: The rendered template with the list of cleaned data files.
    """
    return send_file(
        app.config['CLEANED_DATA_FOLDER']+'/'+
        filename + '.' +ftype,
        as_attachment=True
    )

@app.route('/exportData/jsontocsv/<string:filename>')
def export_csv_from_json(filename: str) -> Response:
    """
    Extract JSON data ant translate to csv for download
    Parameters:
        filename (str): This is came from url so it is not set by hand.

    Returns:
        Response: The response object containing the result of the export operation.
    """
    err = json_to_csv(filename+'.json')
    if err is not None:
        return res.iserr('Something went wrong when downloading exported (labelled) dataset.', err)

    return send_file(
        f"{app.config['CLEANED_DATA_FOLDER']}/{filename}.csv",
        as_attachment=True
    )


@app.route('/exportData/json', methods=['POST'])
def export_json() -> Response:
    """
    Export data in JSON format.
    This function is a route handler for the '/exportData/json' endpoint. It expects a POST request with JSON-formatted data.
    Parameters:
        None
    Returns:
        Response: The response object containing the result of the export operation.
    Description:
        This function first retrieves the JSON data from the request. If the request is not JSON-formatted, it returns an error response.
        Next, it checks if the 'dataset' and 'data' fields in the request are both present. If they are not, it returns an error response.
        The function then constructs a filename by replacing the file extension of the 'dataset' field with 'json'.
        It opens the file with the constructed filename in the 'CLEANED_DATA_FOLDER' directory and writes the 'data' field from the request to the file in JSON format.
        After writing the data to the file, it calls the 'save_to_db' function with the request data.
        If the 'save_to_db' function returns a success status, it redirects the user to the 'export_data' route.
        If there is an error during the export or saving to the database, it returns an error response with the appropriate error message.
    """

    req = request.get_json()

    if req is None:
        return res.iserr('Request must be JSON formatted.')

    if req.get('dataset') in [None, ''] and req.get('data') in [None, '', {}, []]:
        return res.iserr('Dataset must be provided.')

    filename = req.get('dataset').replace('xlsx', 'json') \
                                 .replace('csv', 'json')

    with open(f"{app.config['CLEANED_DATA_FOLDER']}/{filename}", 'w', encoding='utf-8') as json_file:
        json.dump(req.get('data'), json_file, ensure_ascii=False)

    if (err := json_to_csv(filename)) is not None:
        return res.iserr('Something went wrong', err)

    if (err := save_to_db(req)) is not None:
        return res.iserr('Something went wrong', err)

    err = save_to_db(req)

    if err is not None:
        return res.iserr('Something went wrong.', err)

    return redirect(url_for('export_data'))

if __name__ == '__main__':
    """
    Run the Flask application.

    This function starts the Flask application. It sets the host to '0.0.0.0',
    which means the application will listen on all available network interfaces.
    The port is set to 8080. The debug mode is determined by the value of the
    environment variable 'IS_DEV'. If 'IS_DEV' is set to 'True' or 'true',
    the application will run in debug mode.

    Note:
        This function should only be called if the module is run as the main
        module.
    """
    app.run(host='0.0.0.0', port=8080, debug=os.getenv('IS_DEV') or False)
