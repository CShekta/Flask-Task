from flask import Flask, render_template
from flask.ext.script import Manager, Server

app = Flask(__name__)

manager = Manager(app)
manager.add_command('FlaskTask', Server(port=5000, host='0.0.0.0'))

from FlaskTask import views
