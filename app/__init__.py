from flask import Flask
from .config import app_config
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=False)
	app.config.from_object(app_config[config_name])

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	socketio.init_app(app)

	return app