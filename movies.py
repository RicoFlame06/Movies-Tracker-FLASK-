import sqlite3

# This connects to 'contacts.db' and creates the correct columns
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()






command1 = """
CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT, 
    genre TEXT, 
    director TEXT,
    rating INTEGER,
    date TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
"""

command2 = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT, 
    password TEXT

)
"""

cursor.execute(command1)
cursor.execute(command2)


connection.commit()
connection.close()

