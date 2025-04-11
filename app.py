from time import sleep

from flask import Flask, render_template, request
import webbrowser
import os

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/click_event/", methods=["POST"])
def click_event():
    button_clicked = request.form.get('button')
    print('button_clicked',button_clicked)
    return render_template('click_event.html',button_clicked = button_clicked)
if __name__ == "__main__":
    # os.system("pgrep -f 'python3 mouse_demo.py' | xargs kill -9 ")
    sleep(1)
    webbrowser.open_new("http://127.0.0.1:5000")
    app.run()

