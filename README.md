# Flask Project Name

A simple Flask project for managing artists.

![Project Demo(with frontend)](https://cloco-music.netlify.app) 
![Api(with frontend)](https://kailashdev.pythonanywhere.com/) 

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)



## Description

This Flask project provides an api for artist management system. It uses the Flask framework for the backend. Users(admins) can add, edit, and delete artists and their records. The user features haven't been implemented although creation of user accounts is possible through an admin. There is a simplistic jwt authentication implementation for token based authentication. The use of ORM has been completely avoided and the data is stored in sqlite3 database which is manipulated through raw sql queries.

### Why flask?
I chose flask over Django because this project requires pure sql implementation, Using Django without ORM just increases the bundle size of the project specially for small projects like this.

## Features

- Admin registration and authentication
- Add new users as admin(users themselves cannot register)
- Edit existing users and artists
- CSV import and export for artists

## Api Documnetation
[Check full doc](https://documenter.getpostman.com/view/25345798/2s9Xxztryz)

## Installation

To run this project locally, follow these steps:

1. Clone this repository: `git clone https://github.com/Kail48/cloco-back-end.git`
2. Navigate to the project directory: `cd cloco-back-end`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install project dependencies: `pip install -r requirements.txt`
6. Run the script to initialize the database: `python init_db.py`
7. Go into app folder and get your absolute path for the folder called 'uploaded files', paste it into app config upload folder path. 
8. Run the application: `python main.py`

## Usage

1. Start the application: `python main.py`
2. Open your web browser and go to: `http://localhost:5000`





