from flask import Flask
import os 

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = 'progbiblioteca'

from routes import *