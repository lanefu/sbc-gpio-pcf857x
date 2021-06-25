import argparse
import gpio
import http
from flask import Flask, abort

app = Flask(__name__)
gpios = None

@app.route("/on")
def on():
    gpios.set_all(True)
    return '', http.HTTPStatus.NO_CONTENT

@app.route("/off")
def off():
    gpios.set_all(False)
    return '', http.HTTPStatus.NO_CONTENT

@app.route("/toggle")
def toggle_all():
    gpios.toggle_all()
    return '', http.HTTPStatus.NO_CONTENT

@app.route("/<int:line>/toggle")
def toggle(line):
    try:
        gpios.toggle(line)
        return '', http.HTTPStatus.NO_CONTENT
    except KeyError:
        abort(http.HTTPStatus.NOT_FOUND)

@app.route("/bounce")
def bounce_all():
    gpios.bounce_all(5)
    return '', http.HTTPStatus.NO_CONTENT

@app.route("/<int:line>/bounce")
def bounce(line):
    try:
        gpios.bounce(line, 5)
        return '', http.HTTPStatus.NO_CONTENT
    except KeyError:
        abort(http.HTTPStatus.NOT_FOUND)

@app.route("/state")
def state_all():
    return gpios.get_all(), http.HTTPStatus.OK

@app.route("/<int:line>/state")
def state(line):
    return gpios.get(line), http.HTTPStatus.OK

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Drive GPIOs')
    parser.add_argument('--chip', '-c',
        default = '/dev/gpiochip0', help='gpio chip device file')
    parser.add_argument('--lines', '-l', nargs='+', type=int,
        default = [0], help='gpio lines')

    args = parser.parse_args()

    gpios = gpio.armbianGpios(args.chip, args.lines)

    app.run("0.0.0.0")
