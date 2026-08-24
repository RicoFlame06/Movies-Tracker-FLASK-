import sqlite3

# This connects to 'contacts.db' and creates the correct columns
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()



command1 = """
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT, 
    genre TEXT, 
    director TEXT,
    rating INTEGER,
    date TEXT
)
"""

command2 = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT, 
    password TEXT

)
"""







cursor.execute(command1)
cursor.execute(command2)

connection.commit()
connection.close()

