from flask import Flask, render_template, request, jsonify, session
from markupsafe import escape
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
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/login', methods=['GET', 'POST'])
def login():
    what = "Log In"
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        usr = session['username']
        psw = session['password']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT password FROM buggies WHERE username=?", (usr,))
                check_psw = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                print(check_psw.replace("'",""))
                if psw == check_psw.replace("'",""):
                    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=usr)
                else:
                    msg = "Wrong Password"
                    return render_template("updated.html", msg = msg)
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
            msg = "error in update operation"
        finally:
            con.close()
        return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=session['username'])
    return render_template('login.html', what=what)

@app.route('/register', methods=['GET', 'POST'])
def register():
    what = "Register"
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        usr = session['username']
        psw = session['password']
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT username FROM buggies")
                check_usr = str(cur.fetchall()).replace(",","").replace("(", "").replace(")","");
                try:
                    if usr not in check_usr:
                        cur.execute("INSERT INTO buggies (username, password) VALUES (?,?)", 
                        (usr, psw)
                        )
                    else:
                        cur.execute(
                        "UPDATE buggies SET username=?, password=?",
                        (usr, psw)
                        )
                except:
                    cur.execute("INSERT INTO buggies (username, password) VALUES (?,?)", 
                    (usr, psw)
                    )
                con.commit()
                msg = "Record successfully saved"
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
            msg = "error in update operation"
        finally:
            con.close()
        return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=session['username'])
    return render_template('login.html', what=what)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    user = "Not Logged!"
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, user=user)

