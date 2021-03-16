from flask import request, redirect, url_for, session
from flask_mako import render_template

from app import app, db
from app.models import Todo

pages = {
    'ToDo List':'/',
    'ToDo Visits':'/visits',
}

html_escape_table = {
    '&': '&amp;',
    '"': '&quot;',
    "'": '&apos;',
    '>': '&gt;',
    '<': '&lt;'
}

def strip(d):
    safe = {}
    for k, v in d.items():
        v = "".join(html_escape_table.get(c, c) for c in v)
        safe.update({k:v})

    return safe

@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete, pages=pages)

@app.route('/visits')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('visits.html', visits=session.get('visits'), pages=pages)

@app.route('/visits/delete')
def del_visits():
    session.pop('visits', None)
    return redirect(url_for('visits'))

@app.route('/add', methods=['POST'])
def add():
    safe_request = strip(request.form)
    todo = Todo(text=safe_request['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))
