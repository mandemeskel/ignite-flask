# the basics
import logging
from datetime import date

# Google stuff
# noinspection PyUnresolvedReferences
from google.appengine.ext import ndb

# Import the Flask Framework
# noinspection PyUnresolvedReferences
from flask import Flask, render_template, request, Response
# noinspection PyUnresolvedReferences
from flask_restful import Resource, Api

# Import to allow crossdomain requests
from crossdomain import crossdomain

app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True



class RESPONSE_STATUS():
    failed = False
    success = True
    retry = "retry"



# TODO: needed?
def check_key( urlsafe_key, cls, return_model = False ):
    model = ndb.Key( urlsafe = urlsafe_key ).get()

    # make sure we are editing the right type of model
    if not isinstance( model, cls ):
        return False

    if return_model:
        if model is None:
            return False

        return model

    return True



class RestModel( ndb.Model ):

    # model properties
    # TODO: do not allow multiline names
    name = ndb.StringProperty(
        default="Jane Doe",
        required=True
    )
    description = ndb.TextProperty(
        default="Job description: rocket jumper!" )
    # NOTE: should use BolbKeyProperty to store icons?
    # NOTE: but if imgs are hosted elsewhere then a string works
    icon = ndb.StringProperty(
        default="../icons/apple_music_icon_trns.png"
    )

    # search realted properties
    tags = ndb.KeyProperty( repeated=True )
    num_tags = ndb.IntegerProperty( default=0 )

    # user related properties
    # TODO: use kind argument to force list to have a specific model subclass, string or model subclass works
    creators = ndb.KeyProperty( repeated=True )
    num_creators = ndb.IntegerProperty( default=0 )
    admins = ndb.KeyProperty( repeated=True )
    num_admins = ndb.IntegerProperty( default=0 )
    contributors = ndb.KeyProperty( repeated=True )
    num_contributors = ndb.IntegerProperty( default=0 )
    editors = ndb.KeyProperty( repeated=True )
    num_editors = ndb.IntegerProperty( default=0 )

    # auto-properties
    date_created = ndb.DateProperty( auto_now_add=True )
    last_update = ndb.DateProperty( auto_now=True )

    # constants
    OBJECT_PROPS = [ "date_created", "last_update" ]
    # List of properties we don't want to send with get request
    # for this model, usually due to their size
    EXCLUDES = [
        "tags", "creators", "admins",
        "contributors", "editors"
    ]
    REQUIRED_PROPERTIES = [ "name" ]


    # Checks to see if key is an actual entity key
    @classmethod
    def check_key( cls,
                   urlsafe_key,
                   return_model=False,
                   check_model_type=True ):
        model = ndb.Key( urlsafe=urlsafe_key ).get()

        # make sure we are editing the right type of model
        if check_model_type:
            if not isinstance( model, cls ):
                return False

        if return_model:
            if model is None:
                return False

            return model

        return True


    # Converts a list of model keys into the model's dicts
    @classmethod
    def convert_keys_to_dicts( cls,
                               keys,
                               includes=None,
                               excludes=None ):
        dicts = []

        if keys == [] or keys == None:
            return dicts

        if includes != None:
            for key in keys:
                dicts.append( key.get().to_dict(
                    includes=includes,
                    excludes=excludes
                ) )
        else:
            for key in keys:
                dicts.append( key.get().to_dict(
                    excludes=excludes
                ) )

        return dicts


    # Convert dict to model
    @classmethod
    def dict_to_model( cls, model ):
        pass


    # Edit list of model keys, but it can be any type
    @classmethod
    def edit_list( cls, a_list, key, add=True ):
        try:
            # look for key in list
            index = a_list.index( key )
        except ValueError:
            # can't delete a key that isn't in the list
            if add is False:
                return False
            # add key to list
            else:
                a_list.append( key )
                return a_list
        else:
            # remove key from list
            if add is False:
                if len( a_list ) == 0:
                    return False
                a_list.pop( index )
                return a_list
            # key is already in list, do nothing
            else:
                return False


    # Turns model into json encodable dict
    def to_dict( self,
                 object_props=None,
                 includes=None,
                 excludes=None ):
        if includes != [] or includes is not None:
            dct = super( RestModel, self ).to_dict(
                include=includes,
                exclude=excludes
            )
        else:
            dct = super( RestModel, self ).to_dict(
                exclude=excludes
            )

        if object_props is None:
            object_props = dct.keys()
        # if all the key lists are excluded from the model's dict
        # then we don't need to do anything
        elif object_props == excludes:
            # added this in two places for optimization, one less key/value to look up
            # by default to_dict does not include the model's key
            if self.key is None:
                self.put()
            dct[ "key" ] = self.key.urlsafe()
            return dct

        # to_dict does not convert objects properties i.e. datetime, keys etc.
        for prop in object_props:
            if prop not in dct:
                continue

            a_obj = dct[ prop ]

            if isinstance( a_obj, list ):
                if a_obj == []:
                    continue

                if not isinstance( a_obj[0], ndb.KeyProperty ):
                    continue

                urlsafe_keys = []
                # convert keys into urlsafe strings
                for model_key in a_obj:
                    urlsafe_keys.append( model_key.urlsafe() )

                dct[ prop ] = urlsafe_keys

            elif isinstance( a_obj, date ):
                # TODO: add total seconds since 1972 for comparison, frontend it?
                dct[ prop ] = {
                    "year": a_obj.year,
                    "month": a_obj.month,
                    "day": a_obj.day
                }

            elif isinstance( a_obj, ndb.KeyProperty ):
                dct[ prop ] = a_obj.urlsafe()

        # added this in two places for optimization, one less key/value to look up
        # by default to_dict does not include the model's key
        if self.key is None:
            self.put()
        dct[ "key" ] = self.key.urlsafe()

        return dct


    # Creates an instance of the class and saves to database
    # returns the model
    @classmethod
    def create( cls, data ):
        model = cls(
            name=data[ "name" ],
            description=data.get( "description", "" )
        )

        try:
            model.put()
        except Exception, e:
            return False

        return model.key.urlsafe()


    # A hook that is called before delete()
    @classmethod
    def _pre_delete_hook( cls, key ):
        pass


    # Creates dummy data for model
    def create_dummy_data( self ):
        pass


    # Delete model from database
    def delete( self ):
        try:
            self.key.delete()
        except Exception, e:
            return False
        else:
            return True



    def put( self ):
        try:
            return super( RestModel, self ).put()
        except Exception:
            return False


    # Updates the model with the data passed
    # returns boolean depedent on the success of the update
    def update( self, data ):
        # model_name = data.get( "name", self.name )
        # model_descr = data.get( "description", self.description )
        # contributors = data.get( "contributors", self.contributors )

        # TODO: need to use flask-restful to parse incoming data then we can use this loop
        # # TODO: try except ( AttributeError via getattr ) this for optimization
        # for key in data.keys():
        #     if not hasattr( self, key ):
        #         continue
        #
        #     value = data[ key ]
        #     if getattr( self, key ) == value:
        #         continue
        #
        #     setattr( self, key, value )

        # logging.log( logging.INFO, data.keys() )
        # logging.log( logging.INFO, hasattr( self, "name" ) )
        # logging.log( logging.INFO, self.launchlists )

        # if model_name != self.name:
        #     self.name = model_name
        #
        # if model_descr != self.description:
        #     self.description = model_descr
        #
        # if contributors is not self.contributors:
        #     self.contributors = contributors

        return self.put()


    # Checks to see if model is in the passed list
    def is_in_list( self, a_list ):
        return ( self in a_list )


    # Checks to see if the model's is in the passed list
    def is_key_in_list( self, a_list ):
        return ( self.key in a_list )



