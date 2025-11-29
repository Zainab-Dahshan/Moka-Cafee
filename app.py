from flask import Flask, render_template, request, redirect
import sqlite3

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contact_messages (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    conn.commit()
    conn.close()

    return redirect('/contact')
