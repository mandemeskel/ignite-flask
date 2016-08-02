# the basics
import logging
from datetime import date

# Google stuff
from google.appengine.ext import ndb

# Import the Flask Framework
from flask import Flask, render_template, request, Response
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

    name = ndb.StringProperty( default="Psuedoscience", required=True )
    description = ndb.TextProperty( default="It's real!!!" )
    contributors = ndb.KeyProperty( repeated=True )
    date_created = ndb.DateProperty( auto_now_add=True )
    last_update = ndb.DateProperty( auto_now=True )
    OBJECT_PROPS = [ "contributors", "date_created", "last_update" ]


    # Checks to see if key is an actual entity key
    @classmethod
    def check_key( cls, urlsafe_key, return_model = False ):
        model = ndb.Key( urlsafe = urlsafe_key ).get()

        # make sure we are editing the right type of model
        if not isinstance( model, cls ):
            return False

        if return_model:
            if model is None:
                return False

            return model

        return True


    # Converts a list of model keys into the model's dicts
    @classmethod
    def convert_keys_to_dicts( cls, keys, includes=None, excludes=None ):
        dicts = []

        if keys == [] or keys == None:
            return dicts

        if includes != None:
            for key in keys:
                dicts.append( key.get().to_dict( includes=includes, excludes=excludes ) )
        else:
            for key in keys:
                dicts.append( key.get().to_dict( excludes=excludes ) )

        return dicts


    # Convert dict to model
    @classmethod
    def dict_to_model( cls, model ):
        pass


    # Turns model into json encodable dict
    def to_dict( self, object_props=[], includes=[], excludes=[] ):
        if includes != []:
            dct = super( RestModel, self ).to_dict( include=includes, exclude=excludes )
        else:
            dct = super( RestModel, self ).to_dict( exclude=excludes )

        if object_props == []:
            object_props = dct.keys()
        # if all the key lists are excluded from the model's dict
        # then we don't need to do anything
        elif object_props == excludes:
            # added this in two places for optimization, one less key/value to look up
            # by default to_dict does not include the model's key
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

                if not isinstance( a_list[0], ndb.KeyProperty ):
                    continue

                urlsafe_keys = []
                # convert keys into urlsafe strings
                for model_key in a_obj:
                    urlsafe_keys.append( model_key.urlsafe() )

                dct[ prop ] = urlsafe_keys

            elif isinstance( a_obj, date ):
                # TODO: add total secounds since 1972 for comparison, frontend it?
                dct[ prop ] = {
                    "year": a_obj.year,
                    "month": a_obj.month,
                    "day": a_obj.day
                }

            elif isinstance( a_obj, ndb.KeyProperty ):
                dct[ prop ] = a_obj.urlsafe()

        # added this in two places for optimization, one less key/value to look up
        # by default to_dict does not include the model's key
        dct[ "key" ] = self.key.urlsafe()

        return dct


    # Creates an instance of the class and saves to database
    # returns the model
    @classmethod
    def create( cls, data ):
        model = cls(
            name=data[ "name" ],
            description=data.get( "description", "" ),
            contributors=data.get( "contributors", [] )
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


    # Updates the model with the data passed
    # returns boolean depedent on the success of the update
    def update( self, data ):
        model_name = data.get( "name", self.name )
        model_descr = data.get( "description", self.description )
        contributors = data.get( "contributors", self.contributors )

        if model_name != self.name:
            self.name = model_name

        if model_descr != self.description:
            self.description = model_descr

        if contributors is not self.contributors:
            self.contributors = contributors

        try:
            self.put()
        except Exception, e:
            return False
        else:
            return self.key.urlsafe()


    # Checks to see if model is in the passed list
    def is_in_list( self, a_list ):
        return ( self in a_list )


    # Checks to see if the model's is in the passed list
    def is_key_in_list( self, a_list ):
        return ( self.key in a_list )



class RestApi( Resource ):

    model_class = RestModel

    # Deletes the model from database
    @classmethod
    def delete( cls, urlsafe_key ):
        model = cls.model_class.check_key( urlsafe_key, return_model = True )

        if model is False:
            return { "status": False }, 400

        if model.delete() is False:
            return { "status":  False }, 500

        return { "status": True }


    # Retrives the model and sends it as a dict
    @classmethod
    def get( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        model = cls.model_class.check_key( urlsafe_key, return_model = True )

        if model is False:
            return { "status": False }, 400

        model_dict = model.to_dict()
        return { "status": True, "model": model_dict }


    # Updates the model with the data passed
    @classmethod
    def post( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        model = cls.model_class.check_key( urlsafe_key, return_model = True )

        if model is False:
            return { "status": False }, 400

        urlsafe_key = model.update( data )

        if urlsafe_key:
            return { "status": True, "key": urlsafe_key }
        else:
            return { "status": False }, 500


    # Creates a model from data passed, returns model's key
    @classmethod
    def put( cls ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        if "name" not in data or "description" not in data:
            return { "status": False }, 400

        urlsafe_key = cls.model_class.create( data )

        if urlsafe_key is False or urlsafe_key is None:
            return { "status": False }, 500
        else:
            return { "status": True, "key": urlsafe_key }, 201



# requests that will be routed to the RestModel class
api.add_resource( RestApi,
    "/test/<urlsafe_key>",
    "/test"
)
