import os
from werkzeug.contrib.fixers import ProxyFix

from app import create_app, socketio

def fix_werkzeug_logging():
    from werkzeug.serving import WSGIRequestHandler

    def address_string(self):
        forwarded_for = self.headers.get(
            'X-Forwarded-For', '').split(',')

        if forwarded_for and forwarded_for[0]:
            return forwarded_for[0]
        else:
            return self.client_address[0]

    WSGIRequestHandler.address_string = address_string

config_name = os.getenv('FLASK_ENV')
app = create_app(config_name)

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    socketio.run(app)

    
