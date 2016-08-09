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


DEVELOPING = True


class User( RestModel ):

    # user's email
    email = ndb.StringProperty()
    # user password
    password = ndb.StringProperty()
    # use'r role
    role = ndb.IntegerProperty( default=0 )
    # use'r rating
    rating = ndb.IntegerProperty( default=0 )
    # topics belonging to the User
    topics = ndb.KeyProperty( repeated=True )
    num_topics = ndb.ComputedProperty(
        lambda self: len( self.topics ) )
    # launchlists belonging to the User
    launchlists = ndb.KeyProperty( repeated=True )
    num_launchlists = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )
    # resources belonging to the User
    resources = ndb.KeyProperty( repeated=True )
    num_resources = ndb.ComputedProperty(
        lambda self: len( self.resources ) )
    # following_launchlists
    following_launchlists = ndb.KeyProperty( repeated=True )
    num_following_launchlists = ndb.ComputedProperty(
        lambda self: len( self.following_launchlists ) )
    # following_topics
    following_topics = ndb.KeyProperty( repeated=True )
    num_following_topics = ndb.ComputedProperty(
        lambda self: len( self.following_topics ) )

    # firebase user id
    uid = ndb.StringProperty( required=True )


    # photo_url = ndb.StringProperty()



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


    @classmethod
    def create( cls, data ):
        name = data[ "name" ]
        email = data[ "email" ]
        description = data[ "description" ]
        uid = data[ "uid" ]

        model = cls(
            name=name,
            description=description,
            email=email,
            uid=uid
        )

        key = model.put()
        if key == False:
            return { "status": False, "msg": "failed to save" }, 400

        return key.urlsafe()

    # Create dummy resources for a launchlist
    # return a list of resources' dicts
    @classmethod
    def create_dummy_data( cls, launchlist ):
        pass


    # Return list of properties to exclude from to_dict
    @classmethod
    def get_excludes( cls, new_excludes=None ):
        excludes = [ "launchlists", "resources",
                     "topics", "following_topics",
                     "following_launchlists", "uid" ]
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
        requires = [ "name", "email", "uid" ]
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
        # remove references to user in other objects
        lists = [
            self.launchlists, self.topics, self.resources,
            self.following_launchlists, self.following_topics
        ]
        models_to_update = []
        for a_list in lists:
            for model in a_list:
                # TODO: create remove_user method
                model.remove_user( self.key )
                models_to_update.append( model )

        ndb.put_multi( models_to_update )
        return super( User, self ).delete()


    # Converts model into json friendly dict
    # return dict
    def to_dict( self,
                 object_props=None,
                 includes=None,
                 excludes=None ):
        return super( User, self ).to_dict(
            object_props, includes, excludes
        )


    # Updates model with new data
    # returns bool
    def update( self, data ):
        # if "name" in data:
        #     if data[ "name" ] != self.name:
        #         self.name = data[ "name" ]
        #
        #
        return super( User, self ).update( data )


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


    # edit_list()



class UserApi( RestApi ):

    model_class = User

    @classmethod
    def delete( cls, urlsafe_key="" ):
        if urlsafe_key == "":
            return  { "status": False, "msg": "need valid user key" }, 400

        user = cls.model_class.check_key(
            urlsafe_key=urlsafe_key,
            return_model=True,
            check_model_type="User"
        )

        if user == False:
            return user.to_dict(), 400

        success = user.delete()

        if success == False:
            return { "status": False, "msg": "failed to delete user" }, 500

        return  { "status": True }, 200


    @classmethod
    def get( cls, urlsafe_key="", list_name="" ):
        if urlsafe_key == "":
            return  { "status": False, "msg": "need valid user key" }, 400

        if list_name == "":
            user = cls.model_class.check_key(
                urlsafe_key=urlsafe_key,
                return_model=True,
                check_model_type="User"
            )

            if user == False:
                return user.to_dict(), 400

            # unauthenticated users and other users
            user_dict = user.to_dict( includes=[
                "name", "description", "rating", "num_topics",
                "num_launlishts", "num_resources", "num_following_topics",
                "num_following_launchlists", "date_created", "date_updated"
            ] )

            # admins and the user
            # user_dict = user.to_dict()
            return { "status": True, "user": user_dict }, 200


    @classmethod
    def post( cls, urlsafe_key="" ):
        if urlsafe_key == "":
            return  { "status": False, "msg": "need valid user key" }, 400

        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        if urlsafe_key == "":
            return  { "status": False, "msg": "need valid user key" }, 400

        user = cls.model_class.check_key(
            urlsafe_key=urlsafe_key,
            return_model=True,
            check_model_type="User"
        )

        if user == False:
            return user.to_dict(), 400

        list_operations = [
            "add_resources", "remove_resources",
            "add_launchlists", "remove_launchlists",
            "add_topics", "remove_topics",
            "follow_launchlists", "leave_launchlists",
            "follow_topics", "leave_topics"
        ]

        for operation in list_operations:
            if operation not in data:
                continue

            models = data[ operation ]
            data.pop( operation )

            if "add_resources" is operation:
                new_list = user.edit_list(
                    user.resources, add=True, items=models  )
                if new_list == False:
                    continue
                user.resources = new_list

            elif "remove_resources" is operation:
                new_list = user.edit_list(
                    user.resources, add=False, items=models  )
                if new_list == False:
                    continue
                user.resources = new_list

            elif "add_launchlists" is operation:
                new_list = user.edit_list(
                    user.launchlists, add=True, items=models  )
                if new_list == False:
                    continue
                user.launchlists = new_list

            elif "remove_launchlists" is operation:
                new_list = user.edit_list(
                    user.launchlists, add=False, items=models  )
                if new_list == False:
                    continue
                user.launchlists = new_list

            elif "add_topics" is operation:
                new_list = user.edit_list(
                    user.topics, add=True, items=models  )
                if new_list == False:
                    continue
                user.topics = new_list

            elif "remove_topics" is operation:
                new_list = user.edit_list(
                    user.topics, add=False, items=models  )
                if new_list == False:
                    continue
                user.topics = new_list

            elif "follow_launchlists" is operation:
                new_list = user.edit_list(
                    user.following_launchlist, add=True, items=models  )
                if new_list == False:
                    continue
                user.following_launchlist = new_list

            elif "leave_launchlists" is operation:
                new_list = user.edit_list(
                    user.following_launchlist, add=False, items=models  )
                if new_list == False:
                    continue
                user.following_launchlist = new_list

            elif "follow_topics" is operation:
                new_list = user.edit_list(
                    user.following_topics, add=True, items=models  )
                if new_list == False:
                    continue
                user.following_topics = new_list

            elif "leave_topics" is operation:
                new_list = user.edit_list(
                    user.following_topics, add=False, items=models  )
                if new_list == False:
                    continue
                user.following_topics = new_list

        # TODO: need auth for this
        success = user.update( data )

        if success == False:
            return { "status": False,
                     "msg": "failed to save user changes" }, 500
        return { "status": True }, 400


    @classmethod
    def put( cls ):
        pass



class UserApis( Resource ):

    model_class = User

    # TODO: this behaviour should go under respective models that have lists of users
    @classmethod
    def get( cls, model_type="", urlsafe_key="" ):
        pass


