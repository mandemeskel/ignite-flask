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



class Topic( RestModel ):

    # TODO: do not allow multiline names
    # inherited from RestModel
    # name = ndb.StringProperty( default="Psuedoscience", required=True )
    # description = ndb.TextProperty( default="It's real!!!" )
    # contributors = ndb.KeyProperty( repeated=True )
    # date_created = ndb.DateProperty( auto_now_add=True )
    # last_update = ndb.DateProperty( auto_now=True )
    icon = ndb.StringProperty( required=True )
    # display this topic on the front page?
    display_front_page = ndb.BooleanProperty( default=False )
    # this is a list of launchlists keys
    launchlists = ndb.KeyProperty( repeated=True )
    num_launchlists = ndb.IntegerProperty( default=0 )
    REQUIRED_PROPERTIES = [ "name", "description", "icon" ]
    OTHER_PROPERTIES = [ "display_front_page", "launchlists", "num_launchlists" ]
    OBJECT_PROPS = RestModel.OBJECT_PROPS
    OBJECT_PROPS.append( "launchlists" )

    # Returns a list of Topics with display_front_page=True
    # @classmethod
    # def get_front_page_topics( cls, num_topics=3,
    #     excludes=[ "launchlists", "display_front_page" ] ):
    #     return


    # Creates an instance of the class and saves to database
    # returns the model
    @classmethod
    def create( cls, data, return_as_dict=True ):
        # check that required properties are in the passed data
        for prop in cls.REQUIRED_PROPERTIES:
            if prop not in data:
                logging.log( logging.ERROR, "Topic.create(), miss property: " + prop )
                return False

        # TODO: validate passed data
        # for prop in data.keys():
        #     if prop == "name":
        #         if prop is not str:
        #             logging.log( "logging.ERROR", "Topic.create(), bad value: " + prop )
        #             return False

        if DEVELOPING:
            logging.log( logging.INFO, data )

        topic = cls(
            name=data[ "name" ],
            description=data[ "description" ],
            icon=data[ "icon" ],
            display_front_page=data[ "display_front_page" ]
        )

        try:
            topic.put()
        except Exception as e:
            logging.log( logging.ERROR, "Topic.create(), failed to create Topic: " + topic.name )
            logging.log( logging.ERROR, e )
            return False

        if return_as_dict:
            return topic.to_dict()

        return topic


    # TODO: move out to parent class?
    # Creates the first set of dummy topics
    @classmethod
    def create_dummy_topics( cls ):
        topics = []
        names = [ "Music", "Design", "Code", "Politics", "Life", "Relationships", "Health", "School", "Random" ]
        description = '"Happiness today is just a song away, just a song\nI love your music, baby" \n- Just Like Music, Erick Sermon feat. Marvin Gaye'
        icon = "../icons/apple_music_icon_trns.png"
        display_front_page = True

        for name in names:
            topic = cls.create( {
                "name": name,
                "description": description,
                "icon": icon,
                "display_front_page": display_front_page
            } )

            if Topic is False:
                continue

            topics.append( topic )

        return topics


    # Returns a list of topics ordered by number of launchlists they contain
    @classmethod
    def get_topics( cls, num_topics=3, includes=[], excludes=[] ):
        # TODO: make query an dynamic i.e. an arg
        query = cls.query( cls.display_front_page == True ).order( -cls.num_launchlists )

        # search for topics matching our query params
        try:
            topics = query.fetch( num_topics )
        except Exception as e:
            logging.log( logging.ERROR, "Topic.get_topics(), failed to fetch query" )
            logging.log( logging.ERROR, e )
            return False

        # if DEVELOPING:
        #     logging.log( logging.INFO, topics )

        if topics == [] or topics is None:
            return cls.create_dummy_topics()

        # convert all topics into dicts
        topics_dict = []
        for topic in topics:
            topics_dict.append( topic.to_dict( includes=includes, excludes=excludes ) )

        return topics_dict


    # Adds launchlist to Topic
    def add_launchlist( self, launchlist_urlsafe_key ):
        launchlist = cls.check_key( launchlist_urlsafe_key, return_model=True )
        if launchlist.key not in self.launchlists:
            self.launchlists.append( launchlist.key )
            self.num_launchlists += 1
            return True
        return False


    # Creates dummy data for model
    def create_dummy_data( self ):
        pass


    # Removes launchlist from Topic
    def remove_launchlist( self, launchlist_urlsafe_key ):
        # TODO: create method to transform websafe_key to regular key
        launchlist = cls.check_key( launchlist_urlsafe_key, return_model=True )

        if self.num_launchlists == 0:
            return False
        elif launchlist.key in self.launchlists:
            self.launchlists.remove( launchlist.key )
            self.num_launchlists -= 1
            return True

        return False


    # Turns model into json encodable dict
    def to_dict( self, includes=None, excludes=None ):
        # if DEVELOPING:
        #     logging.log( logging.INFO, type( self ) )

        if includes is not None:
            dct = super( Topic, self ).to_dict(
                    object_props=Topic.OBJECT_PROPS,
                    includes=includes,
                    excludes=excludes
                )
        else:
            dct = super( Topic, self ).to_dict(
                    object_props=Topic.OBJECT_PROPS,
                    excludes=excludes
                )
        return dct


    '''
        UPDATE SCENARIOS
        update regular properties like name, descrp, icon, etc.
        update lists by sending list item that with DELETE or POST argument
        in other words lists belonging to this Topic will not be edited using the POST
        method of this Topic?
    '''
    # TODO: validate passed data
    # Update this Topics data and return the Topic
    def update( self, data ):
        model_dict = self.to_dict();
        for prop in data.keys():
            if prop not in Topic.REQUIRED_PROPERTIES or prop not in Topic.OTHER_PROPERTIES:
                continue
            if data[ prop ] == model_dict[ prop ]:
                continue
            model_dict[ prop ] == data[ prop ]

        # TODO: create dict_to_model?
        model = Topic.dict_to_model( model_dict )
        try:
            model.put()
        except Exception as e:
            logging.log( "logging.ERROR", "Topic.update(), failed to update Topic: " + str( data ) )
            logging.log( "logging.ERROR", e )
            return False

        return model_dict



