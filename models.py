# -*- coding: utf-8 -*-
# the basics
import logging
import json

from google.appengine.ext import ndb


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
    # this is a list of subtopic keys
    subtopics = ndb.KeyProperty( repeated=True )
    num_subtopics = ndb.IntegerProperty( default=0 )

    def update( self, name, description, icon, subtopics ):
        if name != None and name != self.name:
            self.name = name

        if description != None and description != self.description:
            self.description = description

        if icon != None and icon != self.icon:
            self.icon = icon

        if subtopics != None and subtopics != self.subtopics:
            self.num_subtopics = len( subtopics )
            self.subtopics = subtopics

        return self.put()

    # TODO: check if subtopic is already in topic
    # def add_subtopic( self, subtopic ):
    #     if not isinstance( subtopic, ndb.KeyProperty ):
    #         return False
    #
    #     if not isinstance( get_document_by_id( subtopic ) ):
    #         return False
    #
    #     self.subtopics.append( subtopic )
    #     self.num_subtopics += 1
    #
    #     return self.put()
    def add_subtopic( self, subtopic ):
        if not isinstance( subtopic, SubTopicModel ):
            return False

        subtopic.topics.append( self.key )
        subtopic_key = subtopic.put()
        self.subtopics.append( subtopic_key )
        self.num_subtopics += 1

        return subtopic_key

    def json_encode( self ):
        return json.dumps( self.to_dict() )

    def create_subtopics( self, number = 4 ):
        # music_production = SubTopicModel(
        #     name = "Music Production",
        #     description = "Theory is a very useful tool, as it is a logic that makes sense of what sounds good in music and why. But what is theory even used for? How does it benefit you? As a beginner, it quickly enables music to make much more sense. As you practice composing and producing, it will open doors to more complicated, layer-driven forms of writing that connects your music to itself in various ways and makes it sound good and powerful.",
        #     topics = self.key,
        #     num_topics = 1
        # )
        subtopic_keys = []
        # create dummy subtopics and add them to topic
        for num in range( 0, number ):
            subtopic = SubTopicModel(
                name = "Subtopic",
                description = "A subtopic",
                topics = [ self.key ],
                num_topics = 1
            )
            subtopic_keys.append( self.add_subtopic( subtopic ) )
            # subtopic.create_launchlists()

        self.put()
        return subtopic_keys

    @classmethod
    def _get_index( cls ):
        return "TopicModel"

    # TODO: add number_of_topics, query_string to settings
    # TODO: check for duplicates
    @classmethod
    def get_topics( cls, number_of_topics = 9, query_string = "" ):
        query = cls.query( cls.display_front_page == True ).order( -cls.num_subtopics )
        topics = query.fetch( number_of_topics )

        if len( topics ) == 0:
            cls.create_topics()
            query = cls.query( cls.display_front_page == True ).order( -cls.num_subtopics )
            topics = query.fetch( number_of_topics )
            # this recursion creates multiple copies of the topics
            # in the datastore because the datastore requires time
            # to update with new entities
        #     return cls.get_topics( number_of_topics, query_string )

        return topics

    def create_music_subtopics( self ):
        # account
        nina = AccountModel(
            first_name = "Nina",
            last_name = "Krishnan",
            # profile_type = ""
            email = "ninakrish@gmail.com",
            description = "NDMA - NenDogMakesArt"
        )
        nina_key = nina.put()
        # resources
        music_theory1 = ResourceModel(
            name = "A Starter’s Guide to Music Production",
            description = "A crowd-sourced Reddit compilation, ideal for beginners who want to understand why music theory is important and how it can be used.",
            # TODO: should be a constant
            resource_type = "LINK",
            source = "https://www.reddit.com/r/edmproduction/comments/1uvtxw/a_starters_guide_to_music_theory/",
            # source_author = "",
            # source_date = "",
            contributor = nina_key,
        )
        music_theory2 = ResourceModel(
            name = "How Basic Chords Work",
            description = "This lesson is on chords, how they work, and the basic intervals that make them up. Learning the underlying music theory behind chords will not only allow you to find any chord you want, anywhere you want, it will also give you a solid foundation to build your entire understanding of music theory on.",
            # TODO: should be a constant
            resource_type = "VIDEO",
            source = "https://www.youtube.com/watch?v=5Y01jIorp",
            # source_author = "",
            # source_date = "",
            contributor = nina_key,
        )
        music_theory3 = ResourceModel(
            name = "Notes, Chords and Melodies",
            description = "This lesson is on chords, how they work, and the basic intervals that make them up. Learning the underlying music theory behind chords will not only allow you to find any chord you want, anywhere you want, it will also give you a solid foundation to build your entire understanding of music theory on.",
            # TODO: should be a constant
            resource_type = "VIDEO",
            source = "https://www.youtube.com/watch?v=rZr5k1_9Dds",
            # source_author = "",
            # source_date = "",
            contributor = nina_key,
        )
        music_theory4 = ResourceModel(
            name = "Chord Creation",
            description = "A video on easy music theory technique to figuring out chord creation.",
            # TODO: should be a constant
            resource_type = "VIDEO",
            source = "https://www.youtube.com/watch?v=g9DTgJFbcvg",
            # source_author = "",
            # source_date = "",
            contributor = nina_key,
        )
        music_theory5 = ResourceModel(
            name = "Making Melodies",
            description = "Melodies are a foundation to any sort of music production and this tutorial teaches you how to craft together melodies.",
            # TODO: should be a constant
            resource_type = "VIDEO",
            source = "https://www.youtube.com/watch?v=pMDOwZkH3y0",
            # source_author = "",
            # source_date = "",
            contributor = nina_key,
        )
        ndb.put_multi(
            music_theory1,
            music_theory2,
            music_theory3,
            music_theory4,
            music_theory5
        )
        # LaunchList
        music_theory = LaunchListModel(
            name = "Music Theory",
            description = "Theory is a very useful tool, as it is a logic that makes sense of what sounds good in music and why. But what is theory even used for? How does it benefit you? As a beginner, it quickly enables music to make much more sense. As you practice composing and producing, it will open doors to more complicated, layer-driven forms of writing that connects your music to itself in various ways and makes it sound good and powerful.",
            contributor = [ nina_key ],
            resources = [
                music_theory1.key,
                music_theory2.key,
                music_theory3.key,
                music_theory4.key,
                music_theory5.key
            ]
        )
        music_theory.put()
        # LaunchList - sub-topic
        music_production = LaunchListModel(
            name = "Music Production",
            description = "Nina Krishnan’s LaunchList for Music Production",
            launchlists = [ music_theory ],
            contributor = [ nina_key ],
            rating = ""
        )
        music_production.put()
        # add sub-topic to user's profile
        nina.launchlists = [ music_production.key, music_theory.key ]
        # add sub-topic to topic
        self.subtopics = [ music_production.key ]
        # update user with resources
        nina.resources = [
            music_theory1,
            music_theory2,
            music_theory3,
            music_theory4,
            music_theory5
        ]
        # save to ndb
        ndb.put_multi(
            nina,
            music_production,
            music_theory,
            music_theory1,
            music_theory2,
            music_theory3,
            music_theory4,
            music_theory5
        )

    @classmethod
    def get_topic( cls, urlsafe_key ):
        topic_key = ndb.Key( urlsafe=urlsafe_key )
        topic = topic_key.get()
        subtopics = topic.subtopics

        # TODO: remove this when not debugging
        if len( subtopics ) == 0:
            topic.create_subtopics()
            return False
        else:
            for index, item in enumerate( subtopics ):
                subtopic_key = subtopics[ index ]
                subtopics[ index ] = SubTopicModel.get_dict( subtopic_key );

        topic_dict = topic.to_dict()
        topic_dict[ "subtopics" ] = subtopics
        topic_dict[ "key" ] = topic_key.urlsafe()

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
    launchlists = ndb.KeyProperty( repeated=True )
    num_launchlists = ndb.IntegerProperty( default=0 )

    # def get_dict( self ):
    #     subtopic_dict = self.to_dict();

    @classmethod
    def get_dict( cls, key ):
        subtopic = key.get()
        subtopic_dict = subtopic.to_dict( exclude = ["topics", "launchlists"] )
        subtopic_dict["key"] = subtopic.key.urlsafe()
        return subtopic_dict

    # TODO: create batch add_launchlists function for effi
    # TODO: check if ll is already in subtopic
    def add_launchlist( self, ll ):
        if not isinstance( ll, LaunchListModel ):
            return False

        ll.subtopics.append( self.key )
        ll_key = ll.put()
        self.launchlists.append( ll_key )

        return ll_key

    def create_launchlists( self, number = 5 ):
        launchlist_keys = []

        for num in range( 0, number ):
            ll = LaunchListModel(
                name = "Launch List",
                description = "A description",
            )
            ll.create_resources( number )
            launchlist_keys.append( self.add_launchlist( ll ) )

        self.put()
        return launchlist_keys


