from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/me')
def about():
    return render_template("1.html")

@app.route('/contact')
def contact():
    if request.method == "GET":
        return render_template("2.html")
    elif request.method == "POST":
        message = request.form['message']
        print(message)