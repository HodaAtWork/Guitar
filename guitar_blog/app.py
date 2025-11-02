#
# Tutorial https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
# Summernote WYSIWIG editor well explained in https://www.youtube.com/watch?v=Ak-CtugDRFA (thanks Anthony from Pretty Printed) 
#
# STEP 3 using HTML templates
# STEP 4 adds sqlite3 database stuff
# STEP 5 display all posts
# STEP 6 display 1 post
# STEP 7 modify posts
#

import sqlite3
from flask import Flask, render_template, url_for, flash, redirect, request
from werkzeug.exceptions import abort
import pyjokes
import os

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * from posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    if post is None:
        abort(404)
    # print(f'POST ID = {post['id']}')
    # print(f'POST TITLE = {post['title']}')
    # print(f'POST CONTENT = {post['content']}')
    
    return post

app = Flask(__name__)  # a Flask application instance. __name__ holds name current Python module
app.config['SECRET_KEY'] = 'Olopretaw%dab1eparet'

@app.route('/')  # a decorator on main url '/': function's return value => http response to display by http client like a webbrowser
def index():  # view function looks for index.html in folder templates
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts = posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post = post)

@app.route('/create', methods = ('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit', methods = ('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
        
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods = ('POST',))
def delete(id):
    post = get_post(id)
    connection = get_db_connection()
    connection.execute('DELETE from posts WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    flash('"{}" was successfully deleted.'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    joke = pyjokes.get_joke(language="en", category="neutral")

    return render_template('about.html', joke=joke)