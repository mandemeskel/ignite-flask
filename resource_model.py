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
from flask_restful import Resource, Api

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
    "mta.io",
    "google.com",
    "example.com",
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
    rating = ndb.IntegerProperty( default=-1 )


    # Create an instance of ResourceModel
    # return the instance
    @classmethod
    def create( cls, data ):
        if data[ "type" ] not in ResourceTypes.types:
            return False

        resource = cls(
            name=data[ "name" ],
            link=data[ "link" ],
            type=data[ "type" ]
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
            links = RESOURCE_LINKS[
                int( (random() * 100 ) % len( RESOURCE_LINKS ) )
            ]
            resource_type = RESOURCE_TYPES.types[
                int((random() * 100) % len(RESOURCE_TYPES.types) )
            ]

            resource = cls(
                name=name,
                description=description,
                links=links,
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
                includes=[ "name", "description", "link", "type", "rating"]
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
            new_requires = new_requires.extend( ["link", "type"] )
        else:
            new_requires = ["link", "type"]

        return super(ResourceModel, cls).get_required_properties(
            new_requires
        )


    # Delete model from database
    # return bool
    def delete( self ):
        return super( ResourceModel, self ).delete()


    # Converts model into json friendly dict
    # return dict
    def to_dict( self,
                 object_props=None,
                 includes=None,
                 excludes=None ):
        return super(ResourceModel, self).to_dict()


    # Updates model with new data
    # returns bool
    def update( self, data ):
        return super(ResourceModel, self).update( data )


    # Add/Remove resource from launchlist
    # return bool
    def edit_launchlist( self, launchlist, add=True, safe=False ):
        if safe is False:
            if type( launchlist ).__name__ != "LaunchList":
                return False

        new_list = self.edit_list( self.launchlists, launchlist.key, add )

        if new_list is False:
            return False

        self.launchlists = new_list

        return True



class ResourceApi( RestApi ):
    model_class = RestModel



class ResourcesApi( RestsApi ):
    model_class = RestModel


