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

def create_table_post():
    try:
        db=dbcon()
        cur=db.cursor()
        cur.execute("CREATE TABLE POSTS (title varchar(50), detail varchar(1000), name varchar(15))")
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

def insert_data_post(title,detail,id):
    db=dbcon()
    try:
        cur= db.cursor()
        setdata_post=(title,detail,id)
        cur.execute("INSERT INTO POSTS VALUES (?,?,?)",setdata_post)
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
def select_all_post():
    ret = list()
    try:
        db=dbcon()
        cur=db.cursor()
        cur.execute("SELECT * FROM POSTS")
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
            return client
    return None
def isLogged():
    if 'id' in session:
        id=session['id']
        return True
    return False
def show_clinet_info(id):
    clients=select_all()
    for client in clients:
        if client[0]==id:
            return client
def show_post_info():
    posts=select_all_post()
    return posts
create_table()
create_table_post()
@app.route('/')
def index():
    if isLogged():
        return render_template('index.html', name=(show_clinet_info(session['id'])[2]))
    else:
        return render_template('index.html',name='None')
@app.route('/showpage')
def showpage():
    if isLogged():
        return render_template('showpage.html', name=(show_clinet_info(session['id'])[2]) , posts=show_post_info())
    else:
        return render_template('showpage.html',name='None', posts=show_post_info())
@app.route('/login',methods=['GET','POST'])
def login():
    if (request.method=='POST'):
        id=request.form['id']
        password=request.form['password']
        client_info=checkclient(id,password)
        if client_info == None:
            flash("Please ENTER CORRECTLY")
            return redirect(url_for('login'))
        session['id']=client_info[0]
        return redirect(url_for('index'))
    else:
        return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('id',None)
    return redirect(url_for('index'))
@app.route('/mypage')
def mypage():
    if isLogged():
        client_info=show_clinet_info(session['id'])
        return render_template('mypage.html',client_info=client_info)
    else:
        return redirect(url_for('login'))
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
@app.route('/write', methods=['GET','POST'])
def write():
    if (request.method=='POST'):
        id=request.form['id']
        title=request.form['title']
        detail=request.form['detail']
        insert_data_post(title,detail,id)
        return  redirect(url_for('showpage'))
    elif (request.method=='GET'):
        return render_template('write.html',id=session['id'])

if __name__=="__main__":
    app.run(debug=True)