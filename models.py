# the basics
import logging
import json

from google.appengine.ext import ndb
# from google.appengine.api import search


# '''
# Returns the index the document is saved under
# '''
# def get_document_index( document ):
#     # if isinstance( document, TopicModel ):
#     return document.__name__

# '''
# Returns a document by its id
# @param [string] id - the id of document
# @param [string] index_name - the name of Search Index
# to search in
# @return [object] document - the document object, needs to be cleaned
# to be accessible as a dictionary
# '''
# def get_document_by_id( id, index_name ):
#     index = search.Index( name=index_name )
#     # TODO: wrap this in a try catch
#     return index.get( id )


#  '''
# Need to send cursor string from results.cursor to client, if it exists
# cursor_string = cursor.web_safe_string
# '''
# def query_index( query_string, index_name, query_options=None ):
#     index = search.Index( name=index_name )
#     results = []
#     if query_options is None:
#         query_options = create_query_options()
#     query = search.Query(
#         query_string=query_string,
#         options=query_options
#         )
#     try:
#         results = index.search( query )
#     except search.Error:
#         logging.exception( "Query failed" )
#     return results


# '''
#     Sets the query options like...
#     which fields should returned items have,
#     if there should be a cursor to keep track of where in the query
#     the user is
# '''
# def create_query_options( returned_fields, cursor=None, result_limit=10 ):
#     if cursor is None:
#         cursor = search.Cursor()
#     query_options = search.QueryOptions(
#         limit=result_limit,
#         returned_fields=returned_fields,
#         cursor=cursor
#         )
#     return query_options


# '''
# need to send query string to client to retrieve past query
# '''
# def create_query_string( query_dict ):
#     query_string = ""
#     for key in query_dict.keys():
#         if query_dict[key] == "" or query_dict[key] == None:
#             continue
#         query_string += " " + key + "=" + str( query_dict[key] )
#     return query_string


# '''
# '''
# def retrieve_query( query_string, cursor_string, index_name ):
#     index = search.Index( name=index_name )
#     cursor = search.Cursor( cursor_string )
#     query_options = search.QueryOptions( cursor=cursor, limit=10 )
#     query = search.Query( query_string=query_string,
#                             options=query_options )
#     return index.search( query )


# '''
# inserts document into index, saving it in the process
# NOTE:
# You can pass up to 200 documents at a time to the put() method.
# Batching puts is more efficient than adding documents one at a time.
# '''
# def save_document( document, index_name ):
#     index = search.Index( name=index_name )
#     try:
#         index.put( document )
#     except search.Error:
#         logging.exception( "Failed to save document" )


# def update_document( document ):
#     pass


# def delete_document( document ):
#     pass


