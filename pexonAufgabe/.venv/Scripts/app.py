import sqlite3


from flask import Flask
from flask import render_template, request, url_for, flash, redirect, abort

#definition of the object of flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zertifizierung'

#Connection to the sqlite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#get the current certification
def get_certification(certification_id):
    conn = get_db_connection()
    sqlQuery='SELECT * FROM certifications WHERE id = ?'
    cert = conn.execute(sqlQuery,
                        (certification_id,)).fetchone()
    conn.close()
    if cert is None:
        abort(404)
    return cert

@app.route('/')
def home():
    conn = get_db_connection()
    certification = conn.execute('SELECT * FROM certifications').fetchall()
    conn.close()
    return render_template('home.html', certifications=certification)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            sqlQuery='INSERT INTO certifications (title, content) VALUES (?, ?)'
            conn.execute(sqlQuery,
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    certification = get_certification(id)
    post= request.method == 'POST'
    if post:
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            sqlQuery='UPDATE certifications SET title = ?, content = ?'' WHERE id = ?'      
            conn.execute(sqlQuery,
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template('edit.html', certification=certification)


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    certification = get_certification(id)
    conn = get_db_connection()
    sqlQuery='DELETE FROM certifications WHERE id = ?'
    conn.execute(sqlQuery, (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(certification['title']))
    return redirect(url_for('home'))

