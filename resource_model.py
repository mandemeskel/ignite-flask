#!/usr/bin/python
# -*- coding: ascii -*-
# the basics
import logging
from random import random

# Google stuff
# noinspection PyUnresolvedReferences
from google.appengine.ext import ndb

# Import the Flask Framework
from flask import Flask, render_template, request, Response
# noinspection PyUnresolvedReferences
from flask_restful import Resource, Api, reqparse

# Import to allow crossdomain requests
from crossdomain import crossdomain

# Our stuff
from rest_model import RestApi, RestsApi, RestModel



app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True
RESOURCE_NAMES = [
    "Step 1/0: How to finish",
    "Go west young man",
    "A square deal for everyone",
    "Answers? No, you need questions",
    "There is no 'no' in Amharic",
    "How to create happiness"
]
RESOURCE_LINKS = [
    "http://mta.io",
    "https://www.google.com/",
    "http://example.com/",
    "http://www.csszengarden.com/132/",
    "http://obduction.com/",
    "https://startuplaunchlist.com/"
]
RESOURCE_DESCRIPTIONS = [
    "In your next letter I wish you'd say \nwhere you are going and what you are doing;",
    "how are the plays and after the plays \nwhat other pleasures you're pursuing:",

    "taking cabs in the middle of the night, \ndriving as if to save your soul",
    "where the road gose round and round the park \nand the meter glares like a moral owl,",

    "and the trees look so queer and green \nstanding alone in big black caves"
    "and suddenly you're in a different place \nwhere everything seems to happen in waves,",

    "and most of the jokes you just can't catch,  \nlike dirty words rubbed off a slate,",
    "and the songs are loud but somehow dim \nand it gets so teribly late,",

    "and coming out of the brownstone house \nto the gray sidewalk, the watered street,",
    "one side of the buildings rises with the sun \nlike a glistening field of wheat.",

    "--Wheat, not oats, dear. I'm afraid \nif it's wheat it's none of your sowing, ",
    "nevertheless I'd like to know \nwhat you are doing and where you are going."
]



class ErrorMsg( object ):
    def __init__( self, msg="", **kwargs ):
        # self.status = status
        self.msg = msg
        self.dct = { "msg": msg }
        self.dct = { "status": False }
        for key, value in kwargs.iteritems():
            self.dct[ key ] = value


    def to_dict( self ):
        return self.dct


    # overload '==' operator for backwards compatibility
    def __eq__( self, other ):
        if other is False:
            return True

        return super( ErrorMsg, self ).__eq__( other )



class ResourceTypes( object ):
    def __init__(self):
        pass

    @property
    def types(self):
        return [
            "community", "multimedia", "other",
            "pictures", "text", "undefined", "video"
        ]

    @property
    def community(self):
        return "community"

    @property
    def multimedia(self):
        return "multimedia"

    @property
    def other(self):
        return "other"

    @property
    def pictures(self):
        return "pictures"

    @property
    def text(self):
        return "text"

    @property
    def undefined(self):
        return "undefined"

    @property
    def video(self):
        return "video"


RESOURCE_TYPES = ResourceTypes()



class ModelTypes( object ):
    def __init__( self ):
        pass

    @property
    def launchlist( self ):
        return "Launchlist"


    @property
    def member( self ):
        return "Member"


    @property
    def resource( self ):
        return "Resource"


    @property
    def tag( self ):
        return "Tag"


    @property
    def topic( self ):
        return "Topic"



