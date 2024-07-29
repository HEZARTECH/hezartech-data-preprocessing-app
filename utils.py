#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yiğit GÜMÜŞ

This module contains utility functions for this project.
And bring functionality to the backend of this project.

Constants:
    ALLOWED_EXTENSIONS: The allowed file extensions.
    UPLOAD_FOLDER: The upload folder.
    CLEANED_DATA_FOLDER: The cleaned data folder.

Variables:
    templates: A dictionary containing key-value pairs of template names.
    db: The MongoDB database.
    client: The MongoDB client.

Functions:
    set_folders:
        Sets the global variables UPLOAD_FOLDER and CLEANED_DATA_FOLDER to the
        provided `upload_folder` and `cleaned_data_folder` respectively.

    register_user_to_db:
        Registers a new user to the database.

    find_user_via_email:
        Finds a user in the database based on their email.

    set_session_user:
        Sets the user ID in the session.

    get_session_property:
        Gets the value of a property in the session.

    allowed_file:
        Checks if the given filename is allowed based on the file extension.

    cleaned_data_folder_is_file:
        Checks if a file with the given name exists in the cleaned data folder.

    upload_folder_is_file:
        Checks if a file with the given name exists in the upload folder.

    turkish_characters:
        Translates Turkish characters in the given text to their English counterparts.

    set_template_names:
        Sets the global variable `templates` with the provided dictionary.

    get_template_name:
        Returns the template name for a given page. It gives data from
        `templates` variable.

    remove_file_extensions:
        Removes the file extensions from a list of file names.

    csv_to_xlsx:
        Converts a CSV file to an XLSX file.

    extract_text_and_ids_from_dataset:
        Extracts the 'id' and 'text' columns from a dataset file and returns them as a list of tuples.

"""

# For backend
from flask import (
    session,

    redirect,
    url_for,
    render_template,

    Response
)
import pymongo
import bcrypt
import re

# For .xlsx, .csv and .json file manipulation
import pandas as pd
import openpyxl
import csv
import json

# Default libraries
import os
from typing import Any, Optional

# Our repository code (responses.py)
from responses import Responses as res
from bson.objectid import ObjectId

# For database connection and dotenv file
__import__('dotenv').load_dotenv()
import certifi
client = pymongo.MongoClient(os.getenv('DB_URI') + '?retryWrites=true&w=majority', authsource='admin', tlsCAFile=certifi.where())
db = client.get_database('hezartech')

templates: dict[str, Any] = dict()

# FOR FILE UPLOAD AND THEIR MIDDLEWARES
ALLOWED_EXTENSIONS: set = {'csv', 'xlsx'}
UPLOAD_FOLDER: str = ''
CLEANED_DATA_FOLDER: str = ''


def set_folders(upload_folder, cleaned_data_folder) -> None:
    """
    Sets the global variables `UPLOAD_FOLDER` and `CLEANED_DATA_FOLDER` to the
    provided `upload_folder` and `cleaned_data_folder` respectively.

    Parameters:
        upload_folder (str): The path to the upload folder.
        cleaned_data_folder (str): The path to the cleaned data folder.

    Returns:
        None
    """

    global UPLOAD_FOLDER, CLEANED_DATA_FOLDER

    UPLOAD_FOLDER = upload_folder
    CLEANED_DATA_FOLDER = cleaned_data_folder


def allowed_file(filename: str) -> bool:
    """
    Check if the given filename is allowed based on the file extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleaned_data_folder_is_file(filename: str) -> bool:
    """
    Check if a file with the given name exists in the cleaned data folder.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    return os.path.isfile(CLEANED_DATA_FOLDER+'/'+filename)

def upload_folder_is_file(filename: str) -> bool:
    """
    Check if a file with the given name exists in the upload folder.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    return os.path.isfile(UPLOAD_FOLDER+'/'+filename)

