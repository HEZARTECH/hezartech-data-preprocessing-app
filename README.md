# Hezartech Data Labeling Tool

A data labeling tool written in Flask.
Created for Teknofest 2024 Turkish Natural Language Processing Competition.

# Table of Contents

- Installation
- Usage
- Features
- License
- Libraries
- Recommendation
- Screenshots
- Folder Structure

## Installation

1. Clone the repository and Change Directory

```sh
$ git clone https://github.com/HEZARTECH/hezartech-data-preprocessing-app
# or
$ gh repo clone HEZARTECH/hezartech-data-preprocessing-app
#and
$ cd hezartech-data-preprocessing-app
```
2. Install the required dependencies

```sh
# Note: you can try `pip3` if `pip` is not working for you.
$ pip install -r requirements.txt
```

3. Set up the environment variables

```sh
# Note: you can try `python3` if `python` is not working for you.
$ python scripts/make_dotenv.py # please just press enter for all inputs
```

Note: we have a guest account for database:

```txt
Email: misafir@hezartech.com
Password: deneme123
```

P.S: You will se that when `make_dotenv.py` finished. ;)

But if you want to create a new user you can use simply:

```sh
$ python utils.py # It'll call the method from scripts/make_user.py
```

4. Run the application

```sh
$ python app.py
```

5. If you want to use as desktop app:

```sh
$ python desktop.py
```

## Usage

1. Upload a dataset

2. Clean the dataset

3. Label the dataset

4. Export the labeled dataset

## Features

- Upload a data file
- Clean the data
- Label the dataset with NER based labelling editor.
- Export the just claned/cleaned and labeled dataset.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/LICENSE.md) file for details.

## Recommendation

If you want to look to the important files, here is a list:

```sh
./scripts/make_dotenv.py
./scripts/make_user.py
./app.py
./utils.py
./desktop.py
```

And if you want to try system with example data file.
You can use the `example_upload_file/TurknetDestek.csv`.

## Libraries

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/)
- [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/)
- [MongoDB](https://www.mongodb.com/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)
- [PyWebView](https://pywebview.flowrl.com/)
- [Pandas](https://pandas.pydata.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
- [Python-Dotenv](https://pypi.org/project/python-dotenv/)
- [Bcrypt](https://pypi.org/project/bcrypt/)
- [PwInput](https://pypi.org/project/pwinput/)

## Screenshots

### Login Screen

![Login Screen](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/login.png)

### Index / Homepage Screen

![Homepage Screen](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/homepage.png)

### Upload Dataset

![Upload Dataset](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/upload_dataset.png)

### Clean Dataset

![Clean Dataset](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/clean_dataset.png)

### Label Dataset

![Label Dataset](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/label_dataset.png)

### Label Dataset Editor

![Label Dataset Editor](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/label_dataset_editor.png)

### Export Dataset

![Export Dataset](https://github.com/HEZARTECH/hezartech-data-preprocessing-app/blob/main/screenshots/export_dataset.png)


## Folder Structure
```sh
.
├── app.py # Main app file
├── desktop.py # Webview desktop app
├── LICENSE.md # our apps LICENSE
├── README.md # This file
├── requirements.txt # for install required libraries
├── responses.py # For `app.py`
├── screenshots # For `README.md`
│  ├── clean_dataset.png
│  ├── export_dataset.png
│  ├── homepage.png
│  ├── label_dataset.png
│  ├── label_dataset_editor.png
│  ├── login.png
│  └── upload_dataset.png
├── scripts # For setup
│  └── make_dotenv.py
├── static # For `app.py`
│  ├── css
│  │  └── login.css
│  ├── HEZARTECH.png
│  ├── HEZARTECH_HORIZONTAL.png
│  ├── js
│  │  └── label_editor.js
│  ├── robots.txt
│  └── uploads # Exaple uploads
│     ├── 20240622172322_sikayet_var.csv
│     └── clean_data
│        ├── 20240622172322_sikayet_var.csv
│        ├── 20240622172322_sikayet_var.json
│        └── 20240622172322_sikayet_var.xlsx
├── templates # For `app.py`
│  ├── base.html
│  ├── clean_dataset.html
│  ├── export_dataset.html
│  ├── index.html
│  ├── label_dataset.html
│  ├── label_dataset_editor.html
│  ├── login.html
│  └── upload_dataset.html
├── utils.py # For `app.py`
└── wsgi.py # Alternate to `app.py` import app variable from `app.py` and run the server.
```
