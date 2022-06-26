from flask import Flask, render_template, session, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector

app = Flask("__name__")
app.secret_key = "drip.inc"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'drip.inc'
db = mysql.connector.connect(host="localhost", user = "root", password = "toor", database = "drip.inc")

mysql = MySQL(app)

@app.route("/")
def home():
    if 'loggedin' in session:
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone()
        return render_template('index.html', email = session['email'], fname = fname)
    else:
        return render_template('index.html')

@app.route("/new")
def new():
    if 'loggedin' in session:
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone()
        return render_template('new.html', email = session['email'], fname = fname)
    else:
        return render_template('new.html')

@app.route("/brands")
def brands():
    return render_template("brands.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    errmsg = ''
    if request.method == "POST" and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['fname'] = account['fname']
            return redirect("/")
    else:
        errmsg= 'Invalid Data'
    return render_template("login.html", errmsg = errmsg)



@app.route("/register", methods=['GET', 'POST'])
def register():
    errmsg = ''
    if request.method == "POST" and 'fname' in request.form and 'password' in request.form and 'email' in request.form:
        fname = request.form['fname']
        password = request.form['password']
        email = request.form ['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cur.fetchone()
        if account:
            errmsg = 'Email found in Database'
        elif not email or not fname or not password:
            errmsg = 'Form data incomplete.'
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (fname, password, email))
            mysql.connection.commit()
            errmsg = 'Registration Complete.'
            return redirect("/login")
    elif request.method == "POST":
        errmsg = 'Form data incomplete '
    return render_template("register.html", errmsg = errmsg)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect("/")

@app.route("/user", methods=["GET", "POST"])
def user():
        if 'loggedin' in session:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM accounts WHERE id = %s", (session['id'],))
            account = cur.fetchone()
            if request.method == "POST" and 'password' in request.form:
                password = request.form['password']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE accounts SET password = %s WHERE id = %s", (password, session['id']))
                mysql.connection.commit()
                return redirect("/user")
            return render_template("userprofile.html", account = account)
        else:
            return redirect("/login")

@app.route('/collections')
def collections():
    if 'loggedin' in session:
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone()
        return render_template('collections.html', email = session['email'], fname = fname)
    else:
        return render_template('collections.html')

@app.route('/all')
def shopall():
    if 'loggedin' in session:
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone()
        return render_template('all.html', email = session['email'], fname = fname)
    else:
        return render_template('all.html')
    
@app.route("/clothing")
def accessories():
    return render_template("clothing.html")

# PRODUCTS
@app.route('/product/nike-air-force-1-react', methods=['GET', 'POST'])
def product_airforce1react():
    if 'loggedin' in session:
        id = 1
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/airforce1react.html', email = session['email'], fname = fname)
    else:
        return render_template('product/airforce1react.html')

@app.route("/product/nike-air-jordan-1", methods=['GET', 'POST'])
def product_nikeairjordan1():
    if 'loggedin' in session:
        id = 2
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/airjordan1.html', email = session['email'], fname = fname)
    else:
        return render_template('product/airjordan1.html')

@app.route("/product/nike-airjordans-XXXVI-low", methods=['GET', 'POST'])
def product_nikeairjordanxxxvilow():
    if 'loggedin' in session:
        id = 3
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/AirJordansXXXVILow.html', email = session['email'], fname = fname)
    else:
        return render_template('product/AirJordansXXXVILow.html')

@app.route("/product/nike-zoomx-invincible-run-flyknit-2", methods=['GET', 'POST'])
def product_zoomxinvinciblerunflyknit2():
    if 'loggedin' in session:
        id = 4
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/zoomxinvinciblerunflyknit2.html', email = session['email'], fname = fname)
    else:
        return render_template('product/zoomxinvinciblerunflyknit2.html')

@app.route("/product/nike-air-max-97", methods=['GET', 'POST'])
def product_airmax97():
    if 'loggedin' in session:
        id = 5
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/airmax97.html', email = session['email'], fname = fname)
    else:
        return render_template('product/airmax97.html')

@app.route("/product/nike-air-max-plus-og", methods=['GET', 'POST'])
def product_airmaxplusog():
    if 'loggedin' in session:
        id = 6
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/airmaxplusog.html', email = session['email'], fname = fname)
    else:
        return render_template('product/airmaxplusog.html')

@app.route("/product/converse-taylor-all-star-classic", methods=['GET', 'POST'])
def product_chucktaylorallstarclassic():
    if 'loggedin' in session:
        id = 7
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/taylorallstarclassic.html', email = session['email'], fname = fname)
    else:
        return render_template('product/taylorallstarclassic.html')

@app.route("/product/nike-dunks-violet", methods=['GET', 'POST'])
def product_dunksviolet():
    if 'loggedin' in session:
        id = 8
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/dunksvioletagednavy.html', email = session['email'], fname = fname)
    else:
        return render_template('product/dunksvioletagednavy.html')
        
@app.route("/product/nike-sb-nyjah-free-2", methods=['GET', 'POST'])
def product_sbnyjah():
    if 'loggedin' in session:
        id = 9
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/sbnyjahfree2.html', email = session['email'], fname = fname)
    else:
        return render_template('product/sbnyjahfree2.html')

@app.route("/product/superdry-premium-beach-sliders", methods=['GET', 'POST'])
def product_beachsliders():
    if 'loggedin' in session:
        id = 10
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/beachsliders.html', email = session['email'], fname = fname)
    else:
        return render_template('product/beachsliders.html')

@app.route("/product/nike-tiempo-legend-9-elite-FG", methods=['GET', 'POST'])
def product_tiempolegend9elite():
    if 'loggedin' in session:
        id = 11
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/tiempolegend9.html', email = session['email'], fname = fname)
    else:
        return render_template('product/tiempolegend9.html')

@app.route("/product/vans-sk8-hi", methods=['GET', 'POST'])
def product_vanssk8hi():
    if 'loggedin' in session:
        id = 12
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/vanssk8hi.html', email = session['email'], fname = fname)
    else:
        return render_template('product/vanssk8hi.html')

@app.route("/product/adidas-M-FI-CB-OH", methods=['GET', 'POST'])
def product_MFICBOH():
    if 'loggedin' in session:
        id = 13
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/MFICBOH.html', email = session['email'], fname = fname)
    else:
        return render_template('product/MFICBOH.html')

@app.route("/product/nike-jordan-air", methods=['GET', 'POST'])
def product_jordanair():
    if 'loggedin' in session:
        id = 14
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/jordanair.html', email = session['email'], fname = fname)
    else:
        return render_template('product/jordanair.html')

@app.route("/product/vans-daniel-johnston-hoodie", methods=['GET', 'POST'])
def product_vansxdanieljohnston():
    if 'loggedin' in session:
        id = 15
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            value = "true"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/vansxdaniel.html', email = session['email'], fname = fname)
    else:
        return render_template('product/vansxdaniel.html')

@app.route("/product/converse-paint-drip-graphic-hoodie", methods=['GET', 'POST'])
def product_paintdrip():
    if 'loggedin' in session:
        id = 16
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone() 
        cur.execute("SELECT id FROM accounts WHERE email = %s", (email,))
        userid = str(cur.fetchone()['id'])
        if request.method == "POST" and 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
            productsid = cursor.fetchone()['productsid']
            productsid = list(productsid)
            if str(id) not in productsid:
                productsid.append(id)
                productsid.remove('[')
                productsid.remove(']')
                cursor.execute("UPDATE cart SET productsid = %s WHERE userid = %s", (str(productsid), userid))
                mysql.connection.commit()
        return render_template('product/paintdripgraphic.html', email = session['email'], fname = fname)
    else:
        return render_template('product/paintdripgraphic.html')

@app.route("/cart")
def cart():
    if 'loggedin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id FROM accounts WHERE email = %s", (session['email'],))
        userid = str(cur.fetchone()['id'])
        cur.execute("SELECT productsid FROM cart WHERE userid = %s", (userid))
        productsid = str(cur.fetchone()['productsid'])
        products = []
        productsid = list(productsid)
        for productid in productsid:
            if productid != '[' and productid != ']' and productid != ','  and productid != ' '  and productid != "'" and productid != '"' :
                cur.execute("SELECT * FROM product WHERE id = %s", (productid))
                productdetails = cur.fetchone()
                products.append([productdetails['name'], productdetails['price']])
        email = session['email']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT fname FROM accounts WHERE email = %s", (email,))
        fname = cur.fetchone()
        return render_template('cart.html', email = session['email'], fname = fname, products = products)# remove comma when backend dun
    else:
        return redirect("/login")
# Error Handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
