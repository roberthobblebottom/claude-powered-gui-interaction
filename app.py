
from flask import Flask, render_template, request


import os
app = Flask(__name__)

@app.route("/")
def hello_world():
    print(os.system("ls"))
    return render_template("index.html")


@app.route("/click_event/", methods=["POST"])
def click_event():
    button_clicked = request.form.get('button')
    print('button_clicked',button_clicked)
    return render_template('click_event.html',button_clicked = button_clicked)

if __name__ == "__main__":
    app.run()