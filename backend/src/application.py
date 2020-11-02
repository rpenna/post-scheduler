from flask import Flask
from flask_mongoengine import MongoEngine

from src.controllers.user_controller import UserController

db_host = {
    'production': 'mongodb://localhost/posts',
    'test': 'mongomock://localhost/posts'
}
def create_app(db_host_type: str = 'production') -> Flask:
    """Creates Flask app

    Args:
        db_host_type (str, optional): Desired database settings. Defaults to 'production'.

    Returns:
        Flask: Flask app
    """
    database = MongoEngine()
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': 'posts',
        'host': db_host[db_host_type]
    }

    database.init_app(app)

    app.add_url_rule('/user', methods=['POST'], view_func=UserController().create_user)

    return app
 