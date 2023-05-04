import boto3
import botocore
import datetime
import os

from keys import *
from flask import *
from blueprints.login_signup import login_bp, signup_bp
from blueprints.files import upload_bp


app = Flask(__name__)


app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(upload_bp)

if __name__ == "__main__":
    app.run(debug=True)