class RestApi( Resource ):

    model_class = RestModel

    @classmethod
    def make_response_dict( cls, status=True, **kwargs ):
        response_dct = { "status": status }
        for key, value in kwargs.iteritems():
            response_dct[ key ] = value

        return response_dct


    # Deletes the model from database
    @classmethod
    def delete( cls ):
        if "key" not in request.form:
            return cls.make_response_dict(
                status=False,
                msg="send the key of the Topic to delete",
                format=" { 'key': 'hey-iam-a-key' }"
            ), 400

        urlsafe_key = request.form[ "key" ]
        model = cls.model_class.check_key(
            urlsafe_key,
            return_model=True,
            check_model_type=True
        )

        if model is False:
            return { "status": False }, 400

        if model.delete() is False:
            return { "status":  False }, 500

        return { "status": True }


    # Retrieves the model and sends it as a dict
    @classmethod
    def get( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        model = cls.model_class.check_key( urlsafe_key, return_model = True )

        if model is False:
            return { "status": False }, 400

        model_dict = model.to_dict( excludes=model.EXCLUDES )
        return { "status": True, "model": model_dict }


    # Updates the model with the data passed
    @classmethod
    def post( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        model = cls.model_class.check_key(
            urlsafe_key=urlsafe_key,
            return_model=True,
            check_model_type=True
        )

        if model is False:
            return {"status": False, "msg": "bad key"}, 400

        success = model.update( data )

        if success:
            return { "status": True }
        else:
            return { "status": False }, 500


    # Creates a model from data passed, returns model's key
    @classmethod
    def put( cls ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        for required_prop in cls.model_class.REQUIRED_PROPERTIES:
            if required_prop not in data:
                return cls.make_response_dict(
                    status=False,
                    msg="need all required properties to create topic, missing: " + required_prop,
                    required_properties=cls.model_class.REQUIRED_PROPERTIES ), 400

        urlsafe_key = cls.model_class.create( data )

        if urlsafe_key is False or urlsafe_key is None:
            return { "status": False }, 500
        else:
            return { "status": True, "key": urlsafe_key }, 201



class RestApis( Resource ):

    model_class = RestModel

    # Deletes the models from database
    @classmethod
    def delete( cls, urlsafe_key="" ):
        return { "status": False, "msg": "no perms" }, 403


    # Gets the models from database
    @classmethod
    def get( cls, urlsafe_key="" ):
        return { "status": False, "msg": "no perms" }, 403


    # Updates the models from database
    @classmethod
    def post( cls, urlsafe_key="" ):
        return { "status": False, "msg": "no perms" }, 403


    # Creates the models from database
    @classmethod
    def put( cls, urlsafe_key="" ):
        return { "status": False, "msg": "no perms" }, 403