class LaunchListModel( ndb.Model ):
    name = ndb.StringProperty( default="How to fleece rubes?", required=True )
    description = ndb.TextProperty( default="You will learn.", required=True )
    parent_launchlists = ndb.KeyProperty( repeated=True )
    child_launchlists = ndb.KeyProperty( repeated=True )
    subtopics = ndb.KeyProperty( repeated=True )
    # list of Resoruce that belong to this LaunchList
    # only holds refrences, empty list by default
    resoruces = ndb.KeyProperty( repeated=True )
    # num_resoruce = ndb.IntegerProperty( default=0 )
    # rating = ndb.RatingProperty()
    # the user that created this tutorial
    contributor = ndb.KeyProperty()
    # users that can edit this tutorial
    editors = ndb.KeyProperty( repeated=True )
    rating = ndb.StringProperty()

    def create_resources( self, number = 6 ):
        resource_keys = []

        for num in range(0, number ):
            resource = ResourceModel(
                name = "Resource",
                description = "A description",
                source = "google.com",
                resource_type = "LINK"
            )
            resource_keys.append( self.add_resource( resource ) )

        # self.put()
        return resource_keys

    # TODO: check for duplicates
    # TODO: create bulk add resources method
    def add_resource( self, resource ):
        if not isinstance( resource, ResourceModel ):
            return False

        resource.launchlists.append( self.key )
        resource_key = resource.put()
        self.resoruces.append( resource_key )

        return resource_key


