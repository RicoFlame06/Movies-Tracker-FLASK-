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




cursor.execute("INSERT INTO movies (title, genre, director, rating, date) VALUES('Spider-man Brand New Day', 'Action', 'Destin Daniel Cretton', 4, '29-07-26')")

cursor.execute("SELECT * FROM movies")
movies = cursor.fetchall()
for movie in movies:
    print(movies)


cursor.execute(command1)
connection.commit()
connection.close()