class ResourceModel( RestModel ):
    # url to the resource
    link = ndb.StringProperty( required=True )
    # type of media
    resource_type = ndb.StringProperty( required=True )
    # when the resource was last scraped
    last_crawl_date = ndb.DateProperty()
    # picture preview of the resource, url to picture
    preview = ndb.StringProperty()
    # launchlists the resource is in
    launchlists = ndb.KeyProperty( repeated=True )
    num_launchlists = ndb.ComputedProperty(
        lambda self: len(self.launchlists) )


    # Checks to see if key is an actual entity key
    @classmethod
    def check_key( cls,
                   urlsafe_key,
                   return_model=False,
                   check_model_type="" ):
        try:
            model = ndb.Key( urlsafe=urlsafe_key ).get()
        except Exception as exception:
            return ErrorMsg(
                msg="cant get model from key",
                log=exception.message,
                exception=exception.__class__.__name__
            )

        # make sure we are editing the right type of model
        if check_model_type != "" and check_model_type is not False:
            # check model type against the calling cls
            if check_model_type is True:
               check_model_type = type( cls ).__name__

            if not type( model ).__name__ is not check_model_type:
                return ErrorMsg(
                    msg="model does not match model_type",
                    log="model type: " + type( model ).__name__
                    + " looking for model type: " + check_model_type
                )

        # TODO: check if this "if" is redundant
        if return_model:
            if model is None:
                return ErrorMsg(
                    msg="key returned no model"
                )

            return model

        return True


    # Create an instance of ResourceModel
    # return the instance
    @classmethod
    def create( cls, data ):
        if data[ "resource_type" ] not in RESOURCE_TYPES.types:
            return False

        resource = cls(
            name=data[ "name" ],
            link=data[ "link" ],
            resource_type=data[ "resource_type" ]
        )

        try:
            key = resource.put()
        except Exception:
            return False

        return key.urlsafe()


    # Create dummy resources for a launchlist
    # return a list of resources' dicts
    @classmethod
    def create_dummy_data( cls, launchlist ):
        resource_dicts = []
        num_lists = int( (random() * 100) % 15)

        for num in range( 0, num_lists ):
            name = RESOURCE_NAMES[
                int( (random() * 100 ) % len( RESOURCE_NAMES ) )
            ]
            description = RESOURCE_DESCRIPTIONS[
                int( (random() * 100 ) % len( RESOURCE_DESCRIPTIONS ) )
            ]
            link = RESOURCE_LINKS[
                int( (random() * 100 ) % len( RESOURCE_LINKS ) )
            ]
            resource_type = RESOURCE_TYPES.types[
                int((random() * 100) % len(RESOURCE_TYPES.types) )
            ]

            resource = cls(
                name=name,
                description=description,
                link=link,
                resource_type=resource_type
            )

            # add launchlist to resource's list of launchlists
            added = resource.edit_launchlist(
                launchlist, add=True, safe=True )

            if not added:
                continue

            # save resource
            resource.put()
            resource_dicts.append( resource.to_dict(
                includes=[ "name", "description", "link", "resource_type", "rating"]
            ) )

            # add resource to launchlists list of resources
            launchlist.edit_resources( resource, add=True, safe=True )

        # save launchlist
        launchlist.put()

        return resource_dicts



    # Return list of properties to exclude from to_dict
    @classmethod
    def get_excludes( cls, new_excludes=None ):
        if new_excludes is not None:
            new_excludes = new_excludes.extend( ["launchlists"] )
        else:
            new_excludes = ["launchlists"]

        return super(ResourceModel, cls).get_excludes(
            new_excludes
        )


    # Return list of necessary properties to create ResourceModel
    @classmethod
    def get_required_properties( cls, new_requires=None ):
        if new_requires is not None:
            new_requires = new_requires.extend( ["link", "resource_type"] )
        else:
            new_requires = ["link", "resource_type"]

        return super(ResourceModel, cls).get_required_properties(
            new_requires
        )


    # Delete model from database
    # return bool
    def delete( self ):
        # remove references to resource from launchlists
        for launchlist in self.launchlists:
            launchlist.edit_resources(
                resource=self,
                add=False,
                safe=True
            )
        return super( ResourceModel, self ).delete()


    # Converts model into json friendly dict
    # return dict
    def to_dict( self,
                 object_props=None,
                 includes=None,
                 excludes=None ):
        return super(ResourceModel, self).to_dict(
            object_props, includes, excludes
        )


    # Updates model with new data
    # returns bool
    def update( self, data ):
        return super(ResourceModel, self).update( data )


    # Add/Remove resource from launchlist
    # return bool
    def edit_launchlist( self, launchlist, add=True, safe=False ):
        if safe is False:
            if type( launchlist ).__name__ != "Launchlist":
                return False

        new_list = self.edit_list( self.launchlists, launchlist.key, add )

        if new_list is False:
            return False

        self.launchlists = new_list

        return True


