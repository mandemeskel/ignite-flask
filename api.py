'''
	RESTfull API
'''
# the basics
import logging
import json

# Google APIs
from google.appengine.api import search
from google.appengine.api import mail

# Import the Flask Framework
from flask import Flask, render_template, request, Response

# Import library to allow crossdomain requests
from crossdomain import crossdomain

app = Flask(__name__)
app.debug = True
