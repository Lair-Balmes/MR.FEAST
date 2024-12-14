# Mr. Feast - Share Your Recipes

## Overview

**Mr. Feast** is a GUI-based recipe sharing application built with Python using the `Tkinter` and `customtkinter` libraries. Users can sign up, log in, create posts to share their recipes, and delete their own posts. The app connects to a MySQL database to manage user accounts and recipe data.

---

## Features

- **User Authentication**: Sign up and log in functionality for user accounts.
- **Recipe Posting**: Logged-in users can create posts to share their recipes.
- **Recipe Feed**: View a list of recipes posted by different users.
- **Delete Posts**: Users can delete their own recipes.
- **Search Functionality**: Search recipes by title, description, or ingredients.
- **Drag Functionality**: The window can be dragged around by clicking and holding the mouse.

---

## Requirements

To run the application, you'll need the following dependencies:

- **Python 3.x**
- **MySQL Server** for database operations

### Python Libraries

Install the necessary libraries with pip:

```bash
pip install customtkinter
pip install mysql-connector-python
pip install Pillow
```

---

## Setup

### 1. MySQL Database

Create a MySQL database called `MR_FEASTDB` and the following tables:

```sql
CREATE DATABASE MR_FEASTDB;
USE MR_FEASTDB;

CREATE TABLE user (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    account_date DATETIME NOT NULL
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    post_date DATETIME NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID) ON DELETE CASCADE
);
```

### 2. Update MySQL Credentials

Update the database credentials in `GUI.py` to match your MySQL configuration:

```python
mysql.connector.connect(
    host="YOUR_HOST",
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    database="MR_FEASTDB"
)
```

---

## Running the Application

1. **Start MySQL Server** and ensure your database is set up.
2. **Run the Python script**:

```bash
python GUI.py
```

---

## Usage

- **Sign Up**: Create an account to start sharing recipes.
- **Log In**: Access your account and manage your posts.
- **Post a Recipe**: Share a recipe with a title, description, and ingredients.
- **Delete a Recipe**: Delete any recipe that you posted.
- **Search Recipes**: Use the search bar to find recipes by keywords.

---

## Notes

- **Icons and Images**: Ensure that `MRF_ICON.ico` and `MRF_LOGO.png` are present in the project directory.
- **Database Security**: Passwords are currently stored in plain text. Consider hashing passwords for added security in a production environment.


---

**Happy Cooking! 🍽️**
