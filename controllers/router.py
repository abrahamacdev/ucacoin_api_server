from bottle import Bottle, route, run, template

from controllers import users


def setup_routes():
    app = Bottle()

    # Relacionado con los usuarios
    app.route('/login', 'POST', users.login)        # En local, nada de JWT
    app.route('/registro', 'POST', users.register)
    app.route('/logout', 'POST', users.logout)

    # Relacionado con historial
    # app.route('/historial', 'GET', transactions.history)
    # app.route('/balance', 'GET', transactions.actual_balance)

    # Relacionado con transacciones
    # app.route('/enviar', 'POST', transactions.send)

    return app
