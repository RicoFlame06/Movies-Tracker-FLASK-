from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'movies.db'

def updateMovie(id, title, genre, director, rating, date):
    # Connecting to the database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('UPDATE movies SET title = ?, genre = ?, director = ?, rating = ?, date = ? WHERE id = ?',(title, genre, director, rating, date, id))
    connection.commit()
    connection.close()  


# Get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# Fetch all rows in database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

################################################################
################################################################
################################################################
###################### INDEX  ##################################
################################################################
################################################################

@app.route("/")
def home():
    return render_template('index.html')

################################################################
################################################################
################################################################
###################### ADD CONFIRM #############################
################################################################
################################################################

@app.route("/addConfirm")
def addConfirmation():

    return render_template('addConfirmation.html')

################################################################
################################################################
################################################################
######################## ADD MOVIE #############################
################################################################
################################################################

@app.route("/add", methods=["GET", "POST"])
def addMovie():

    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()

    if request.method == "POST":
        # Grabbing form fields matching your HTML 'name' attributes
        title = request.form["title"]
        genre = request.form["genre"]
        director = request.form["director"]
        rating = request.form["rating"]
        date = request.form["date"]



        # Running the exact insert query matching your database table layout
        cursor.execute(
            "INSERT INTO movies (title, genre, director, rating, date) VALUES (?, ?, ?, ?, ?)",
            (title, genre, director, rating, date)
        )

        connection.commit()
        connection.close()  

        return redirect("addConfirm")


    return render_template('add.html')


################################################################
################################################################
################################################################
##################### VIEW MOVIES ##############################
################################################################
################################################################



@app.route("/view", methods=["GET", "POST"])
def viewMovie():  
    
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM movies")
    movies_data = cursor.fetchall()

    connection.close()

    return render_template("view.html", movies=movies_data)


################################################################
################################################################
################################################################
##################### EDIT MOVIES ##############################
################################################################
################################################################


@app.route("/updateMovie/<int:id>", methods=["POST", "GET"])

def editMovie(id):

    if request.method == "POST":

        # Grabbing form fields matching your HTML 'name' attributes
        title = request.form["title"]
        genre = request.form["genre"]
        director = request.form["director"]
        rating = request.form["rating"]
        date = request.form["date"]

        updateMovie(id, title, genre, director, rating, date)

        return redirect(url_for("viewMovie"))

    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies WHERE id = ?",(id,))
    movies_data = cursor.fetchone()
    print(movies_data)

    connection.commit()
    connection.close()

    
    return render_template("edit.html", movie=movies_data)


################################################################
################################################################
################################################################
##################### DELETE MOVIES ############################
################################################################
################################################################

@app.route("/delete/<int:id>", methods=["POST"])
def deleteMovie(id):

    if request.form['submit'] == 'delete':

            connection = sqlite3.connect("movies.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM movies WHERE id = ?", (id,))
            connection.commit()
            connection.close()

            return redirect(url_for("viewMovie"))
    
    return render_template("view.html")

################################################################
################################################################
################################################################
##################### SEARCH MOVIES ############################
################################################################
################################################################

@app.route("/search", methods=["GET"])
def searchMovie():

    searchValue = request.args.get('searchMovie', '').strip()

    if searchValue:

        sql = "SELECT * FROM movies WHERE title LIKE ? OR genre LIKE ? OR director LIKE ?" 
        wildcardSearch = f"%{searchValue}%"

        movies = query_db(sql, (wildcardSearch, wildcardSearch, wildcardSearch))

        return render_template('search.html', movies=movies, query=searchValue)
    else:
        return render_template('search.html')


################################################################
################################################################
################################################################
##################### CHOOSE GENRE #############################
################################################################
################################################################

@app.route('/chooseGenre', methods=['POST'])

def chooseGenre():

    genre = request.form.get("genre")

    sql = "SELECT * FROM movies WHERE genre = ?" 
    movies = query_db(sql, (genre,))

    print(movies)

    return render_template('view.html', movies=movies)







if __name__ == '__main__':  
    # Debug mode is now fully activated to catch any sneaky issues
     app.run(debug=True)
