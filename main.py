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
        cur.execute("CREATE TABLE POSTS (title varchar(50), detail varchar(1000), id varchar(15), post_num INT(5))")
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

def insert_data_post(title,detail,id,post_num):
    db=dbcon()
    try:
        cur= db.cursor()
        setdata_post=(title,detail,id,post_num)
        cur.execute("INSERT INTO POSTS VALUES (?,?,?,?)",setdata_post)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
def update_data_post(title,detail,id,post_num):
    db=dbcon()
    try:
        cur= db.cursor()
        setdata_post=(title,detail,id,post_num)
        cur.execute("UPDATE POSTS SET title=? ,detail=? ,id=? where post_num=?",setdata_post)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
def delete_data_post(post_num):
    db=dbcon()
    try:
        cur= db.cursor()
        cur.execute("DELETE FROM POSTS WHERE post_num=?",str(post_num))
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
def write_templates(title,id,detail,post_num):
    with open("templates/posts/{}.html".format(post_num),"w")as p:
            p.write('''
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <h2 style="margin: auto; text-align: center; margin-top:60px;">{}</h2>
        <h4 style="margin: auto; text-align: center; margin-top:60px;">by {}</h4> 
        <div class="info" style="text-align: center; margin: auto;">
            <div class="subinfo" style="margin-top: 50px";>
                <p>{}</p>
            </div>
            <div class="APPEND" style="display: flex; justify-content: center; text-align: center; margin-top: 60px;">
                <form action="../update" method="POST">
                    <input type="hidden" value="{}" name="post_num_update">
                    <input type="hidden" value="{}" name="id">
                    <input type="submit" value="UPDATE">
                </form>
                <form action="../delete" method="POST">
                    <input type="hidden" value="{}" name="post_num_delete">
                    <input type="hidden" value="{}" name="id">
                    <input type="submit" value="DELETE">
                </form>
        </div>
            <div class="subinfo" style="margin: auto; text-align: center; margin-top:60px;">
                <form action="/showpage">
                    <input type="submit"  value="BACK TO LIST">
                </form>
            </div>
        </div>
    </body>
</html>
            '''.format(title,id,detail,post_num,id,post_num,id))
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
        post_num=len(show_post_info())+1
        write_templates(title,id,detail,post_num)
        insert_data_post(title,detail,id,post_num)
        return  redirect(url_for('showpage'))
    elif (request.method=='GET'):
        return render_template('write.html',id=session['id'])
@app.route('/posts/<post_num>')
def post(post_num):
    return render_template("/posts/{}.html".format(post_num))

@app.route('/update', methods=['POST'])
def update():
    if isLogged():
        if request.method=='POST':
            post_num_update=request.form['post_num_update']
            id=request.form['id']
            posts=show_post_info()
            for post in posts:
                if post[3]==int(post_num_update) and session['id']==id:
                    return render_template('update.html', post=post)
            return redirect(url_for('showpage'))
    
    else:
        return redirect(url_for('login'))

@app.route('/delete',methods=['POST'])
def delete():
    if isLogged():
        if request.method=='POST':
            post_num_delete=request.form['post_num_delete']
            id=request.form['id']
            posts=show_post_info()
            for post in posts:
                if post[3]==int(post_num_delete) and session['id']==id:
                    delete_data_post(int(post[3]))
                    with open("templates/posts/{}.html".format(post_num_delete),"w")as p:
                        p.write('''
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <h1 style="text-align: center;"> THIS PAGE IS DELETED</h1><br>
        <div style=" text-align: center; justify-content: center;">
        <form action="/del_save" method="POST">
            <input type="submit" value="GO TO INDEX">
        </form>
    </div>  
    </body>
</html>
''')
            return redirect(url_for('showpage'))
    
    else:
        return redirect(url_for('login'))

@app.route('/save',methods=['POST'])
def save():
    if isLogged():
        title=request.form['title']
        detail=request.form['detail']
        id=request.form['id']
        post_num=request.form['post_num']
        write_templates(title,id,detail,post_num)
        update_data_post(title,detail,id,post_num)
        return redirect(url_for('showpage'))
    else:
        return redirect(url_for('login'))
@app.route('/del_save',methods=['POST'])
def del_save():
    return redirect(url_for('showpage'))

if __name__=="__main__":
    app.run(debug=True)