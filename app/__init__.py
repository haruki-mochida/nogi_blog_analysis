from flask import Flask

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = 'your-secret-key'

    app.config.from_pyfile('config.py')

    from . import views
    app.register_blueprint(views.bp)

    return app
