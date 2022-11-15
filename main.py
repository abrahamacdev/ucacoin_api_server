# This is a sample Python script.
from controllers import users
from bottle import Bottle, route, run, template


@route('/hello/<name>')
def index(name):
    name + 123
    return template('<b>Hello {{name}}</b>!', name=name)


def setup_routes():
    app = Bottle()

    # Relacionado con los usuarios
    app.route('/login', 'POST', users.login)    # En local, nada de JWT
    #app.route('/registro', 'POST', users.registro)
    #app.route('/logout', 'POST', users.logout)

    # Relacionado con historial
    #app.route('/historial', 'GET', transactions.history)
    #app.route('/balance', 'GET', transactions.actual_balance)

    # Relacionado con transacciones
    #app.route('/enviar', 'POST', transactions.send)

    return app

if __name__ == "__main__":

    # COnfiguramos el enrutamiento de las peticiones
    app = setup_routes()

    # Lanzamos la app
    run(app, host='localhost', port=8080)
