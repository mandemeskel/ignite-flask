'''
appengine - all options
https://cloud.google.com/appengine/docs/python/oauth/

appengine - user
https://cloud.google.com/appengine/docs/python/users/

firebase
https://firebase.google.com/docs/auth/web/manage-users

flask
https://flask-login.readthedocs.io/en/latest/

'''
import logging

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
from rest_model import RestApi, RestsApi, RestModel, ErrorMsg, ModelTypes, RESOURCE_TYPES



class Member( RestModel ):
    # launchlists belonging to the member
    launchlists = ndb.KeyProperty( repeated=True )
    num_launchlists = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )
    # resources belonging to the member
    resources = ndb.KeyProperty( repeated=True )
    num_resources = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )
    # following_launchlist
    following_launchlist = ndb.KeyProperty( repeated=True )
    num_following_launchlist = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )
    # following_topics
    following_topics = ndb.KeyProperty( repeated=True )
    num_following_topics = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )


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


    # Create dummy resources for a launchlist
    # return a list of resources' dicts
    @classmethod
    def create_dummy_data( cls, launchlist ):
        pass



    # Return list of properties to exclude from to_dict
    @classmethod
    def get_excludes( cls, new_excludes=None ):
        excludes = [ "launchlists", "resources", "following_topics",
                     "following_launchlists" ]
        if new_excludes is not None:
            new_excludes = new_excludes.extend( excludes )
        else:
            new_excludes = excludes

        return super( cls, cls ).get_excludes(
            new_excludes
        )


    # Return list of necessary properties to create ResourceModel
    @classmethod
    def get_required_properties( cls, new_requires=None ):
        requires = ["email"]
        if new_requires is not None:
            new_requires = new_requires.extend( requires )
        else:
            new_requires = requires

        return super( cls, cls ).get_required_properties(
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
        return super( Member, self ).delete()


    # Converts model into json friendly dict
    # return dict
    def to_dict( self,
                 object_props=None,
                 includes=None,
                 excludes=None ):
        return super( Member, self ).to_dict(
            object_props, includes, excludes
        )


    # Updates model with new data
    # returns bool
    def update( self, data ):
        return super( Member, self ).update( data )


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



class MemberApi( RestApi ):
    model_class = Member



class MemberApis( Resource ):
    model_class = Member




