from flask import Flask,render_template,session,request,flash,jsonify,redirect,url_for
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'login'
)

# @app.route('/')
# def login():
#     return render_template('index.html')

@app.route('/user',methods=["GET"])
def user():
    cur = db.cursor()
    cur.execute('SELECT * FROM mahasiswa')
    users = cur.fetchall()
    res = jsonify(users)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res

# @app.route('/login',methods=["POST"])
# def home():
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']


#         cur = db.cursor()
#         cur.execute('SELECT * FROM user WHERE username=%s',(username,))
#         data = cur.fetchone()
#         cur.close()    
#         try:
#             if username == data[1]:
#                 if password == data[2]:
#                     session['username'] = data[1]
#                     session['password'] = data[2]
#                     return render_template('home.html')
#                 else:
#                     flash('Wrong Password!')
#                     return render_template('login.html')
            
#         except:
#             flash("User Not Found")
#             return render_template('login.html')

        
# @app.route('/logout')
# def logoout():
#     user = session['username']
#     flash(f"You have been Logout,{user}!")
#     return render_template('login.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add',methods=["POST"])
def add():
    if request.method == 'POST':
        username = request.form['usernameRegister'] 
        password = request.form['passwordRegister']

        cur = db.cursor()
        query = ('INSERT INTO user (username,password) VALUES(%s,%s)')
        data = (username,password,)
        cur.execute(query,data)
        db.commit()
        flash("User Successfully Registered") 
    return render_template('login.html')

@app.route('/search',methods=["POST"])
def search():
    if request.method == "POST":
        data = request.form['search']
        cur=db.cursor()
        cur.execute('SELECT * FROM mahasiswa WHERE nama=%s',(data,))
        p = cur.fetchone()
        try:
            if data == p[2]:
                session['npm'] = p[1]
                session['nama'] = p[2]
                session['asal'] = p[3]
                session['fakultas'] = p[4]
                session['prodi'] = p[5]
                return render_template('profil.html')
        except:
            return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/back')
def back():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminhome')
def adminhome():
    cur = db.cursor()
    cur.execute('SELECT * FROM mahasiswa')
    data = cur.fetchall()
    return render_template('admin_home.html',data = data)

@app.route('/adminlogin',methods=["POST"])
def loginadmin():
    if request.method == "POST":
        username = request.form['username_admin']
        password = request.form['password_admin']


        cur = db.cursor()
        cur.execute('SELECT * FROM admin WHERE username_admin=%s',(username,))
        data = cur.fetchone()
        cur.close()    
        try:
            if username == data[1]:
                if password == data[2]:
                    session['username'] = data[1]
                    session['password'] = data[2]

                    cur = db.cursor()
                    cur.execute('SELECT * FROM mahasiswa')
                    data = cur.fetchall()
                    return render_template('admin_home.html',data=data)
                else:
                    flash('Wrong Password')
                    return render_template('adminlogin.html')
            
        except:
            flash('User not found!')
            return render_template('adminlogin.html')

@app.route('/adminlogout')
def adminlogout():
    flash("You have been Logout")
    return render_template('adminlogin.html')

@app.route('/forminsert')
def forminsert():
    return render_template('insert.html')

@app.route('/insert',methods=['POST'])
def insert():
    try:
        if request.method == 'POST':
            npm = request.form['npm']
            nama = request.form['nama']
            asal = request.form['asal']
            fakultas = request.form['fakultas']
            prodi = request.form['prodi']

            cur = db.cursor()
            cur.execute("INSERT INTO mahasiswa(NPM,nama,asal,fakultas,prodi)VALUES(%s,%s,%s,%s,%s)",(npm,nama,asal,fakultas,prodi,))
            db.commit()
    except:
        flash('data harus diisi')
        return render_template('insert.html')
    return redirect(url_for('adminhome'))

@app.route('/update/<int:id>')
def update(id):
    cur = db.cursor()
    cur.execute('SELECT * FROM mahasiswa where id=%s',(id,))
    id = cur.fetchall()
    return render_template('update.html', id = id)

@app.route('/updatedata',methods=['POST'])
def updatedata():
    if request.method == "POST":
        npm = request.form['npm']
        nama = request.form['nama']
        asal = request.form['asal']
        fakultas = request.form['fakultas']
        prodi = request.form['prodi']

        cur = db.cursor()
        query = ("UPDATE mahasiswa SET npm=%s,nama=%s,asal=%s,fakultas=%s,prodi=%s WHERE npm=%s")
        data = (npm,nama,asal,fakultas,prodi,npm,)
        cur.execute(query,data)
        db.commit()
    return redirect(url_for('adminhome'))


@app.route('/delete/<int:id>',methods=['GET'])
def delete(id):
    if request.method == 'GET':
        cur = db.cursor()
        cur.execute('DELETE FROM mahasiswa WHERE id=%s',(id,))
        db.commit()
    return redirect(url_for('adminhome'))


if __name__ == "__main__":
    app.run(debug=True)