##################################################
# Models
##################################################
class TopicModel( ndb.Model ):
    # TODO: do not allow multiline names
    name = ndb.StringProperty( default="Psuedoscience", required=True )
    description = ndb.TextProperty( default="It's real!!!", required=True )
    # icon = ndb.LinkProperty( required=True )
    icon = ndb.StringProperty( required=True )
    # display this topic on the front page?
    display_front_page = ndb.BooleanProperty( default=False )
    # this is a list of sub_topic keys
    sub_topics = ndb.KeyProperty( repeated=True )
    num_sub_topics = ndb.IntegerProperty( default=0 )

    def update( self, name, description, icon, sub_topics ):
        if name != None and name != self.name:
            self.name = name

        if description != None and description != self.description:
            self.description = description

        if icon != None and icon != self.icon:
            self.icon = icon

        if sub_topics != None and sub_topics != self.sub_topics:
            self.num_sub_topics = len( sub_topics )
            self.sub_topics = sub_topics

        return self.put()

    def add_sub_topic( self, sub_topic ):
        if not isinstance( sub_topic, ndb.KeyProperty ):
            return False

        if not isinstance( get_document_by_id( sub_topic ) ):
            return False

        self.sub_topics.append( sub_topic )
        self.num_sub_topics += 1

        return self.put()

    def json_encode( self ):
        return json.dumps( self.to_dict() )

    def create_sub_topics( self ):
        music_production = SubTopicModel(
            name = "Music Production",
            description = "Theory is a very useful tool, as it is a logic that makes sense of what sounds good in music and why. But what is theory even used for? How does it benefit you? As a beginner, it quickly enables music to make much more sense. As you practice composing and producing, it will open doors to more complicated, layer-driven forms of writing that connects your music to itself in various ways and makes it sound good and powerful.",
            topics = self.key,
            num_topics = 1
        )

        return self.add_sub_topic( music_production )
        # music_theory = LaunchListModel(
        #     name = ""
        # )

    @classmethod
    def _get_index( cls ):
        return "TopicModel"

    # TODO: add number_of_topics, query_string to settings
    # TODO: check for duplicates
    @classmethod
    def get_topics( cls, number_of_topics = 9, query_string = "" ):
        query = cls.query( cls.display_front_page == True ).order( -cls.num_sub_topics )
        topics = query.fetch( number_of_topics )

        if len( topics ) == 0:
            cls.create_topics()
            query = cls.query( cls.display_front_page == True ).order( -cls.num_sub_topics )
            topics = query.fetch( number_of_topics )
            # this recursion creates multiple copies of the topics
            # in the datastore because the datastore requires time
            # to update with new entities
        #     return cls.get_topics( number_of_topics, query_string )

        return topics

    @classmethod
    def get_topic( cls, urlsafe_key ):
        topic_key = ndb.Key( urlsafe=urlsafe_key )
        topic = topic_key.get()
        sub_topics = topic.sub_topics

        if len( sub_topics ) == 0:
            
        else:
            for index in enumerate( sub_topics ):
                sub_topic = sub_topics[ index ]
                sub_topics[ index ] = sub_topic.get_dict();

            # for index in enumerate( sub_topics ):
            #     sub_topic = sub_topics[ index ]
            #     sub_topics[ index ] = sub_topic.urlsafe()

        topic_dict = topic.to_dict()
        topic_dict["key"] = topic.key.urlsafe()

        return topic_dict

    @classmethod
    def create_topics( cls ):
        music = TopicModel(
                    name = "Music",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        code = TopicModel(
                    name = "Code",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        design = TopicModel(
                    name = "Design",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        politics = TopicModel(
                    name = "Politics",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        life = TopicModel(
                    name = "Life",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        relationships = TopicModel(
                    name = "Relationships",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        health = TopicModel(
                    name = "Health",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        school = TopicModel(
                    name = "School",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        random = TopicModel(
                    name = "Random",
                    description = "'Happiness today is just a song away, just a song\nI love your music, baby' \n- Just Like Music, Erick Sermon feat. Marvin Gaye",
                    icon = "../icons/apple_music_icon_trns.png",
                    display_front_page = True )

        ndb.put_multi( [ music, code, design,
                        politics, life, relationships,
                        health, school, random ] )


class SubTopicModel( ndb.Model ):
    name = ndb.StringProperty( default="Phrenology", required=True )
    description = ndb.TextProperty( default="Can you feel me?", required=True )
    # list of topic keys that this subtopic is included in
    topics = ndb.KeyProperty( repeated=True )
    num_topics = ndb.IntegerProperty( default=1 )
    # list of launchlist keys
    launchlist = ndb.KeyProperty( repeated=True )
    num_launchlist = ndb.IntegerProperty( default=0 )

    # def get_dict( self ):
    #     sub_topic_dict = self.to_dict();

    @classmethod
    def get_dict( cls, key ):
        sub_topic = key.get()
        sub_topic_dict = sub_topic.to_dict()
        sub_topic_dict["key"] = sub_topic.key.urlsafe()
        return sub_topic_dict


class LaunchListModel( ndb.Model ):
    name = ndb.StringProperty( default="How to fleece rubes?", required=True )
    description = ndb.TextProperty( default="You will learn.", required=True )
    # list of Resoruce that belong to this LaunchList
    # only holds refrences, empty list by default
    resoruce = ndb.KeyProperty( repeated=True )
    # num_resoruce = ndb.IntegerProperty( default=0 )
    # rating = ndb.RatingProperty()
    # the user that added to this tutorial
    contributor = ndb.KeyProperty()
    rating = ndb.StringProperty()


class ResourceModel( ndb.Model ):
    name = ndb.StringProperty( default="How to fleece rubes?", required=True )
    description = ndb.TextProperty( default="You will learn.", required=True )
    link = ndb.StringProperty( default="mta.io/#", required=True)
    # resource_type = ndb.KeyProperty()
    resource_type = ndb.StringProperty( default="Text", required=True )
    # rating = ndb.RatingProperty()
    source_author = ndb.StringProperty()
    source_date = ndb.DateProperty()
    # the user that added to this resource
    contributor = ndb.KeyProperty()
    date_created = ndb.DateProperty( auto_now_add=True )
    date_update = ndb.DateProperty( auto_now=True )
    # list of LaunchLists that this Resource belong to
    # only holds refrences, empty list by default
    launch_list = ndb.KeyProperty( repeated=True )
    # num_launch_list = ndb.IntegerProperty( default=0 )
    rating_smily = ndb.StringProperty()


class AccountModel( ndb.Model ):
    first_name = ndb.StringProperty( default="Friedrich", required=True )
    last_name = ndb.StringProperty( default="Nietzsche", required=True )
    profile_type = ndb.StringProperty( required=True )
    # TODO: needs to be validated
    email = ndb.StringProperty( required=True )
    description = ndb.TextProperty( default="Iam the UberMentch!", required=True )
    # "A user with a Google account"
    user = ndb.UserProperty( auto_current_user=True, auto_current_user_add=True, required=True )
    date_created = ndb.DateProperty( auto_now_add=True )
    date_update = ndb.DateProperty( auto_now=True )
    # list of LaunchLists that this Account Created
    # only holds refrences, empty list by default
    launch_list = ndb.KeyProperty( repeated=True )
    # list of LaunchLists that this Account Created
    resources = ndb.KeyProperty( repeated=True )


class SubscriberModel( ndb.Model ):
    # TODO: email needs to be validated
    email = ndb.StringProperty( required=True )
    first_name = ndb.StringProperty( default="Friedrich" )
    last_name = ndb.StringProperty( default="Nietzsche" )
    occupation = ndb.StringProperty( default="Deranged Lunatic" )
    age = ndb.IntegerProperty( default=0 )
