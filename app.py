from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', 'pass'),
    os.getenv('DB_HOST', 'flask_mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Run server:
# First method: python app.py (app.run needs to be included, like the if statement below)
# Second method: flask run (after exporting 2 env variables:
# export FLASK_ENV=development, export FLASK_APP=app.py)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=["GET"])
def index():
    t = Todo.query.all()
    return render_template("index.html", list_todo=t)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    #db.create_all()
    app.run(host=os.getenv('IP', '0.0.0.0'), debug=True)
    # app.run(host=os.getenv('IP', '0.0.0.0'), debug=True,
    #         port=int(os.getenv('PORT', 4444)))