# TODO: throws "working outside of request context" error
# # parse arguments that are sent with requests
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



class ResourceApi( RestApi ):
    model_class = ResourceModel

    @classmethod
    def post( cls, urlsafe_key="", add_remove="", launchlist_key="" ):
        if add_remove == "":
            return super( ResourceApi, cls ).post( urlsafe_key )

        if launchlist_key == "":
            return cls.make_response_dict(
                status=False,
                msg="bad launchlist key"
            ), 400

        launchlist = cls.model_class.check_key(
            urlsafe_key=launchlist_key,
            return_model=True,
            check_model_type=ModelTypes().launchlist
        )

        if launchlist == False:
            return launchlist.to_dict(), 400

        if add_remove == "add":
            success = cls.model_class.edit_launchlist(
                launchlist=launchlist,
                add=True,
                safe=True
            )
        elif add_remove == "remove":
            success = cls.model_class.edit_launchlist(
                launchlist=launchlist,
                add=False,
                safe=True
            )
        else:
            success = launchlist.key in cls.model_class.launchlists
            return cls.make_response_dict(
                status=True,
                msg="Is launchlist in resource: " + str( success ),
                is_in=success
            )

        if success is True:
            return { "status": True }, 200
        elif isinstance( success, ErrorMsg ):
            return success.to_dict(), 400
        else:
            return { "status": False }, 400




class ResourcesApi( Resource ):
    model_class = ResourceModel
    # TODO: this should be a attribute of super class, RestApi
    MODEL_TYPES = ModelTypes()

    @classmethod
    def get( cls, model_type="", urlsafe_key="" ):
        if model_type == "":
            return {
                "status": False,
                "msg": "provide a model_type to get resources from"
            }, 400
        elif urlsafe_key == "":
            return {
                "status": False,
                "msg": "provide key to get the resource from"
            }, 400

        # get resources belonging to this launchlist
        if model_type == cls.MODEL_TYPES.launchlist.lower():
            launchlist = cls.model_class.check_key(
                urlsafe_key=urlsafe_key,
                return_model=True,
                check_model_type=model_type
            )

            if launchlist == False:
                return launchlist.to_dict(), 400

            resources = launchlist.resources

            if DEVELOPING:
                logging.log( logging.INFO, len(resources) )

            if resources == []:
                resources_dcts = cls.model_class.create_dummy_data(
                    launchlist=launchlist
                )

                if DEVELOPING:
                    logging.log( logging.INFO, "creating dummy sources" )
            else:
                resources_dcts = cls.model_class.convert_keys_to_dicts(
                    resources,
                    includes=[ "name", "description", "rating", "link" ]
                )

                if DEVELOPING:
                    logging.log( logging.INFO, "getting sources" )

            return {
                "status": True,
                "resources": resources_dcts
            }, 200

        elif model_type == cls.MODEL_TYPES.topic.lower():
            return {
                "status": True,
                "msg": "endpoint not implemented for model " + model_type
            }, 501
        elif model_type == cls.MODEL_TYPES.tag.lower():
            return {
                "status": True,
                "msg": "no " + model_type
            }, 501
        elif model_type == cls.MODEL_TYPES.member.lower():
            return {
                "status": True,
                "msg": "no " + model_type
            }, 501
        else:
            return {
                "status": False,
                "msg": "bad model type " + model_type
            }, 400
