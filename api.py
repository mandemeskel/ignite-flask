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


@app.route( "/api/topics", methods=["GET"] )
def get_topics():
	pass



# Topic model handlers
'''
Handles DELETE request
'''
@app.route( "/api/topic/<topic>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_topic( topic ):
	pass


'''
Handles GET request
'''
@app.route( "/api/topic/<topic>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/topic/<topic>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_topic( topic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/topic/<topic>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_topic( topic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/topic/<topic>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_topic( topic ):
	pass



# Sub-Topic 
'''
Handles DELETE request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_topic( topic ):
	pass


'''
Handles GET request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_topic( topic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_topic( topic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_topic( topic ):
	pass



# Resource model handlers
'''
Handles DELETE request
'''
@app.route( "/api/resource/<resource>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_topic( topic ):
	pass


'''
Handles GET request
'''
@app.route( "/api/resource/<resource>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/resource/<resource>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_topic( topic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/resource/<resource>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_topic( topic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/resource/<resource>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_topic( topic ):
	pass



# Launchlist 
'''
Handles DELETE request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_topic( topic ):
	pass


'''
Handles GET request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_topic( topic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_topic( topic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_topic( topic ):
	pass



# Account 
'''
Handles DELETE request
'''
@app.route( "/api/account/<account>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_topic( topic ):
	pass


'''
Handles GET request
'''
@app.route( "/api/account/<account>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/account/<account>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_topic( topic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/account/<account>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_topic( topic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/account/<account>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_topic( topic ):
	pass


