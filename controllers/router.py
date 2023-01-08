import bottle
from bottle import Bottle, response

from bottle_cors_plugin import cors_plugin

from controllers import users
from controllers import transactions


def setup_routes():
    app = Bottle()
    app.install(cors_plugin('*'))

    # Relacionado con los usuarios
    app.route('/login', 'POST', users.login)  # En local, nada de JWT
    app.route('/login', 'OPTIONS', users.login)  # En local, nada de JWT
    app.route('/registro', 'POST', users.register)
    app.route('/logout', 'OPTIONS', users.logout)
    app.route('/logout', 'POST', users.logout)

    # Relacionado con historial
    app.route('/historial', 'POST', transactions.history)
    app.route('/historial', 'OPTIONS', transactions.history)
    app.route('/balance', 'POST', transactions.actual_balance)
    app.route('/balance', 'OPTIONS', transactions.actual_balance)

    # Relacionado con transacciones
    app.route('/enviar', 'POST', transactions.send)
    app.route('/enviar', 'OPTIONS', transactions.send)

    return app
