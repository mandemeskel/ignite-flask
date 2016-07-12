'''
	RESTfull API
'''
# the basics
import logging
import json

# Datastore models
from models import TopicModel, SubscriberModel

# Google APIs
from google.appengine.api import search
from google.appengine.api import mail

# Import the Flask Framework
from flask import Flask, render_template, request, Response

# Import library to allow crossdomain requests
from crossdomain import crossdomain

app = Flask(__name__)
app.debug = True
DEVELOPING = True

@app.route( "/api/topics", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topics():
	topics = TopicModel.get_topics();

	if len( topics ) > 0:
		result = {
			"status" : True,
			"topics" : []
		}

		# TODO: move this logic to models.py
		for topic in topics:
			topic_dict = topic.to_dict()
			topic_dict["key"] = topic.key.urlsafe()
			result["topics"].append( topic_dict )

	else:
		result = {
			"status" : False,
			"msg" : "no topics found :?"
		}

	return json.dumps( result )


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
@app.route( "/api/topic/<topic_key>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_topic( topic_key ):
	entity = TopicModel.get_topic( topic_key )
	return json.dumps( entity )

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
@app.route( "/api/subtopic/<subtopic_key>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_subtopic( subtopic_key ):
	pass


'''
Handles GET request
'''
@app.route( "/api/subtopic/<subtopic_key>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_subtopic( subtopic_key ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_subtopic( subtopic ):
	pass


'''
Handles POST request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_subtopic( subtopic ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/subtopic/<subtopic>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_subtopic( subtopic ):
	pass



# Resource model handlers
'''
Handles DELETE request
'''
@app.route( "/api/resource/<resource>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_resource( resource ):
	pass


'''
Handles GET request
'''
@app.route( "/api/resource/<resource>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_resource( resource ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/resource/<resource>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_resource( resource ):
	pass


'''
Handles POST request
'''
@app.route( "/api/resource/<resource>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_resource( resource ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/resource/<resource>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_resource( resource ):
	pass



# Launchlist
'''
Handles DELETE request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_launchlist( launchlist ):
	pass


'''
Handles GET request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_launchlist( launchlist ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_launchlist( launchlist ):
	pass


'''
Handles POST request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_launchlist( launchlist ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/launchlist/<launchlist>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_launchlist( launchlist ):
	pass



# Account
'''
Handles DELETE request
'''
@app.route( "/api/account/<account>", methods=["DELETE"] )
# @crossdomain(origin='*',  methods=["DELETE"])
def delete_account( account ):
	pass


'''
Handles GET request
'''
@app.route( "/api/account/<account>", methods=["GET"] )
# @crossdomain(origin='*',  methods=["GET"])
def get_account( account ):
	pass


'''
Handles OPTIONS request
'''
@app.route( "/api/account/<account>", methods=["OPTIONS"] )
# @crossdomain(origin='*',  methods=["OPTIONS"])
def options_account( account ):
	pass


'''
Handles POST request
'''
@app.route( "/api/account/<account>", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def post_account( account ):
	pass


'''
Handles PUT request
'''
@app.route( "/api/account/<account>", methods=["PUT"] )
# @crossdomain(origin='*',  methods=["PUT"])
def update_account( account ):
	pass


# Misc handlers
'''
Handles POST request
'''
@app.route( "/api/subscribe", methods=["POST"] )
# @crossdomain(origin='*',  methods=["POST"])
def add_subscriber():
	if DEVELOPING:
		logging.log( logging.INFO, "add_subscriber: " + str( request.form ) )

	if "email" not in request.form:
		return json.dumps( {
							"status" : False,
							"msg" : "no email found"
		} )

	# TODO: validate email
	subscriber = SubscriberModel( email = request.form["email"] )

	# TODO: saving to ndb, exception wrap this
	# TODO: should call custom put method that validates, checks for duplicates etc.
	if subscriber.put():
		if DEVELOPING:
			logging.log( logging.INFO, "saved subscriber" )
		return json.dumps( { "status" : True })
	else:
		if DEVELOPING:
			logging.log( logging.INFO, subscriber.put() )
			return json.dumps( {
								"status" : False,
								"msg" : "failed to save"
			} )
