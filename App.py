from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)

#myslq connection
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'administrador'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kkpEJnkFyZZK7SzI'
app.config['MYSQL_DATABASE_DB'] = 'users'
mysql = MySQL()
mysql.init_app(app)

# settings
app.secret_key = 'misecreto'

@app.route('/')
def Index():
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname'] #reciviomos los datos
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", #escribimos la consulta 
        (fullname, phone, email))
        mysql.get_db().commit() #ejecutamos la consula
        flash('Contact Added Successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.get_db().cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s,
            WHERE  id = %s
        """, (fullname, phone, email, id))
        mysql.get_db().commit()
        flash('Contact Update Successfully')
        return redirect(url_for('Index'))



@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.get_db().cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.get_db().commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True) 