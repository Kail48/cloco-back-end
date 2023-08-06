# Flask Project Name

A simple Flask project for managing artists.

![Project Demo](demo.gif) <!-- Replace with a link to your project demo video or GIF -->

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

## Installation

To run this project locally, follow these steps:

1. Clone this repository: `git clone https://github.com/your-username/task-tracker.git`
2. Navigate to the project directory: `cd task-tracker`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install project dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`

## Usage

1. Start the application: `python app.py`
2. Open your web browser and go to: `http://localhost:5000`
3. Register a new user account or log in if you already have one.
4. Use the interface to add, edit, and manage your tasks.



