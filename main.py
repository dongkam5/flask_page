from flask import *
import sqlite3

app=Flask(__name__)
app.secret_key='dongkam is good'
def dbcon():
    return  sqlite3.connect('./database.db')

def create_table():
    try:
        db=dbcon()
        cur=db.cursor()
        cur.execute("CREATE TABLE CLIENTS (id varchar(10), password varchar(10), name varchar(15), age INT(10))")
        db.commit()
    except Exception as e:
        print('db error: ',e)
    finally:
        db.close()
def insert_data(id,password,name,age):
    db=dbcon()
    try:
        cur= db.cursor()
        setdata=(id,password,name,age)
        cur.execute("INSERT INTO CLIENTS VALUES (?,?,?,?)",setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
def select_all():
    ret = list()
    try:
        db=dbcon()
        cur=db.cursor()
        cur.execute("SELECT * FROM CLIENTS")
        ret=cur.fetchall()
    except Exception as e:
        print('db Error:',e)
    finally:
        db.close()
        return ret    
def checkclient(id,password):
    clients=select_all()
    for client in clients:
        if client[0]==id and client[1]==password: ## 0=id, 1= password
            return client[2]
    return None
create_table()
LoggedIn=False
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/showpage')
def showpage():
    return render_template('showpage.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if (request.method=='POST'):
        id=request.form['id']
        password=request.form['password']
        name=checkclient(id,password)
        if not name:
            flash("Please ENTER CORRECTLY")
            return redirect(url_for('login'))
        flash("WELCOME   "+ name)
        return redirect(url_for('index'))
    else:
        return render_template('login.html')
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/signup', methods=['GET','POST'])
def signup():
    if (request.method=='POST'):
        id=request.form['id']
        name=request.form['name']
        password=request.form['password']
        age=request.form['age']
        print(id,name,password,age) 
        insert_data(id,password,name,age)
        print(select_all())
        return redirect(url_for('index'))
    elif (request.method=='GET'):
        return render_template('signup.html')

if __name__=="__main__":
    app.run(debug=True)