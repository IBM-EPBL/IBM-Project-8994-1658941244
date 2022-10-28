from flask import Flask, render_template, redirect, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__,template_folder="template")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gibsqbxqelvght:bd2af40fd3a7372a4da33e7090e7606349d24f661df710450123851701b84fe8@ec2-44-209-186-51.compute-1.amazonaws.com:5432/dcrlivg5r4ajd1'
app.config['SECRET_KEY'] = 'mysecret'

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db = scoped_session(sessionmaker(bind = engine))


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.execute("SELECT * FROM users where username = :username and password = :password", {
          "username": username,
          "password": password
        }).fetchone()

        if user == None:
          return "<h1 style = 'color: red'> Invalid username or password </h1>"
        
        session['user'] = user.username
        return redirect('dashboard')
    else:
        return render_template("signin.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
      return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
      return "<h1 style = 'color: red'> Passwords dont match </h1>"

    if db.execute("SELECT id from users where username = :username", {"username" : username}).fetchone() != None:
      return "<h1 style = 'color: red'> Username not available </h1>"

    db.execute("insert into users (username, password) values (:username, :password)", {
      "username": username,
      "password": password
    })
    db.commit()

    session['user'] = username
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
  return render_template("dashboard.html")


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')