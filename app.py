from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        return render_template("buggy-form.html")
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        if not qty_wheels.isdigit():
            msg = f"Oh noes, that is not a number: {qty_wheels}"
            return render_template("buggy-form.html", msg = msg)
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies SET qty_wheels=?, flag_color=? WHERE id=?",
                    (qty_wheels, flag_color, DEFAULT_BUGGY_ID)
                )
                con.commit()
                msg = "Record successfully saved"
        except:
            con.rollback()
            msg = "error in update operation"
        finally:
            con.close()
        return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone(); 
    return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
