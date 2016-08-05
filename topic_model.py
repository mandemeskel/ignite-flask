# the basics
import logging

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
from rest_model import RestApi, RestsApi, RestModel, RESPONSE_STATUS
from launchlist_model import LaunchList

app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True



class POST_KEYWORDS:
    remove_launchlists = "remove_launchlists"
    add_launchlists = "add_launchlists"



class Topic( RestModel ):

    # display this topic on the front page?
    display_front_page = ndb.BooleanProperty( default=False )
    # this is a list of launchlists keys
    launchlists = ndb.KeyProperty( repeated=True,  kind=LaunchList )
    num_launchlists = ndb.ComputedProperty(
        lambda self: len( self.launchlists ) )

    # constants
    # REQUIRED_PROPERTIES = [ "name", "description", "icon" ]
    OBJECT_PROPS = RestModel.OBJECT_PROPS
    OBJECT_PROPS.append( "launchlists" )
    # EXCLUDES = RestModel.EXCLUDES
    # EXCLUDES.extend( [
    #     "launchlists"
    # ] )

    # Returns a list of Topics with display_front_page=True
    # @classmethod
    # def get_front_page_topics( cls, num_topics=3,
    #     excludes=[ "launchlists", "display_front_page" ] ):
    #     return


    # Creates an instance of the class and saves to database
    # returns the model
    @classmethod
    def create( cls, data, return_as_dict=False ):
        # check that required properties are in the passed data
        # for prop in cls.REQUIRED_PROPERTIES:
        #     if prop not in data:
        #         logging.log( logging.ERROR, "Topic.create(), miss property: " + prop )
        #         return False

        # TODO: validate passed data
        # for prop in data.keys():
        #     if prop == "name":
        #         if prop is not str:
        #             logging.log( "logging.ERROR", "Topic.create(), bad value: " + prop )
        #             return False

        if DEVELOPING:
            logging.log( logging.INFO, data )

        # add required properties to create class
        topic = cls(
            name=data[ "name" ],
            description=data[ "description" ],
            icon=data[ "icon" ]
        )

        # NOTE: can't remove because data is an ImmutableMultiDict
        # remove the properties already in class
        # data.pop( "name" )
        # data.pop( "description" )
        # data.pop( "icon" )

        # add all other properties
        # DONE: we will need to add by property
        # for key, value in data.iteritems():
        #     if not hasattr( topic, key ):
        #         continue
        #     if getattr( topic, key ) == value:
        #         continue
        #     setattr( topic, key, value )
        if "display_front_page" in data:
            value = data[ "display_front_page" ]
            if value == "true" or value == "True":
                topic.display_front_page = True
            else:
                topic.display_front_page = False

        # save to database
        try:
            key = topic.put()
        except Exception as e:
            logging.log( logging.ERROR, "Topic.create(), failed to create Topic: " + topic.name )
            logging.log( logging.ERROR, e )
            return False

        # return as dict for display
        if return_as_dict:
            return topic.to_dict()

        return key.urlsafe()


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
            topic = cls.create(
                {
                    "name": name,
                    "description": description,
                    "icon": icon,
                    "display_front_page": display_front_page
                } ,
                return_as_dict=True
            )

            if Topic is False:
                continue

            topics.append( topic )

        return topics


    # Returns a list of topics ordered by number of launchlists they contain
    @classmethod
    def get_topics( cls, num_topics=3, includes=None, excludes=None ):
        # TODO: make query an dynamic i.e. an arg
        query = cls.query( cls.display_front_page == True ).order(
            -cls.num_launchlists )

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
            topics_dict.append(
                topic.to_dict(
                includes=includes,
                excludes=excludes )
            )

        return topics_dict


    @classmethod
    def get_excludes( cls, new_excludes=None ):
        return super( Topic, cls ).get_excludes( [ "launchlists" ] )


    @classmethod
    def get_required_properties( cls, new_requires=None ):
        return super( Topic, cls ).get_required_properties(
            [
                "description",
                "icon"
            ]
        )


    # Adds launchlist to Topic
    def add_launchlist( self, launchlist_urlsafe_key="", launchlist=None ):

        if launchlist_urlsafe_key != "" and launchlist is None:
            launchlist = self.check_key(
                urlsafe_key=launchlist_urlsafe_key,
                return_model=True,
                check_model_type=False
            )

            if launchlist is False:
                return False

        elif launchlist is None:
            return False

        a_list = self.edit_list( self.launchlists, launchlist.key, add=True )

        if a_list is False:
            return False

        self.launchlists = a_list
        return launchlist.put()


    # Creates dummy data for model
    def create_dummy_data( self ):
        pass


    # Remove references to this topic
    def delete( self ):
        logging.log( logging.INFO, self.EXCLUDES )
        for property in self.get_excludes():
            for entity_key in getattr( self, property ):
                entity_key.get().edit_topics(
                    self,
                    add=False,
                    safe=True
                )
        # for launchlist_key in self.launchlists:
        #     launchlist_key.get().edit_topics(
        #         self,
        #         add=False,  # remove topic from launchlist
        #         safe=True,  # don't need to validate topic
        #     )

        return True


    def edit_launchlists( self, launchlist, add=True ):
        key = launchlist.key
        a_list = self.edit_list( self.launchlists, key, add )

        if a_list is False:
            return False

        self.launchlists = a_list

        return True


    # Removes launchlist from Topic
    def remove_launchlist( self, launchlist_urlsafe_key ):
        # TODO: create method to transform websafe_key to regular key
        # NOTE: don't need to check model type sense kind argument in list property
        # does that for us
        launchlist = self.check_key(
            urlsafe_key=launchlist_urlsafe_key,
            return_model=True,
            check_model_type=False
        )
        # launchlist = ndb.Key( urlsafe=launchlist_urlsafe_key ).get()

        if launchlist is False:
            return False

        # logging.log( logging.INFO, launchlist )

        a_list = self.edit_list( self.launchlists, launchlist.key, add=False )

        # logging.log( logging.INFO, a_list )

        if a_list is False:
            return False

        self.launchlists = a_list
        return launchlist.put()


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
        logging.log( logging.INFO, "display_front_page" in data )

        if POST_KEYWORDS.remove_launchlists in data:
            lists = data[ POST_KEYWORDS.remove_launchlists ]
            if lists is not list:
                lists = lists.split( "," )

            for launchlist in lists:
                success = self.remove_launchlist( launchlist_urlsafe_key=launchlist )

                if success is False:
                    return False

        if POST_KEYWORDS.add_launchlists in data:
            lists = data[ POST_KEYWORDS.add_launchlists ]
            if lists is not list:
                lists = lists.split( "," )

            # logging.log( logging.INFO, lists )
            for launchlist in lists:
                # logging.log( logging.INFO, launchlist )
                success = self.add_launchlist( launchlist_urlsafe_key=launchlist )

                if success is False:
                    return False

        if "display_front_page" in data:
            value = data[ "display_front_page" ]
            if value == "true" or value == "True":
                self.display_front_page = True
            else:
                self.display_front_page = False

        return super( Topic, self ).update( data )




