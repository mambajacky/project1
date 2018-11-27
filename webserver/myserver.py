
"""
Columbia W4111 Intro to databases
Example webserver
To run locally
    python server.py
Go to http://localhost:8111 in your browser
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)



# XXX: The Database URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@<IP_OF_POSTGRE_SQL_SERVER>/<DB_NAME>
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@<IP_OF_POSTGRE_SQL_SERVER>/postgres"
#
# For your convenience, we already set it to the class database

# Use the DB credentials you received by e-mail
DB_USER = "yf2433"
DB_PASSWORD = "y5l475f5"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
#
# This is a home page.  You can see it at
# 
#     localhost:8111/
#
# You can visit other pages with the links in the home page
#
@app.route('/')
def home():
  return render_template("home.html")
    

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/users
#
# notice that the function name is users() rather than home()
# the functions for each app.route needs to have different names
#
@app.route('/users')
def users():
  """
  request is a special object that Flask provides to access web request information:
  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2
  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  # print request.args


  #
  # fetch data from Users_Live table
  #
  cursor = g.conn.execute("SELECT * FROM Users_Live")
  uid = []
  uname = []
  email_address = []
  password = []
  gender = []
  state = []
  city = []
  street_name = []
  street_number = []
  for result in cursor:
    uid.append(result['uid'])  # can also be accessed using result[0]
    uname.append(result['uname'])
    email_address.append(result['email_address'])
    password.append(result['password'])
    gender.append(result['gender'])
    state.append(result['state'])
    city.append(result['city'])
    street_name.append(result['street_name'])
    street_number.append(result['street_number'])
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/users.html
  #
  # context are the variables that are passed to the template.
  # for example, "data1" key in the context variable defined below will be 
  # accessible as a variable in users.html:
  #
  context = dict(data1 = uid, data2 = uname, data3 = email_address, data4 = password, 
              data5 = gender, data6 = state, data7 = city, data8 = street_name, data9 = street_number)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/users.html
  #
  return render_template("users.html", **context)


#
# This is a different path.  You can see it at
# 
#     localhost:8111/votes
#
@app.route('/participants')
def participants():
  cursor = g.conn.execute("SELECT * FROM Participate_Vote_Events")
  uid = []
  eid = []
  rating = []
  birth_date = []
  interest = []

  for result in cursor:
    uid.append(result['uid'])  # can also be accessed using result[0]
    eid.append(result['eid'])
    rating.append(result['rating'])
    birth_date.append(result['birth_date'])
    interest.append(result['interest'])
  cursor.close()

  context = dict(data1 = uid, data2 = eid, data3 = rating, data4 = birth_date, data5 = interest) 

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/participants.html
  #
  return render_template("participants.html", **context)


@app.route('/locations')
def locations():
  cursor = g.conn.execute("SELECT * FROM Locations")
  state = []
  city = []
  street_name = []
  street_number = []

  for result in cursor:
    state.append(result['state'])  # can also be accessed using result[0]
    city.append(result['city'])
    street_name.append(result['street_name'])
    street_number.append(result['street_number'])
  cursor.close()

  context = dict(data1 = state, data2 = city, data3 = street_name, data4 = street_number) 

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/locations.html
  #
  return render_template("locations.html", **context)


@app.route('/organizers')
def organizers():
  cursor = g.conn.execute("SELECT * FROM Organize_Events")
  uid = []
  eid = []

  for result in cursor:
    uid.append(result['uid'])  # can also be accessed using result[0]
    eid.append(result['eid'])
  cursor.close()

  context = dict(data1 = uid, data2 = eid) 

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/organizers.html
  #
  return render_template("organizers.html", **context)


@app.route('/events')
def events():
  cursor = g.conn.execute("SELECT * FROM Events_TakePlace_Belong_Organize")
  eid = []
  cost = []
  date = []
  ename = []
  smallest_age = []
  category = []
  uid = []
  state = []
  city = []
  street_name = []
  street_number = []

  for result in cursor:
    eid.append(result['eid'])  # can also be accessed using result[0]
    cost.append(result['cost'])
    date.append(result['date'])
    ename.append(result['ename'])
    smallest_age.append(result['smallest_age'])
    category.append(result['category'])
    uid.append(result['uid'])
    state.append(result['state'])
    city.append(result['city'])
    street_name.append(result['street_name'])
    street_number.append(result['street_number'])
  cursor.close()

  context = dict(data1 = eid, data2 = cost, data3 = date, data4 = ename, data5 = smallest_age, data6 = category, 
                 data7 = uid, data8 = state, data9 = city, data10 = street_name, data11 = street_number) 

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/events.html
  #
  return render_template("events.html", **context)


#
# Adding new data to the database. 
# 
@app.route('/adduser', methods=['POST'])
def adduser():
  try:
    uid = request.form['uid']
    uname = request.form['uname']
    email_address = request.form['email_address']
    password = request.form['password']
    gender = request.form['gender']
    state = request.form['state']
    city = request.form['city']
    street_name = request.form['street_name']
    street_number = request.form['street_number']
    cmd = "INSERT INTO Users_Live(uid, uname, email_address, password, gender, state, city, street_name, street_number)  \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    g.conn.execute(cmd, (uid, uname, email_address, password, gender, state, city, street_name, street_number))
    return redirect('/users')
  except:
    #raise ValueError("bad input, please try again.")
    return redirect('/users')

