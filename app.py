from flask import Flask, render_template, request, redirect, url_for, g, session, make_response
import sqlite3
import hashlib

app = Flask(__name__)

DATABASE = 'movies.db'

app.secret_key = 'super_secret_random_key_here'


################################################################
################################################################
###################### SET COOKIES #############################
################################################################
################################################################


# getting cookie from the previous set_cookie code
@app.route('/getcookie')
def getcookie():
    GFG = request.cookies.get('GFG')
    return 'GFG is a '+ GFG

################################################################
################################################################
###################### Update Movie ############################
################################################################
################################################################


def updateMovie(id, title, genre, director, rating, date):
    # Connecting to the database
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('UPDATE movies SET title = ?, genre = ?, director = ?, rating = ?, date = ? WHERE id = ?',(title, genre, director, rating, date, id))
    connection.commit()
    connection.close()  

################################################################
################################################################
################################################################
######################### GET DATABASE #########################
################################################################
################################################################
################################################################

# Get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

################################################################
################################################################
################################################################
############################ QUERY DB ##########################
################################################################
################################################################
################################################################

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
################################################################
################################################################
################################################################
@app.route("/")

@app.route("/home")
def home():
    if "user_id" in session:
        
        return render_template('index.html')
    
    return render_template('visitor.html')



def sessionCheck():
    if "user_id" not in session:
        return render_template('redirect.html')


################################################################
################################################################
################################################################
###################### ADD CONFIRM #############################
################################################################
################################################################
################################################################
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
################################################################
################################################################

@app.route("/add", methods=["GET", "POST"])
def addMovie():

    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()
    
    if "user_id" not in session:
        return render_template('redirect.html')

    else:    

        user_id = session["user_id"]


        if request.method == "POST":

            # Grabbing form fields matching your HTML 'name' attributes
            title = request.form["title"]
            genre = request.form["genre"]
            director = request.form["director"]
            rating = request.form["rating"]
            date = request.form["date"]

            # Running the exact insert query matching your database table layout
            cursor.execute(
                "INSERT INTO movies (title, genre, director, rating, date, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (title, genre, director, rating, date, user_id)
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
################################################################
################################################################
################################################################



@app.route("/view", methods=["GET", "POST"])
def viewMovie():  
    
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()

    if "user_id" not in session:
        return render_template('redirect.html')

    else:
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
################################################################
################################################################
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
    cursor.execute("SELECT * FROM movies WHERE movie_id = ?",(id,))
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
################################################################
################################################################
################################################################
################################################################


@app.route("/delete/<int:id>", methods=["POST"])
def deleteMovie(id):

    if request.form['submit'] == 'delete':

            connection = sqlite3.connect("movies.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM movies WHERE movie_id = ?", (id,))
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
################################################################
################################################################
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
################################################################
################################################################
################################################################
################################################################


@app.route('/chooseGenre', methods=['POST'])

def chooseGenre():

    genre = request.form.get("genre")

    sql = "SELECT * FROM movies WHERE genre = ?" 
    movies = query_db(sql, (genre,))

    print(movies)

    return render_template('view.html', movies=movies)


################################################################
################################################################
################################################################
##################### SORT RATINGS #############################
################################################################
################################################################
################################################################
################################################################
################################################################


@app.route('/sortRatings', methods=['POST'])



def sortRatings():

    rating = request.form.get("rating")

    if rating == "high":

        sql = "SELECT * FROM movies ORDER BY rating DESC" 

    elif rating == "low":
        
        sql = "SELECT * FROM movies ORDER BY rating ASC" 


    movies = query_db(sql)

    print(movies)

    return render_template('view.html', movies=movies)


################################################################
################################################################
################################################################
##################### SORT DATES ###############################
################################################################
################################################################
################################################################
################################################################

 

@app.route('/sortDates', methods=['POST'])

def sortDates():

    date = request.form.get("date")

    if date == "newest":

        sql = "SELECT * FROM movies ORDER BY date DESC" 

    elif date == "oldest":
        
        sql = "SELECT * FROM movies ORDER BY date ASC" 


    movies = query_db(sql)

    print(movies)

    return render_template('view.html', movies=movies)

################################################################
################################################################
################################################################
################################################################
################################################################
#####################  Email Validation #######################
################################################################
################################################################
################################################################
################################################################


def emailValidation(email):

    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()

    if request.form["email"]:

        email = request.form["email"].strip()

        cursor.execute("SELECT email FROM users WHERE email = ?", (email,)) # compares the email user types to the existing ones in the table
        rows = cursor.fetchone() # Checks one specific email

        if rows:
            return "Email Already Exists"
        else:
            return None



################################################################
################################################################
################################################################
################################################################
################################################################
#####################  Password Validation #####################
################################################################
################################################################
################################################################
################################################################


def passwordValidation(password, cpassword):

    if request.form["password"]:

        password = request.form["password"].strip()
        cpassword = request.form["cpassword"].strip()

        if password != cpassword:
            return "Passwords don't match"

        elif len(password) < 6:
            return "Password must be 6 characters"

        elif not any(char.isupper() for char in password ):
            return "Password must have a uppercase letter"
        
        elif not any(char.islower() for char in password ):
            return "Password must have a lowercase letter"

        elif not any(char.isdigit() for char in password ):
            return "Password must have a number"

        elif not any(char in "!@#$%^&*()-_=+[{]};:'\",<.>/?`~" for char in password):
            return "Password must contain a symbol"

        else:
            return None


################################################################
################################################################
################################################################
##################### REGISTER #################################
################################################################
################################################################

@app.route("/registerConfirm")
def registerConfirm():

    return render_template('confirm.html')


@app.route('/register', methods=['GET', 'POST'])
def register():


    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()

    if request.method == "POST":
    
            # Grabbing form fields matching your HTML 'name' attributes
            email = request.form["email"]
            password = request.form["password"]
            cpassword = request.form["cpassword"]

            validationError = passwordValidation(password, cpassword)
            emailCheck = emailValidation(email)

            if validationError:
                return render_template('register.html', error=validationError)

            elif emailCheck:
                return render_template('register.html', error=emailCheck)

            else: 

                # generates alt key
                s = '5gz'

                password_salt = password + s

                # Hashes password
                h = hashlib.sha256(password_salt.encode())

                print(h.hexdigest())
                
            # Running the exact insert query matching your database table layout
                cursor.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, password)
                )

                connection.commit()
                connection.close()  

                return redirect("registerConfirm")


    return render_template('register.html')


        
