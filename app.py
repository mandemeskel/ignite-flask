# the basics
import logging

# Import the Flask Framework
from flask import Flask, render_template, request, Response
# noinspection PyUnresolvedReferences
from flask_restful import Resource, Api, reqparse

# Import to allow crossdomain requests
from crossdomain import crossdomain

# Our stuff
from rest_model import RestApi, RestsApi
from topic_model import TopicApi, TopicsApi
from launchlist_model import LaunchlistApi, LaunchlistsApi
from resource_model import ResourceApi, ResourcesApi
from user_model import UserApi, UserApis



app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True



# parse arguments that are sent with requests
# with app.app_context():
#     request_parse = reqparse.RequestParser()
#     request_parse.add_argument(
#         "name",
#         type="string",
#         help="name can't be converted",
#         location="form"
#     )
#     # NOTE: cant use reqparse on url arguments
#     request_parse.add_argument(
#         "model_type",
#         type="url",
#         help="name can't be converted",
#         location="headers"
#     )
#     request_args = request_parse.parse_args()


# requests that will be routed to the RestModel class
api.add_resource(
    RestApi,
    "/app/test/<urlsafe_key>",
    "/app/test"
)

# requests that will be routed to the RestModel class
api.add_resource(
    TopicApi,
    "/app/topic/<urlsafe_key>",
    "/app/topic"
)

# NOTE: there is no default boolean converter
# NOTE: http://werkzeug.pocoo.org/docs/0.11/routing/
# TODO: remove includes and excludes url params
api.add_resource(
    TopicsApi,
    "/app/topics/<int:num>",
    "/app/topics"
)

api.add_resource(
    LaunchlistApi,
    "/app/launchlist/<urlsafe_key>",
    "/app/launchlist"
)

api.add_resource(
    LaunchlistsApi,
    "/app/launchlists/<urlsafe_key>",
    "/app/launchlists/<urlsafe_key>/<string:list_type>"
)

api.add_resource(
    ResourceApi,
    "/app/resource/<string:urlsafe_key>/<string:add_remove>/<string:launchlist_key>",
    "/app/resource/<string:urlsafe_key>",
    "/app/resource"
)

api.add_resource(
    ResourcesApi,
    "/app/resources/<string:urlsafe_key>",
    "/app/resources/<string:model_type>/<string:urlsafe_key>"
)

api.add_resource(
    UserApi,
    "/app/user/<string:urlsafe_key>/<string:list_name>",
    "/app/user/<string:urlsafe_key>"
)
