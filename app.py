import secrets
from flask import Flask
import mongoengine as me
from flask_mongoengine import MongoEngine
from flask_admin import Admin

from admin import System, SystemForm, Task, TaskForm


class Settings:
  flask_env = 'dev'
  SECRET_KEY = secrets.token_hex(nbytes=24)

  MONGODB_SETTINGS = {
      "db": 'raz',
  }



def init_mongodb(app):
    app.logger.info(f'MongoDB enabled ${app.config.get("MONGODB_SETTINGS")}')
    db = MongoEngine()
    db.init_app(app)
    return db


def enable_flask_admin(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin_db = me.get_db()   # connects to DB
    admin.add_view(SystemForm(System))
    admin.add_view(TaskForm(Task))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings())
    init_mongodb(app=app)
    enable_flask_admin(app=app)
    return app


################################

def hello_world():
    return "<p>Hello, World!</p>"


def run_debug_server():
    app = create_app()
    app.add_url_rule("/", view_func=hello_world)
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_debug_server()
