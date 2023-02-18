from flask import Flask, request, render_template, session, flash
from collections import deque
import datetime
import sqlite3
from sqlite3 import Error
from util import *

app = Flask(__name__, template_folder = "templates", static_folder="static")
app.secret_key = 'bankqueuesystem2023'  

branches = ['Jurong','Woodlands','Bedok','HarbourFront']   # branches to be used

try:
    con = sqlite3.connect("bankQueue.db")  # creating tables for each branch
    cur = con.cursor()
    for each in branches:
        cur.execute(f""" 
        CREATE TABLE IF NOT EXISTS {each} (
        q_num INTEGER PRIMARY KEY,
        contact INTEGER,
        purpose TEXT NOT NULL DEFAULT '',
        category TEXT NOT NULL DEFAULT '');
        """)
    con.commit()
except Error as err:
    print(err)
finally:
    if con:
        con.close()

# defining all queues
"""
services = ['dw','ao','rem','iil','prio']       # exec use is discouraged

for branch in branches:
    for each in services:
        var = '{}_{} = deque()'.format(each,branch)
        exec(var)
        print(var)
"""
# corporate - start 1   
# depo withdrawl - 2
# acc opening - 4
# remittance - 6
# ins inv loan - 8

miss = []
ans = None                  # may need some cleaning
next_num = None
waiting = None
to_delete = None

year = datetime.date.today().year

# admin login
@app.route('/admin', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        counter_num = request.form.get('counter_num')
        admin_branch = request.form.get('admin_branch')
        session['counter_num'] = counter_num
        session['admin_branch'] = admin_branch
        return render_template('admin.html',counter_num=counter_num,admin_branch=admin_branch)
    else:
        return render_template('login.html')

# admin page
@app.route('/admin/main/<counter_num>', methods = ['GET','POST'])   # solved counter number disappearing problem
def admin(counter_num):
    if request.method == 'POST':
        service = request.form.get('service')
        press = request.form.get('choice')
        counter_num = session.get('counter_num',None)
        admin_branch = session.get('admin_branch',None)

        if press == 'Next':
            if service == 'dw':
                ans = get_next_num('Deposit or Withdrawal',admin_branch)
                        
            elif service == 'ao':
                ans = get_next_num('Account Opening',admin_branch)

            elif service == 'rem':
                ans = get_next_num('Remittance',admin_branch)

            elif service == 'iil':
                ans = get_next_num('Insurance Investment Loans',admin_branch)

            elif service == 'cor':
                ans = get_next_num('Corporate',admin_branch)

            global next_num     # pls don't touch this
            global waiting
            global to_delete

            next_num = ans[0]
            waiting = ans[1]
            to_delete = ans[2]

        if press == 'Missed':   # add to miss queue (not the best condition but works)
            miss.append(to_delete)
            print(miss)

        elif press == 'Call Again':     # no functional use as of now; can link w bell to call clients
            pass

        session['next_num'] = next_num  
        session['miss'] = miss

    return render_template('admin.html', next_num=next_num, waiting=waiting, miss=miss, counter_num=counter_num, admin_branch=admin_branch)

# main page
@app.route('/', methods=['GET','POST'])   
def index():
    return render_template('main.html')                        
    
@app.route('/form', methods = ['GET','POST'])
def form():
    if request.method == 'POST':
        action = request.form.get('biz')
        session['biz'] = action
        return render_template('form.html',action=action)
    else:
        return render_template('main.html')

@app.route('/personal', methods = ['GET','POST'])      ##### cannot go straight to this url bc of database
def personal():
    contact = request.form.get('contact')
    cat = request.form.get('category')
    branch = request.form.get('branch')
    purpose = session.get('biz',None)      # biz purpose
    curr_serve = session.get('next_num',None)
      
    num = 0
    q = ''
    with sqlite3.connect('bankQueue.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f'SELECT * FROM {branch};')
        row = cur.fetchall()    # queue data

        if cat == 'Corporate':
            prio = deque()                                      
            if row:             # populating queue if existing
                for r in row:   
                    if r[3] == 'Corporate':
                        prio(r[0])     
            if not prio:
                num = 1
                prio.append(num)
            else:
                num = prio[-1]+1
                prio.append(num)
            q = prio

        elif cat == 'Individual' and purpose == 'Deposit or Withdrawal':
            dw = deque()
            if row:                     # populating queue if existing
                for r in row:
                    if r[2] == 'Deposit or Withdrawal' and r[3] == 'Individual':
                        dw.append(r[0])
            if not dw:
                num = 2001
                dw.append(num)
            else:
                num = dw[-1]+1
                dw.append(num)
            q = dw

        elif cat == 'Individual' and purpose == 'Account Opening':
            ao = deque()
            if row:                     
                for r in row:
                    if r[2] == 'Account Opening' and r[3] == 'Individual':
                        ao.append(r[0])
            if not ao:
                num = 4001
                ao.append(num)
            else:
                num = ao[-1]+1
                ao.append(num)
            q = ao

        elif cat == 'Individual' and purpose == 'Remittance':
            rem = deque()
            if row:                     # populating queue if existing
                for r in row:
                    if r[2] == 'Remittance' and r[3] == 'Individual':
                        rem.append(r[0])
            if not rem:
                num = 6001
                rem.append(num)
            else:
                num = rem[-1]+1
                rem.append(num)
            q = rem
                        
        else:
            iil = deque()
            if row:                     # populating queue if existing
                for r in row:
                    if r[2] == 'Insurance Investment Loans' and r[3] == 'Individual':
                        iil.append(r[0])
            if not iil:
                num = 8001
                iil.append(num)
            else:
                num = iil[-1]+1
                iil.append(num)
            q = iil

        param = (num,contact,purpose,cat)
        cur.execute(f"INSERT INTO {branch} (q_num,contact,purpose,category) VALUES (?,?,?,?);",param)
        con.commit()        # updating database with new queue num
            
    return render_template('personal.html', purpose=purpose, num=num, q=q, curr_serve=curr_serve,branch=branch)  ########## have issues here, form resubmits when refreshed; queue number increases when it shouldn't
  
    ##### troubleshoot: separate function that increases queue number and condition to check if button was pressed(??) - Probably needs JavaScript eventlistener? Need more time to think 

# big screen
@app.route('/screen/<branch>', methods = ['GET','POST'])     
def screen(branch):
    with sqlite3.connect('bankQueue.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f'SELECT * FROM {branch};')
        row = cur.fetchall()    # branch queue data
    counter_num = session.get('counter_num',None)
    all_serve = []
    curr_serve = session.get('next_num',None)
    all_serve.append((curr_serve,counter_num))      ####### counter number does not get appended, gets overriden instead. Is it possible to send multiple requests without using threads?
    miss = session.get('miss',None)
    if not miss:
        miss = []
    return render_template('screen.html', row=row,miss=miss,all_serve=all_serve,branch=branch)

if __name__ == "__main__":
    app.run(debug=False)
