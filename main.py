from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
from random import randint

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home_page():
    text = request.form.get("text")
    if text:
        return redirect(url_for('result', text=text))

    return render_template("home_page.html")


# private key
def gerarSequenciaSuperCrescimento():
    potencia, sequencia = 0, []

    while len(sequencia) != 10:
        num = randint(0, 9*pow(10, potencia))

        s = sum(sequencia)
        if num <= s:
            potencia = potencia + 1
            continue

        sequencia.append(num)

    return sequencia


@app.route('/result/<text>', methods=["GET", "POST"])
def result(text):
    privateKey = gerarSequenciaSuperCrescimento()

    return render_template("result.html", data=text)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
