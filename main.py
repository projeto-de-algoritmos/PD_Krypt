from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
from random import randint

import math

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def pagina_principal():
    texto = request.form.get("texto")
    if texto:
        return redirect(url_for('resultados', texto=texto))

    return render_template("pagina_principal.html")


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


def gerarDadosPublicKey(privateKey):
    mod = privateKey.pop()
    mult = privateKey.pop()

    while mod != 1 and mult != 1 and math.gcd(mod, mult) != 1:
        mult = randint(0, mult)

    publicKey = []
    for i in privateKey:
        publicKey.append((i * mult) % mod)

    return (mult, mod, publicKey)


def codificarTexto(publicKey, texto):
    textoBinario = texto.encode("utf8")

    textoCriptografado = []
    for byte in textoBinario:
        codigo = format(byte, '#010b')[2:]

        posicao = 0
        while posicao < 8:
            if not posicao:
                textoCriptografado.append(0)
            if codigo[posicao] == '1':
                posicaoSendoCifrada = len(textoCriptografado) - 1

                codigoCifrado = textoCriptografado[posicaoSendoCifrada]
                novoCodigoCifrado = codigoCifrado + publicKey[posicao]

                textoCriptografado[posicaoSendoCifrada] = novoCodigoCifrado

            posicao = posicao + 1

    return textoCriptografado


def knapsack(codigo, privateKey):
    if codigo == 0:
        return '00000000'

    reversePrivateKey = privateKey.copy()
    reversePrivateKey.reverse()

    print(codigo, reversePrivateKey)

    binarioDecodificado = ''
    for componenteChave in reversePrivateKey:
        if componenteChave <= codigo:
            binarioDecodificado = str(1) + binarioDecodificado
            codigo = codigo - componenteChave
        else:
            binarioDecodificado = str(0) + binarioDecodificado

    return binarioDecodificado


def decodificarMensagem(mensagem, privateKey, multiplicador, modulo):
    inversoMultiplicativoModular = pow(multiplicador, -1, modulo)

    print(mensagem)
    print(privateKey)

    binarios = []
    for codigo in mensagem:
        binario = knapsack(
            (codigo * inversoMultiplicativoModular) % modulo, privateKey
        )

        binarios.append(int(binario, 2))

    return bytes(binarios).decode("utf8")


@app.route('/resultados/<texto>', methods=["GET", "POST"])
def resultados(texto):
    privateKey = gerarSequenciaSuperCrescimento()

    dadosPublicKey = gerarDadosPublicKey(privateKey)

    multiplicador = dadosPublicKey[0]
    modulo = dadosPublicKey[1]
    publicKey = dadosPublicKey[2]

    textoCriptografado = codificarTexto(publicKey, texto)

    componentesTextoCriptografado = []
    for componente in textoCriptografado:
        componentesTextoCriptografado.append(componente % 256)

    print(bytes(componentesTextoCriptografado).decode("utf8", "replace"))

    textoDescriptografado = decodificarMensagem(
        textoCriptografado, privateKey, multiplicador, modulo
    )

    print(textoDescriptografado)

    return render_template("resultados.html", data=textoDescriptografado)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