class TopicApi( RestApi ):
    model_class = Topic

    # TODO: needs auth to delete
    # Handles all behaviour that removes data from this Topic
    @classmethod
    def delete( cls, topic_ulrsafe_key, list_urlsafe_key=None ):
        # if list_urlsafe_key != None:
        #     topic = cls.model_class.check_key( topic_ulrsafe_key, return_model=True )
        #     result = cls.model_class.remove_launchlist( list_urlsafe_key )

        #     if result:
        #         return { "status": False, "msg": "failed to remove launchlist" }, 500

        #     return { "status": True }
        # else:
        #     return super( TopicApi, cls ).delete( topic_ulrsafe_key )

        return { "status": False, "msg": "no perms" }, 403


    # Gets all the Topic in its entirety
    @classmethod
    def get( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        topic = cls.model_class.check_key( urlsafe_key, return_model = True )

        if topic is False:
            return { "status": False }, 400

        topic_dict = topic.to_dict( excludes=[ "contributors", "launchlists" ] )

        launchlists = cls.model_class.convert_keys_to_dicts( model.launchlists, includes=[ "name", "rating", "author", "last_update", "num_resoruces" ] )

        contributors = cls.model_class.convert_keys_to_dicts( model.contributors, includes=[ "name", "author", "last_update" ] )

        topic_dict[ "launchlists" ] = launchlists
        topic_dict[ "contributors" ] = contributors

        return { "status": True, "topic": topic_dict }, 200



    # Updates the topic with the data passed
    @classmethod
    def post( cls, urlsafe_key ):
        return { "status": False, "msg": "no perms" }, 403


    # Creates a model from data passed, returns model's key
    @classmethod
    def put( cls ):
        return { "status": False, "msg": "no perms" }, 403



class TopicsApi( RestApi ):
    model_class = Topic

    # TODO: validate data
    # TODO: remove includes and excludes params
    # gets multiple topics
    @classmethod
    def get( cls, ajax=False, num=3, includes=[], excludes=[] ):
        # NOTE: not python 3.x friendly
        if includes != [] and isinstance( includes, basestring ):
            includes = includes.split( "," )

        # NOTE: not python 3.x friendly
        if excludes != [] and isinstance( excludes, basestring ):
            excludes = excludes.split( "," )

        if DEVELOPING:
            logging.log( logging.INFO, type( includes ) )
            logging.log( logging.INFO, type( excludes ) )

        # send only the neccassary info by default
        if excludes == []:
            excludes = cls.model_class.OBJECT_PROPS
            excludes.extend( [ "display_front_page", "num_launchlists" ] )

        # NOTE: not python 3.x friendly, should be isinstance( num, str )
        if isinstance( num, basestring ):
            try:
                num = int( num )
            except Exception, e:
                return { "status": False }, 500


        # if DEVELOPING:
        #     logging.log( logging.INFO, num )

        if ajax:
            topics = cls.model_class.get_topics(
                num_topics=num,
                includes=includes,
                excludes=excludes
            )

            if topics is False:
                return { "status": False }, 500
            elif topics is None:
                return { "status": False, RESPONSE_STATUS.retry: True }, 204

            return { "status": True, "topics": topics }

        else:
            return { "status": False }, 404



# requests that will be routed to the RestModel class
api.add_resource( TopicApi,
    "/topic/<urlsafe_key>",
    "/topic"
)

# TODO: remove includes and excludes url params
api.add_resource( TopicsApi,
    "/topics/<ajax>/<num>/<includes>/<excludes>",
    "/topics/<ajax>/<num>/<includes>",
    "/topics/<ajax>/<num>",
    "/topics/<ajax>",
    "/topics"
)
