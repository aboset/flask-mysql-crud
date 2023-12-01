from flask import Flask,render_template,request,redirect,url_for
import os
import database as db 

app = Flask(__name__, template_folder='templates')

#rutas aplicacion

@app.route('/')

def home():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM contacts")
    myresult = cursor.fetchall()
    #datos a diccionario
    insertObject= []
    columnNames=[column[0]for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames,record)))
    
    cursor.close()
    
    return render_template('index.html',data=insertObject)

#rutas guardar usuario
@app.route('/user', methods=['POST'])

def adduser():
    nombres=request.form['nombres']
    telefono=request.form['telefono']
    email=request.form['email']
    
    
    if nombres and telefono and email:
        cursor=db.database.cursor()
        sql= "INSERT INTO contacts (nombres,telefono,email) VALUES (%s,%s,%s)"
        data= (nombres,telefono,email)
        cursor.execute(sql,data)
        db.database.commit()
    
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')

def delete(id):
        
    cursor=db.database.cursor()
    sql= "DELETE FROM contacts WHERE id=%s"
    data= (id,)
    cursor.execute(sql,data)
    db.database.commit()
    
    
    return redirect(url_for('home'))

@app.route('/edit/<string:id>',methods=['POST'])

def edit(id):
    
    nombres=request.form['nombres']
    telefono=request.form['telefono']
    email=request.form['email']
    
    
    if nombres and telefono and email:
        cursor=db.database.cursor()
        sql= "UPDATE contacts SET nombres=%s, telefono=%s, email=%s WHERE id=%s"
        data= (nombres,telefono,email,id)
        cursor.execute(sql,data)
        db.database.commit()
    
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