def get_session_property(property_name: str) -> str | None:
    """
    Gets the value of a property in the session.

    Args:
        property_name (str): The name of the property.

    Returns:
        str | None: The value of the property if it exists in the session,
                    otherwise None.
    """

    return session.get(property_name)

def set_template_names(_template: dict[str, str]) -> None:
    """
    Set the global variable `templates` with the provided dictionary.

    Args:
        _template (dict[str, str]): A dictionary containing key-value pairs of template names.

    Returns:
        None
    """

    global templates
    templates = _template

def get_template_name(page_name: str) -> str:
    """
    Returns the template name for a given page.

    Args:
        page_name (str): The name of the page.

    Returns:
        str: The template name for the given page.

    """

    return templates.get(page_name)

def set_session_user(user_id: ObjectId, email: str, name: str) -> None:
    """
    Sets the user ID in the session.

    Args:
        user_id (ObjectId): The ID of the user (mongodb uses object_id for id seralization).
        email (str): The email of the user.
        name (str): Fullname of user.
    Returns:
        None
    """
    session['user_id'] = str(user_id)
    session['email'] = email
    session['name'] = name

def register_user_to_db(name: str, email: str, password: str) -> None:
    """
    Registers a new user to the database.

    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db.users.insert_one({
        'name': name,
        'email': email,
        'password': hashed_password
    })


def find_user_via_email(email: str) -> dict[str, str] | None:
    """
    Finds a user in the database based on their email.

    Args:
        email (str): The email of the user.

    Returns:
        dict[str, str] | None: The user document if found, or None if not found.
    """

    return db.users.find_one({
        'email': email
    })

def login_required_render_template(template_name: str, **kwargs) -> Response:
    """
    A function that checks if the user is logged in and renders a template after that.

    Args:
        template_name (str): The name of the template to render.
        **kwargs: Additional keyword arguments to pass to the template.

    Returns:
        Response: The rendered template if the user is logged in, otherwise a redirect to the login page.
    """

    if session.get('user_id') is None:
        return redirect(url_for('login'))

    return render_template(template_name, session_user=session, **kwargs)


def turkish_characters(text: str) -> str:
    """
    Translates Turkish characters in the given text to their English counterparts.

    Args:
        text (str): The text containing Turkish characters.

    Returns:
        str: The text with Turkish characters replaced by their English counterparts.
    """

    return text.translate(str.maketrans("ğĞıİöÖüÜşŞçÇ", "gGiIoOuUsScC"))

def clean_text(text: str) -> str:
    """
    Cleans the given text by performing the following operations:
    1. Converts the text to lowercase.
    2. Removes words containing '#' or '@'.
    3. Removes URLs, mentions, and hashtags.
    4. Removes non-alphanumeric characters and extra whitespace.
    5. Removes digits.

    Parameters:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """

    text = str(text).lower()
    text = " ".join([word for word in text.split() if '#' not in word and '@' not in word])
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    text = re.sub(r'''
                   \W+
                   \s*
                   ''',
                  ' ',
                  text,
                  flags=re.VERBOSE)
    text = re.sub(r"\d+", "", text)
    return text

def csv_to_xlsx(filename: str) -> Response:
    """
    Convert a CSV file to an XLSX file.

    Args:
        filename (str): The name of the CSV file to convert.

    Returns:
        Response: The response object.

    Raises:
        FileNotFoundError: If the CSV file is not found.

    """

    wb = openpyxl.Workbook()
    ws = wb.active
    with open(f'static/uploads/clean_data/{filename}', 'r', encoding='utf-8') as file:
        for row in csv.reader(file):
            ws.append(row)
    filename = filename.replace("csv", "xlsx")
    wb.save(f'static/uploads/clean_data/{filename}')

def remove_file_extensions(items: list[str]) -> list[str]:
    """
    Remove the file extensions from a list of file names.

    Args:
        items (list[str]): The list of file names.

    Returns:
        list[str]: The list of file names without extensions.
    """

    return [item.rsplit('.', 1)[0] for item in items]

def extract_text_and_ids_from_dataset(filename: str) -> list[tuple[int, str]]:
    """
    Extracts the 'id' and 'text' columns from a dataset file and returns them as a list of tuples.

    Args:
        filename (str): The name of the dataset file.

    Returns:
        list[tuple[int, str]]: A list of tuples containing the 'id' and 'text' values from the dataset.
    """

    if 'csv' in filename:
        df = pd.read_csv(f'static/uploads/clean_data/{filename}', usecols=['id', 'text'])
    if 'xlsx' in filename:
        df = pd.read_excel(f'static/uploads/clean_data/{filename}', usecols=['id', 'text'])

    df['id'] = df['id'].astype('int64')
    df['text'] = df['text'].astype('string')
    #df['clean_text'] = df['clean_text'].astype('string')


    return list(df.itertuples(index=False, name=None))

def data_cleaner(filename: str) -> Response:
    """
    Cleans the given dataset file and saves the cleaned data to a new file.

    Args:
        filename (str): The name of the dataset file.

    Returns:
        Response: The response object indicating the result of the operation.

    Raises:
        FileNotFoundError: If the DataFrame
    """

    try:
        df: pd.DataFrame = None
        if 'csv' in filename:
            df = pd.read_csv(f'static/uploads/{filename}')
        if 'xslx' in filename:
            df = pd.read_excel(f'static/uploads/{filename}')

        if df is None:
            raise FileNotFoundError("DataFrame is not implemented via files.")

        texts = df.text.apply(turkish_characters) \
                        .apply(clean_text)
        text_list = list(texts)

        df['clean_text'] = text_list

        df.to_csv(f'static/uploads/clean_data/{filename}', index=False)
        csv_to_xlsx(filename)

    except Exception as e:
        return res.iserr('Verilen dataset temizlenirken bir hata meyadana geldi.', e)
    else:
        return redirect(url_for('clean_data'))

def save_to_db(request: dict[str, Any]) -> Optional[Exception]:
    """
    Save the given request dictionary to the database.

    Parameters:
        request (dict[str, Any]): The dictionary containing the data to be saved.

    Returns:
        Optional[Exception]: Returns None if the data is successfully saved to the database,
                                        or an Exception object if an error occurs.
    """

    try:
        db.datasets.insert_one(request)
        return None
    except Exception as err:
        return err

def json_to_csv(filename: str) -> None | Exception:
    """
    Translate labeled JSON file dataset to CSV format.

    Paramaters:
        filename (str): The name of JSON file.

     Returns:
        Optional[Exception]: Returns True if the data is successfully saved to the database,
                                        or an Exception object if an error occurs.
    """
    df_data = {
        'id': [],
        'text': [],
        'company': [],
        'positive': [],
        'negative': [],
        'notr': []
    }

    translate_json = {
        'FIRMA': 'company',
        'POZITIF': 'positive',
        'NEGATIF': 'negative',
        'NOTR': 'notr'
    }

    with open(CLEANED_DATA_FOLDER + '/' + filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)

        for i in data:
            df_data['id'].append(i['page'])
            df_data['text'].append(i['text'])

            temp_data = {
                'company': [],
                'positive': [],
                'negative': [],
                'notr': []
            }
            annotations = i['annotations']

            for x in annotations:
                try:
                    eng_version = translate_json[x['tag']]
                    temp_data[eng_version].append(x['text'])

                except Exception as err:
                    return err
            for b in temp_data:
                if temp_data[b]:
                    del_dup = list(set(temp_data[b]))

                    new_value = '|'.join(del_dup)
                    df_data[b].append(new_value)

                else:
                    df_data[b].append('')
    df = pd.DataFrame(df_data)

    df.to_csv(CLEANED_DATA_FOLDER + '/' + filename.replace('json', 'csv'), index= False)
    return None



if __name__ == '__main__':
    from scripts.make_user import make_user
    make_user()