class ResourceModel( ndb.Model ):
    name = ndb.StringProperty( default="How to fleece rubes?", required=True )
    description = ndb.TextProperty( default="You will learn.", required=True )
    source = ndb.StringProperty( default="mta.io/#", required=True)
    # resource_type = ndb.KeyProperty()
    resource_type = ndb.StringProperty( default="TEXT", required=True )
    # rating = ndb.RatingProperty()
    # source_author = ndb.StringProperty()
    # source_date = ndb.DateProperty()
    # the user that added to this resource
    contributor = ndb.KeyProperty()
    date_created = ndb.DateProperty( auto_now_add=True )
    date_update = ndb.DateProperty( auto_now=True )
    # list of LaunchLists that this Resource belong to
    # only holds refrences, empty list by default
    launchlist = ndb.KeyProperty( repeated=True )
    # num_launch_list = ndb.IntegerProperty( default=0 )
    rating_smily = ndb.StringProperty()
    # list of launchlist keys
    launchlists = ndb.KeyProperty( repeated=True )
    crawled = ndb.BooleanProperty()


class AccountModel( ndb.Model ):
    first_name = ndb.StringProperty( default="Friedrich", required=True )
    last_name = ndb.StringProperty( default="Nietzsche", required=True )
    # profile_type = ndb.StringProperty( required=True )
    # TODO: needs to be validated
    email = ndb.StringProperty( required=True )
    description = ndb.TextProperty( default="Iam the UberMentch!", required=True )
    # "A user with a Google account"
    user = ndb.UserProperty( auto_current_user=True, auto_current_user_add=True )
    date_created = ndb.DateProperty( auto_now_add=True )
    date_update = ndb.DateProperty( auto_now=True )
    # list of LaunchLists that this Account Created
    # only holds refrences, empty list by default
    launchlists = ndb.KeyProperty( repeated=True )
    # list of LaunchLists that this Account Created
    resources = ndb.KeyProperty( repeated=True )


class SubscriberModel( ndb.Model ):
    # TODO: email needs to be validated
    email = ndb.StringProperty( required=True )
    first_name = ndb.StringProperty( default="Friedrich" )
    last_name = ndb.StringProperty( default="Nietzsche" )
    occupation = ndb.StringProperty( default="Deranged Lunatic" )
    age = ndb.IntegerProperty( default=0 )