@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# the error page
#------------------------------------------------------------
# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
  return render_template("404.html")

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
            
            try:
                cur.execute("SELECT id FROM buggies")
                prev_id = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_id = int(prev_id)
            except:
                prev_id = 1
            try:    
                cur.execute("SELECT qty_wheels FROM buggies")
                prev_qty_wheels = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_qty_wheels = int(prev_qty_wheels)
            except:
                prev_qty_wheels = 4
            try:
                cur.execute("SELECT tyres FROM buggies")
                prev_tyres = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_tyres = "knobbly"
            try:
                cur.execute("SELECT qty_tyres FROM buggies")
                prev_qty_tyres = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_qty_tyres = int(prev_qty_tyres)
            except:
                prev_qty_tyres = 4
            try:
                cur.execute("SELECT flag_color FROM buggies")
                prev_flag_color = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_flag_color = "#ffffff"
            
            try:
                cur.execute("SELECT flag_color_secondary FROM buggies")
                prev_flag_color_secondary = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_flag_color_secondary = "#ffffff"
            
            try:
                cur.execute("SELECT flag_pattern FROM buggies")
                prev_flag_pattern = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_flag_pattern = "plain"
                
            try:
                cur.execute("SELECT power_type FROM buggies")
                prev_power_type = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_power_type = "petrol"
            
            try:    
                cur.execute("SELECT power_units FROM buggies")
                prev_power_units = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_power_units = int(prev_power_units)
            except:
                prev_power_units = 1
            
            try:
                cur.execute("SELECT aux_power_type FROM buggies")
                prev_aux_power_type = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_aux_power_type = "none"
            
            try:    
                cur.execute("SELECT aux_power_units FROM buggies")
                prev_aux_power_units = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_aux_power_units = int(prev_aux_power_units)
            except:
                prev_aux_power_units = 0
            
            try:
                cur.execute("SELECT hamster_booster FROM buggies")
                prev_hamster_booster = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_hamster_booster = int(prev_hamster_booster)
            except:
                prev_hamster_booster = 0
            
            try:
                cur.execute("SELECT aux_hamster_booster FROM buggies")
                prev_aux_hamster_booster = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_aux_hamster_booster = int(prev_aux_hamster_booster)
            except:
                prev_aux_hamster_booster = 0
            try:
                cur.execute("SELECT armour FROM buggies")
                prev_armour = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_armour = "none"
            try:
                cur.execute("SELECT attack FROM buggies")
                prev_attack = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_attack = "none"
            try:
                cur.execute("SELECT qty_attacks FROM buggies")
                prev_qty_attacks = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
                prev_qty_attacks = int(prev_qty_attacks)
            except:
                prev_qty_attacks = 0
            try:
                cur.execute("SELECT fireproof FROM buggies")
                prev_fireproof = str(cur.fetchone()).replace(",","").replace("(", "").replace(")","");
            except:
                prev_fireproof = "false"
            try:
                cur.execute("SELECT insulated FROM buggies")
                prev_insulated = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_insulated = "false"
            try:
                cur.execute("SELECT antibiotic FROM buggies")
                prev_antibiotic = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_antibiotic = "false"
            try:
                cur.execute("SELECT banging FROM buggies")
                prev_banging = str(cur.fetchone()).replace(",","").replace("(","").replace(")","");
            except:
                prev_banging = "false"
                
            prev_form_store = [prev_id, prev_qty_wheels, prev_flag_color, prev_flag_color_secondary, prev_flag_pattern, prev_power_type, prev_power_units, prev_aux_power_type, prev_aux_power_units, prev_hamster_booster, prev_aux_hamster_booster, prev_tyres, prev_qty_tyres, prev_armour, prev_attack, prev_qty_attacks, prev_fireproof, prev_insulated, prev_antibiotic, prev_banging]
            for i in range(0, len(prev_form_store)):
                if prev_form_store[i] != "''":
                    prev_form_store[i] = str(prev_form_store[i]).replace("'","")
                else:
                    prev_form_store[i] = "None"
            cur = con.cursor()
            cur.execute("INSERT or IGNORE INTO buggies (id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (prev_id, prev_qty_wheels, prev_tyres, prev_qty_tyres, prev_flag_color, prev_flag_color_secondary, prev_flag_pattern, prev_power_type, prev_power_units, prev_aux_power_type, prev_aux_power_units, prev_hamster_booster, prev_aux_hamster_booster, prev_armour, prev_attack, prev_qty_attacks, prev_fireproof, prev_insulated, prev_antibiotic, prev_banging, 0)
            )
            con.commit()
            record = cur.fetchone();
            return render_template("buggy-form.html", buggy=record)
        #return render_template("buggy-form.html", prev_id=int(prev_form_store[0]), prev_qty_wheels=int(prev_form_store[1]), prev_flag_color=prev_form_store[2], prev_flag_color_secondary=prev_form_store[3], prev_flag_pattern=prev_form_store[4], prev_power_type=prev_form_store[5], prev_power_units=prev_form_store[6], prev_aux_power_type=prev_form_store[7], prev_aux_power_units=prev_form_store[8], prev_hamster_booster=prev_form_store[9], prev_aux_hamster_booster=prev_form_store[10], prev_tyres=prev_form_store[11], prev_qty_tyres=prev_form_store[12], prev_armour=prev_form_store[13], prev_attack=prev_form_store[14], prev_qty_attacks=prev_form_store[15], prev_fireproof=prev_form_store[16], prev_insulated=prev_form_store[17], prev_antibiotic=prev_form_store[18], prev_banging=prev_form_store[19])
    elif request.method == 'POST':
        msg = ""
        msg2 = ""
        buggy_id = request.form['id']
        qty_wheels = request.form['qty_wheels']
        flag_color = request.form['flag_color']
        flag_color_secondary = request.form['flag_color_secondary']
        flag_pattern = request.form['flag_pattern']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        aux_hamster_booster = request.form['aux_hamster_booster']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        cost_limit = request.form["cost_limit"]
        total_cost = 0
        
        form_store = [buggy_id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, armour, attack]#, aux_power_type, aux_power_units]
       
        #----ERRORS------------------------------------------------------------------------------------
        for i in range(0, len(form_store)):
            if form_store[i] == "":
                msg = "Insert the text in all the fields; "
        if  not request.form["qty_wheels"].strip().isdigit():
            msg += f"Oh noes, that is not a number: {qty_wheels}; "
        if int(qty_wheels) in range(0,4):
            msg += "Oh noes, the number of wheels can't be less than 4!; "
        if (int(qty_wheels) % 2) != 0:
            msg += "Oh noes, the number of wheels should be an even number!; "
        if int(qty_tyres) < int(qty_wheels):
            msg += "Oh noes, the number of tyres can't be less than the number of wheels!; "
        if power_type in ["fusion", "thermo", "solar", "wind"] and int(power_units) > 1:
            msg2 += "You can use only one unit for this power types --> Change the number to 1 to use it; "
        if aux_power_type in ["fusion", "thermo", "solar", "wind"] and int(aux_power_units) > 1:
            msg2 += "You can use only one unit for this power types --> Change the number to 1 to use it; "
        
        if msg != "" or msg2 != "":
            return render_template("buggy-form.html", prev_qty_wheels=qty_wheels, prev_flag_color=flag_color, prev_flag_color_secondary=flag_color_secondary, prev_flag_pattern=flag_pattern, prev_power_type=power_type, prev_power_units=power_units, prev_aux_power_type=aux_power_type, prev_aux_power_units=aux_power_units, prev_hamster_booster=hamster_booster, prev_aux_hamster_booster=aux_hamster_booster, prev_tyres=tyres, prev_qty_tyres=qty_tyres, prev_armour=armour, prev_attack=attack, prev_qty_attacks=qty_attacks, prev_fireproof=fireproof, prev_insulated=insulated, prev_antibiotic=antibiotic, prev_banging=banging, msg=msg, msg2=msg2)
        #----------------------------------------------------------------------------------------------        
        power_type_consumables = {"petrol": 4, "steam":3, "bio":5, "electric":20, "rocket": 16}#, "hamster": 3}
        power_type_non_consumables = {"fusion": 400, "thermo": 300, "solar": 40, "wind": 20}
        
        #--------------------------------------------------------------------------------------------  
        tyres_types_lim = {"knobbly": 15, "slick": 10, "steelband": 20, "reactive": 40, "maglev": 50}
        armours_lim = {"none": 0, "wood": 40, "aluminium": 200, "thinsteel": 100, "thicksteel": 200, "titanium": 290}
        attacks_lim = {"none": 0, "spike": 5, "flame": 20, "charge": 28, "biohazard": 30}
        if cost_limit != "" and int(cost_limit)>0:
            import random
            cost_limit_start = int(cost_limit)
            still_greater_than_zero = False
            rnd_qty_tyres = 0
            rnd_qty_power = 0
            rnd_qty_attacks = 0
            while still_greater_than_zero != True:
                rnd_qty_tyres = random.randrange(4, 12, 2)#12 max number for security
                rnd_tyres = random.choice(list(tyres_types_lim.values()))
                rnd_tyres_total = rnd_tyres*rnd_qty_tyres
                res = dict((v,k) for k,v in tyres_types_lim.items())
                rnd_tyres_choice = res[rnd_tyres]
                cost_limit = int(cost_limit)-rnd_tyres_total
                if int(cost_limit) <= 0:
                    while int(cost_limit) > 0:
                        rnd_qty_tyres = random.randrange(4, 12, 2)#12 max number for security
                        rnd_tyres = random.choice(list(tyres_types_lim.values()))
                        rnd_tyres_total = rnd_tyres*rnd_qty_tyres
                        res = dict((v,k) for k,v in tyres_types_lim.items())
                        rnd_tyres_choice = res[rnd_tyres]
                        cost_limit = int(cost_limit)-rnd_tyres_total
                rnd_qty_power = random.randint(1,10)#10 for security
                #ONLY consumable power for security of the code
                rnd_power_type = random.choice(list(power_type_consumables.values()))
                rnd_power_type_tot = rnd_power_type*rnd_qty_power
                res2 = dict((v,k) for k,v in power_type_consumables.items())
                rnd_power_type_choice = res2[rnd_power_type]
                cost_limit = int(cost_limit)-rnd_power_type_tot
                if int(cost_limit) <= 0:
                    while int(cost_limit) > 0:
                        rnd_qty_power = random.randint(1,10)#10 for security
                        #ONLY consumable power for security of the code
                        rnd_power_type = random.choice(list(power_type_consumables.values()))
                        rnd_power_type_tot = rnd_power_type*rnd_qty_power
                        res2 = dict((v,k) for k,v in power_type_consumables.items())
                        rnd_power_type_choice = res2[rnd_power_type]
                        cost_limit = int(cost_limit)-rnd_power_type_tot
                
                rnd_armour = random.choice(list(armours_lim.values()))
                rnd_armour_tot = rnd_armour*rnd_qty_tyres
                res3 = dict((v,k) for k,v in armours_lim.items())
                rnd_armours_choice = res3[rnd_armour]
                cost_limit = int(cost_limit)-rnd_armour_tot
                if int(cost_limit) <= 0:
                    while int(cost_limit) > 0:
                        rnd_armour = random.choice(list(armours._limvalues()))
                        rnd_armour_tot = rnd_armour*rnd_qty_tyres
                        res3 = dict((v,k) for k,v in armours_lim.items())
                        rnd_armours_choice = res3[rnd_power_type]
                        cost_limit = int(cost_limit)-rnd_armour_tot
                        
                rnd_qty_attacks = random.randint(0,10)#10 max number for security
                rnd_attacks = random.choice(list(tyres_types_lim.values()))
                rnd_attacks_tot = rnd_attacks*rnd_qty_tyres
                res = dict((v,k) for k,v in tyres_types_lim.items())
                rnd_attacks_choice = res[rnd_tyres]
                cost_limit = int(cost_limit)-rnd_attacks_tot
                if int(cost_limit) <= 0:
                    while int(cost_limit) > 0:
                        rnd_qty_attacks = random.randint(0,10)#10 max number for security
                        rnd_attacks = random.choice(list(tyres_types_lim.values()))
                        rnd_attacks_tot = rnd_attacks*rnd_qty_tyres
                        res = dict((v,k) for k,v in tyres_types_lim.items())
                        rnd_attacks_choice = res[rnd_tyres]
                        cost_limit = int(cost_limit)-rnd_attacks_tot
                def getRandomCol():
                    r = hex(random.randrange(0, 255))[2:]
                    g = hex(random.randrange(0, 255))[2:]
                    b = hex(random.randrange(0, 255))[2:]

                    random_col = '#'+r+g+b
                    return random_col
                rnd_flag_color = getRandomCol()
                rnd_flag_color_secondary = getRandomCol()
                flags = ["plain", "vstripe", "hstripe", "dstripe", "checker", "spot"]
                rnd_flag_pattern = flags[random.randint(0, len(flags)-1)]
                aux_power_type = "none"
                aux_power_units = 0
                fireproof = "false"
                insulated = "false"
                antibiotic = "false"
                banging = "false"
                if int(cost_limit) >= 0:
                    still_greater_than_zero = True
                else:
                    still_greater_than_zero = False
                    cost_limit = cost_limit_start
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("SELECT id FROM buggies")
                    buggy_id_d = str(cur.fetchall()).replace(",","").replace("(","").replace(")","");
                    if buggy_id in buggy_id_d :
                        cur.execute(
                        "UPDATE buggies SET qty_wheels=?, tyres=?, qty_tyres=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, aux_hamster_booster=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, total_cost=? WHERE id=?",
                        (rnd_qty_tyres, rnd_tyres_choice, rnd_qty_tyres, rnd_flag_color, rnd_flag_color_secondary, rnd_flag_pattern, rnd_power_type_choice, rnd_qty_power, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, rnd_armours_choice, rnd_attacks_choice, rnd_qty_attacks, fireproof, insulated, antibiotic, banging, cost_limit, buggy_id)
                        )
                    else:
                        cur.execute("INSERT INTO buggies (id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (buggy_id, rnd_qty_tyres, rnd_tyres_choice, rnd_qty_tyres, rnd_flag_color, rnd_flag_color_secondary, rnd_flag_pattern, rnd_power_type_choice, rnd_qty_power, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, rnd_armours_choice, rnd_attacks_choice, rnd_qty_attacks, fireproof, insulated, antibiotic, banging, cost_limit)
                        )
                    con.commit()
                    msg = "Record successfully saved"
            except sql.connect(DATABASE_FILE).Error as err:
                con.rollback()
                print("Something went wrong: {}".format(err))
                msg = "error in update operation"
            finally:
                con.close()
            return render_template("updated.html", msg = msg)
            
        #--------------------------------------------------------------------------------------------
        #TYRES
        tyres_types = {"knobbly": 15, "slick": 10, "steelband": 20, "reactive": 40, "maglev": 50}
        if tyres in tyres_types:
            total_cost += tyres_types[tyres]*int(qty_tyres)
        
        #ARMOUR
        armours = {"none": 0, "wood": 40, "aluminium": 200, "thinsteel": 100, "thicksteel": 200, "titanium": 290}
        if int(qty_tyres) == 4:
            total_cost += armours[armour]
        elif int(qty_tyres) > 4:
            total_cost += ((((int(qty_tyres)-4)*10)/100)*armours[armour])+armours[armour]
        
        #ATTACK
        attacks = {"none": 0, "spike": 5, "flame": 20, "charge": 28, "biohazard": 30}
        total_cost += attacks[attack]*int(qty_attacks)
        
        #FIREPROOF
        if fireproof == "true":
            total_cost += 70
        
        #INSULATED
        if insulated == "true":
            total_cost += 100
        
        #ANTIBIOTIC
        if antibiotic == "true":
            total_cost += 90
        
        #BANGING
        if banging == "true":
            total_cost += 42
        
        #HAMSTER BOOSTERS
        if power_type == "hamster":
            total_cost += int(power_units)*3
            if hamster_booster != 0:
                total_cost += int(hamster_booster)*5
            else: 
                total_cost = total_cost
        if aux_power_type == "hamster":
            total_cost += int(aux_power_units)*3
            if aux_hamster_booster != 0:
                total_cost += int(aux_hamster_booster)*5
            else: 
                total_cost = total_cost
            
        #Primary Engine
        if power_type in power_type_consumables:
            total_cost += power_type_consumables[power_type]*int(power_units)
        elif power_type in power_type_non_consumables:
            if total_cost == 0:
                total_cost += power_type_non_consumables[power_type]*int(power_units)
            else:
                total_cost = total_cost*power_type_non_consumables[power_type]
        #Auxiliary Engine
        if aux_power_type in power_type_consumables:
            total_cost += power_type_consumables[aux_power_type]*int(aux_power_units)
        elif aux_power_type in power_type_non_consumables:
            if total_cost == 0:
                total_cost += power_type_non_consumables[aux_power_type]*int(aux_power_units)
            else:
                total_cost = total_cost*power_type_non_consumables[aux_power_type]
        
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM buggies")
                buggy_id_d = str(cur.fetchall()).replace(",","").replace("(","").replace(")","");
                if buggy_id in buggy_id_d :
                    cur.execute(
                    "UPDATE buggies SET qty_wheels=?, tyres=?, qty_tyres=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, aux_hamster_booster=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, total_cost=? WHERE id=?",
                    (qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost, buggy_id)
                    )
                else:
                    cur.execute("INSERT INTO buggies (id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (buggy_id, qty_wheels, tyres, qty_tyres, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, aux_hamster_booster, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, total_cost,)
                    )    
                con.commit()
                msg = "Record successfully saved"
        except sql.connect(DATABASE_FILE).Error as err:
            con.rollback()
            print("Something went wrong: {}".format(err))
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
    records = cur.fetchall(); 
    con.close()
    return render_template("buggy.html", buggies=records)

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    print(f"FIXME I want to edit buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
    record = cur.fetchone();
    con.close()
    return render_template("buggy-form.html", buggy=record)

#------------------------------------------------------------
# delete the selected buggy
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
    print(f"I want to delete buggy #{buggy_id}")
    con = sql.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
    msg = "buggy deleted coorectly!"
    con.commit()
    return render_template("updated.html", msg=msg)
    
#------------------------------------------------------------
# delete all the buggies
#------------------------------------------------------------
@app.route('/delete_all')
def delete_buggies():
    print(f"I want to delete all the buggies")
    con = sql.connect(DATABASE_FILE)
    cur = con.cursor()
    cur.execute("DELETE FROM buggies")
    msg = "buggies deleted coorectly!"
    con.commit()
    return render_template("updated.html", msg=msg)

#------------------------------------------------------------
# a page for the project poster!
#------------------------------------------------------------
@app.route('/poster')
def poster():
   return render_template('poster.html')

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
def summary_first():
    try:
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
        buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items() 
        return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })
    except:
        msg = "No buggies stored in the database"
        return render_template("updated.html", msg=msg)
        
@app.route('/json_all')
def summary():
    try:
        con = sql.connect(DATABASE_FILE)
        SQL = "select * from buggies;"
        cur = con.cursor()
        cur.execute(SQL)
        result_list = cur.fetchall()      #return sql result
        print("fetch result-->",type(result_list))  #is s list type, need to be a dict

        fields_list = cur.description   # sql key name
        print("fields result -->",type(fields_list))
        #print("header--->",fields)
        cur.close()
        con.close()



        # main part
        column_list = []
        for i in fields_list:
            column_list.append(i[0])
        print("print final colume_list",column_list)

            # print("colume list  -->", column_list)

        jsonData_list = []
        for row in result_list:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            jsonData_list.append(data_dict)
        if len(jsonData_list) != 0:
            return jsonify({'buggies': jsonData_list})
        else:
            msg = "No buggies stored in the database"
            return render_template("updated.html", msg=msg)
    except:
        msg = "An error appeared -_-"
        return render_template("updated.html", msg=msg)
    

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
