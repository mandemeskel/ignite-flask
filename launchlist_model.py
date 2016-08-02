# the basics
import logging

# Google stuff
from google.appengine.ext import ndb

# Import the Flask Framework
from flask import Flask, render_template, request, Response
from flask_restful import Resource, Api

# Import to allow crossdomain requests
from crossdomain import crossdomain

# Our stuff
from rest_model import RestApi, RestModel, RESPONSE_STATUS

app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True


class LaunchList( RestModel ):
    pass



class LaunchListApi( RestApi ):
    pass



class LaunchListsApi( RestApi ):
    pass


api.add_resource( LaunchListApi,
    "/launchlist/<urlsafe_key"
)

api.add_resource( LaunchListsApi,
    "/topics/<urlsafe_key>"
)
