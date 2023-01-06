from bottle import Bottle, response

from controllers import users
from controllers import transactions

app = Bottle()

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


def setup_routes():
    # Relacionado con los usuarios
    app.route('/login', 'POST', users.login)  # En local, nada de JWT
    app.route('/registro', 'POST', users.register)
    app.route('/logout', 'POST', users.logout)

    # Relacionado con historial
    app.route('/historial', 'GET', transactions.history)
    app.route('/balance', 'GET', transactions.actual_balance)

    # Relacionado con transacciones
    app.route('/enviar', 'POST', transactions.send)

    return app