################################################################
################################################################
################################################################
##################### LOGIN Password Validation ################
################################################################
################################################################





################################################################
################################################################
################################################################
##################### LOGIN ####################################
################################################################
################################################################

def loginValidation():
    return "Invalid Credentials"



@app.route('/login', methods=['POST', "GET"])

def login():
    
    # Connecting to the database
    connection = sqlite3.connect("movies.db")
    cursor = connection.cursor()

    if request.method == "POST":
    
            # Grabbing form fields matching your HTML 'name' attributes
            email = request.form["email"]
            password = request.form["password"]

            # Running the exact insert query matching your database table layout
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password)) 
            
            user = cursor.fetchone() 
            connection.commit()
            connection.close()  

            if user:
                output = "Welcome"
                resp = make_response(output)
                resp.set_cookie('user_id')
                session["user_id"] = request.form["email"]

                return redirect(url_for("home"))
            else:

                #### validation / error message
                loginValid = loginValidation()
                return render_template('login.html', error=loginValid)


    return render_template('login.html')


################################################################
################################################################
################################################################
##################### LOGOUT ###################################
################################################################
################################################################

@app.route('/logout')

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


################################################################
################################################################
################################################################
##################### YOUR MOVIES ##############################
################################################################
################################################################


@app.route('/userMovies')

def userMovies():

    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()

    if "user_id" not in session:
        return render_template('redirect.html')


    logged_user = session["user_id"]

    cursor.execute("SELECT * FROM movies WHERE user_id = ?", (logged_user,))
    movies_data = cursor.fetchall()

    connection.close()

    return render_template("userMovies.html", movies=movies_data)





################################################################
################################################################
################################################################
##################### DEBUGGING ################################
################################################################
################################################################



if __name__ == '__main__':  
    # Debug mode is now fully activated to catch any sneaky issues
     app.run(debug=True)
