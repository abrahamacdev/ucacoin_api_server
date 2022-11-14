# This is a sample Python script.
import bottle
from bottle import route, run, template


@route('/hello/<name>')
def index(name):
    name + 123
    return template('<b>Hello {{name}}</b>!', name=name)


if __name__ == "__main__":

    app = bottle.Bottle()

    # app.route(#endpoint, #métodoHTTP, #claseControladora.metodo)

    # Lanzamos la app
    run(app, host='localhost', port=8080)