@app.route('/selectuser', methods=['POST'])
def selectuser():
  target = request.form['target']
  value = request.form['search']
  if target == "uid":
    cmd = "SELECT * FROM Users_Live WHERE uid = %s;"
  elif target == "uname":
    cmd = "SELECT * FROM Users_Live WHERE uname = %s;"
  elif target == "gender":
    cmd = "SELECT * FROM Users_Live WHERE gender = %s;"
  else:
    raise ValueError("Please use another target attribute.")
  cursor = g.conn.execute(cmd, (value))
  uid = []
  uname = []
  email_address = []
  password = []
  gender = []
  state = []
  city = []
  street_name = []
  street_number = []
  for result in cursor:
    uid.append(result['uid'])  # can also be accessed using result[0]
    uname.append(result['uname'])
    email_address.append(result['email_address'])
    password.append(result['password'])
    gender.append(result['gender'])
    state.append(result['state'])
    city.append(result['city'])
    street_name.append(result['street_name'])
    street_number.append(result['street_number'])
  cursor.close()

  context = dict(data1 = uid, data2 = uname, data3 = email_address, data4 = password, 
              data5 = gender, data6 = state, data7 = city, data8 = street_name, data9 = street_number)

  return render_template("selectedusers.html", **context)


@app.route('/addlocation', methods=['POST'])
def addlocation():
  try:
    state = request.form['state']
    city = request.form['city']
    street_name = request.form['street_name']
    street_number = request.form['street_number']
    cmd = "INSERT INTO Locations(state, city, street_name, street_number) VALUES (%s, %s, %s, %s);"
    g.conn.execute(cmd, (state, city, street_name, street_number))
    return redirect('/locations')
  except:
    return redirect('/locations')

@app.route('/addevent', methods=['POST'])
def addevent():
  try:
    eid = request.form['eid']
    cost = request.form['cost']
    date = request.form['date']
    ename = request.form['ename']
    smallest_age = request.form['smallest_age']
    category = request.form['category']
    uid = request.form['uid']
    state = request.form['state']
    city = request.form['city']
    street_name = request.form['street_name']
    street_number = request.form['street_number']
    cmd = "INSERT INTO Events_TakePlace_Belong_Organize(eid, cost, date, ename, smallest_age, category, uid, state, city, street_name, street_number)  \
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    g.conn.execute(cmd, (eid, cost, date, ename, smallest_age, category, uid, state, city, street_name, street_number))
    return redirect('/events')
  except:
    return redirect('/events')

@app.route('/selectevent', methods=['POST'])
def selectevent():
  target = request.form['target']
  value = request.form['search']
  if target == "eid":
    cmd = "SELECT * FROM Events_TakePlace_Belong_Organize WHERE eid = %s;"
  elif target == "ename":
    cmd = "SELECT * FROM Events_TakePlace_Belong_Organize WHERE ename = %s;"
  elif target == "state":
    cmd = "SELECT * FROM Events_TakePlace_Belong_Organize WHERE state = %s;"
  else:
    raise ValueError("Please use another target attribute.")
  cursor = g.conn.execute(cmd, (value))
  eid = []
  cost = []
  date = []
  ename = []
  smallest_age = []
  category = []
  uid = []
  state = []
  city = []
  street_name = []
  street_number = []

  for result in cursor:
    eid.append(result['eid'])  # can also be accessed using result[0]
    cost.append(result['cost'])
    date.append(result['date'])
    ename.append(result['ename'])
    smallest_age.append(result['smallest_age'])
    category.append(result['category'])
    uid.append(result['uid'])
    state.append(result['state'])
    city.append(result['city'])
    street_name.append(result['street_name'])
    street_number.append(result['street_number'])
  cursor.close()

  context = dict(data1 = eid, data2 = cost, data3 = date, data4 = ename, data5 = smallest_age, data6 = category, 
                 data7 = uid, data8 = state, data9 = city, data10 = street_name, data11 = street_number) 

  return render_template("selectedevents.html", **context)

@app.route('/participate', methods=['POST'])
def participate():
  try:
    uid = request.form['uid']
    eid = request.form['eid']
    rating = request.form['rating']
    birth_date = request.form['birth_date']
    interest = request.form['interest']
    cmd = "INSERT INTO Participate_Vote_Events(uid, eid, rating, birth_date, interest) VALUES (%s, %s, %s, %s, %s);"
    g.conn.execute(cmd, (uid, eid, rating, birth_date, interest))
    return redirect('/participants')
  except:
    return redirect('/participants')

@app.route('/organize', methods=['POST'])
def organize():
  try:
    uid = request.form['uid']
    eid = request.form['eid']
    cmd = "INSERT INTO Organize_Events(uid, eid) VALUES (%s, %s);"
    g.conn.execute(cmd, (uid, eid))
    return redirect('/organizers')
  except:
    return redirect('/organizers')

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
