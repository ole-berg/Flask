import os

from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import flask_monitoringdashboard as dashboard

app = Flask(__name__)
dashboard.bind(app)


@app.route("/", methods=['GET'])
def hello_world():
    return "Hallo Welt!"


@app.route("/<name>")
def hello_name(name):
    return f"Hallo {name}!"


@app.route("/html/<name>")
def hello_html(name):
    return render_template("hello.html", name=name)


@app.route("/createUser", methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template("form.html")
    else:
        return f"<h1>Benutzer mit dem Benutzernamen {escape(request.form['username'])} angelegt</h1>"


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET' or request.files['file'] is None:
        return render_template('upload.html')
    else:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
            return redirect(url_for('show', file_name=uploaded_file.filename))


@app.route('/photo/<file_name>')
def show(file_name):
    full_filename = "../"+file_name
    return render_template('img.html', file_name=file_name)


if __name__ == '__main__':
    app.run(debug=True)
