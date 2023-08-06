import sqlite3
DATABASE_NAME="cloco_db" #is to be used across the app to connect to database
def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(500) NOT NULL,
        is_admin BOOLEAN NOT NULL,
        phone VARCHAR(20) NOT NULL,
        dob DATETIME NOT NULL,
        gender TEXT CHECK(gender IN ('M', 'T', 'O')) NOT NULL,
        address VARCHAR(255) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME);
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS artist(
        id INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
        name VARCHAR(255)NOT NULL,
        dob DATETIME NOT NULL,
        gender TEXT CHECK(gender IN ('M', 'T', 'O')) NOT NULL,
        address VARCHAR(255) NOT NULL,
        first_release_year SMALLINT NOT NULL,
        number_of_albums_released INT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME
        );

        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS music(
        artist_id VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        album_name VARCHAR(255) NOT NULL,
        genre TEXT CHECK(genre IN ('rnb', 'jazz', 'country', 'rock', 'classic')) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME ,
        FOREIGN KEY(artist_id) REFERENCES artist(id)
        );
        """
    )
    conn.commit()
    conn.close()
    
initialize_database()
