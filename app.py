# the basics
import logging

# Import the Flask Framework
from flask import Flask, render_template, request, Response
# noinspection PyUnresolvedReferences
from flask_restful import Resource, Api

# Import to allow crossdomain requests
from crossdomain import crossdomain

# Our stuff
from rest_model import RestApi, RestApis
from topic_model import TopicApi, TopicsApi
from launchlist_model import LaunchListApi, LaunchListsApi

app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True


api.add_resource( LaunchListApi,
    "/app/launchlist/<urlsafe_key>"
)

api.add_resource( LaunchListsApi,
    "/app/launchlists/<urlsafe_key>"
)
