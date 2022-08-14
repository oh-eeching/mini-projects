from flask import Flask, request, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__, template_folder = "templates")

try:
    con = sqlite3.connect("products.db")
    cur = con.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS product (
    prod_id INTEGER PRIMARY KEY,
    prod_name TEXT NOT NULL DEFAULT '');
    """)
    con.commit()
except Error as err:
    print(err)
finally:
    if con:
        con.close()

@app.route('/')
def index():
    return render_template("menu.html")

@app.route('/a/products/all')
def displayAll():
        with sqlite3.connect("products.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM product;")
            row = cur.fetchall()
            return render_template("display.html",row = row)

@app.route('/a/product', methods = ['GET','POST'])
def search():
    if request.method == "POST":
        value = request.form['id']
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT prod_id, prod_name FROM product WHERE prod_id = {value};")
            row = cur.fetchall()
            return render_template("display.html", row = row)
    else: 
        return render_template("getprod.html")

@app.route('/a/product/add',methods = ['GET','POST'])
def addProd():
    if request.method == "POST":
        value1 = request.form['id']
        value2 = request.form['name']
        param = (value1,value2)
        with sqlite3.connect('products.db') as con:
            cur = con.cursor() 
            cur.execute("INSERT INTO product (prod_id,prod_name) VALUES (?,?);",param)
            con.commit()
        return render_template('added.html')
    else:
        return render_template('insert.html')

@app.route('/a/product/remove',methods = ['GET','POST'])
def removeProd():
    if request.method == "POST":
        prod = request.form['id']
        with sqlite3.connect('products.db') as con:
            cur = con.cursor() 
            cur.execute(f"DELETE FROM product WHERE prod_id = {prod};")
            con.commit()
        return render_template('removed.html')

    else:
        with sqlite3.connect('products.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM product;")
            row = cur.fetchall() 
        return render_template('remove.html', row = row)
    
if __name__ == "__main__":
    app.run()