# TODO: needs auth to delete, post, and put
class TopicApi( RestApi ):

    model_class = Topic

    # DONE: remove topic from launchlists
    # Handles all behaviour that removes data from this Topic
    @classmethod
    def delete( cls, urlsafe_key="" ):
        topic = cls.model_class.check_key(
            urlsafe_key=urlsafe_key,
            return_model=True,
            check_model_type=True
        )

        if topic is False:
            return cls.make_response_dict(
                status=False,
                msg="bad key, can't get topic"
            ), 400

        if not topic.delete():
            return cls.make_response_dict(
                status=False,
                msg="can't delete topic"
            ), 400

        topic.key.delete()

        return cls.make_response_dict(
            status=True
        )


    # Gets all the Topic in its entirety
    @classmethod
    def get( cls, urlsafe_key ):
        data = request.form

        if DEVELOPING:
            logging.log( logging.INFO, data )

        topic = cls.model_class.check_key( urlsafe_key, return_model = True )

        if topic is False:
            return { "status": False }, 400

        topic_dict = topic.to_dict( excludes=topic.get_excludes() )

        return { "status": True, "topic": topic_dict }, 200


    # Updates the topic with the data passed
    # NOTE: why not save ourselves the trouble and just directly go to super method?
    # NOTE: because user auth for this topic will happen here
    @classmethod
    def post( cls, urlsafe_key ):
        return super( TopicApi, cls ).post( urlsafe_key )


    # Creates a model from data passed, returns model's key
    @classmethod
    def put( cls ):
        return super( TopicApi, cls ).put()



class TopicsApi(RestsApi):
    model_class = Topic

    # TODO: validate data
    # gets multiple topics
    @classmethod
    def get( cls, num=3 ):
        data = request.args

        if DEVELOPING:
            logging.log( logging.INFO, data )

        # NOTE: not python 3.x friendly, should be isinstance( num, str )
        if isinstance( num, basestring ):
            try:
                num = int( num )
            except Exception, e:
                return { "status": False }, 500

        # if DEVELOPING:
        #     logging.log( logging.INFO, num )

        topics = cls.model_class.get_topics(
            num_topics=num,
            includes=[ "name", "icon" ]
        )

        if topics is False:
            return { "status": False }, 500
        elif topics is None:
            return { "status": False, RESPONSE_STATUS.retry: True }, 204

        return { "status": True, "topics": topics }


