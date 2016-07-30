import logging
import json

from google.appengine.ext import ndb


class RestModel( ndb.Model ):

    # Deletes model from database
    @classmethod
    def DELETE( cls, urlsafe_key ):
        if cls.check_key( urlsafe_key ) is False:
            return False
        ndb.Key( urlsafe_key=urlsafe_key ).delete()
        return True

    # Retrives model and sends it as a dict
    @classmethod
    def GET( cls, urlsafe_key ):
        model = RestModel.check_key( urlsafe_key, return_model = True )
        if model is False:
            return False
        return cls.to_dict()

    # Updates the model with the data passed
    @classmethod
    def POST( cls, urlsafe_key, data ):
        model = RestModel.check_key( urlsafe_key, return_model = True )
        if model is False:
            return False
        return model.update( data )

    # Create model from data passed, returns model's key
    @classmethod
    def PUT( cls, data ):
        model = cls.create( data )
        if model is False:
            return False
        return model.key.urlsafe()

    @classmethod
    def check_key( cls, urlsafe_key, return_model = False ):
        if return_model:
            return ndb.Key( urlsafe=urlsafe_key ).get()

    # def json_encode( self ):
        # pass

    def to_dict( self ):
        dct = super( ndb.Model, self ).to_dict()
        dct[ "key" ] = self.key.urlsafe()
        # to_dict does not convert mutable properties i.e. dicts/lists
        for key in dct.keys:
            if isinstance( dct[ key ], list ):
                urlsafe_keys = []
                for item in dct[ key ]:
                    if isinstance( item, ndb.KeyProperty ):
                        urlsafe_keys.append( item.urlsafe() )
                dct[ key ] = urlsafe_keys
        # return json.dumps( dct )
        return dct

    # Creates an instance of the class and saves to database
    # returns the model
    def create( self, data ):
        pass

    def create_dummy_data( self ):
        pass

    # Updates the model with the data passed
    # returns boolean depedent on the success of the update
    def update( self, data ):
        pass

    # Checks to see if model is in the passed list 
    def is_in_list( self, a_list ):
        return ( self in a_list )

    # Checks to see if the model's is in the passed list
    def is_key_in_list( self, a_list ):
        return ( self.key in a_list )
