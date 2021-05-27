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
    msg=""
    msg2=""
    if request.method == 'GET':
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM buggies")
            prev_id = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            
            cur.execute("SELECT qty_wheels FROM buggies")
            prev_qty_wheels = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            
            cur.execute("SELECT flag_color FROM buggies")
            prev_flag_color = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            
            cur.execute("SELECT flag_color_secondary FROM buggies")
            prev_flag_color_secondary = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            
            cur.execute("SELECT flag_pattern FROM buggies")
            prev_flag_pattern = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            
            prev_form_store = [prev_id, prev_qty_wheels, prev_flag_color, prev_flag_color_secondary, prev_flag_pattern]
            for i in range(0, len(prev_form_store)):
                if prev_form_store[i] != "''":
                    prev_form_store[i] = prev_form_store[i].replace("'","")
                else:
                    prev_form_store[i] = "None"
            return render_template("buggy-form.html", prev_id=int(prev_form_store[0]), prev_qty_wheels=int(prev_form_store[1]), prev_flag_color=prev_form_store[2], prev_flag_color_secondary=prev_form_store[3], prev_flag_pattern=prev_form_store[4])
    elif request.method == 'POST':
        msg = ""
        msg2 = ""
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        
        form_store = [qty_wheels, flag_color, flag_color_secondary, flag_pattern]
       
        
        for i in range(0, len(form_store)):
            if form_store[i] == "":
                msg = "Insert the text in all the fields"
        if  not request.form["qty_wheels"].strip().isdigit():
            msg += f"Oh noes, that is not a number: {qty_wheels}"
        if int(qty_wheels) in range(0,4):
            msg += "Oh noes, the number of wheels can't be less than 4!"
        if flag_color.strip().isdigit():
            msg2 = f"Oh noes, that is not a text: {flag_color}"
        elif flag_color_secondary.strip().isdigit():
            msg2 = f"Oh noes, that is not a text: {flag_color_secondary}"
        elif flag_pattern.strip().isdigit():
            msg2 = f"Oh noes, that is not a text: {flag_pattern}"
        if msg != "" or msg2 != "":
            return render_template("buggy-form.html", prev_qty_wheels=qty_wheels, prev_flag_color=flag_color, prev_flag_color_secondary=flag_color_secondary, prev_flag_pattern=flag_pattern, msg=msg, msg2=msg2)
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE buggies SET qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=? WHERE id=?",
                    (qty_wheels, flag_color, flag_color_secondary, flag_pattern, DEFAULT_BUGGY_ID)
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
