import os

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import flask_monitoringdashboard as dashboard
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
dashboard.bind(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wta.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def hello_world():
    return "Hallo Welt!"


@app.route("/<name>")
def hello_name(name):
    return f"Hallo {name}!"


@app.route("/html/<name>")
def hello_html(name):
    return render_template("hello.html", name=name)


@app.route("/user/create", methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template("user/form.html")
    else:
        if not user_exists(request.form['username']):
            print(user_exists(request.form['username']))
            add_user(request.form['username'], request.form['password'])
            return f"<h1>Benutzer mit dem Benutzernamen {escape(request.form['username'])} angelegt</h1>", 200
        else:
            return "Ein Benutzer mit dem gleichen Benutzernamen existiert bereits", 400


@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)


def add_user(username, password):
    db.session.add(User(username=username, password=password))
    db.session.commit()


def user_exists(username):
    result = db.session.execute(db.select(User).filter_by(username=username)).scalars()
    return result.first() is not None


if __name__ == '__main__':
    app.run(debug=True)
