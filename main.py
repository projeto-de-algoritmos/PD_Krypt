from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template("home_page.html")


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
