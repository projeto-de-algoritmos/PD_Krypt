from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home_page():
    text = request.form.get("text")
    if text:
        return redirect(url_for('result', text=text))

    return render_template("home_page.html")


@app.route('/result/<text>', methods=["GET", "POST"])
def result(text):
    return render_template("result.html", data=text)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
