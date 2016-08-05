#!/usr/bin/python
# -*- coding: ascii -*-
# the basics
import logging, random

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
from rest_model import RestApi, RestApis, RestModel, RESPONSE_STATUS

app = Flask( __name__ )
api = Api( app )
# TODO: turn app.debug and developing off when launching
app.debug = True
DEVELOPING = True
LAUNCHLIST_NAMES = [
    "How to perform dentistry on Unicorns and other mythical beasts",
    "Forger for dummies",
    "Cabinet installation for those who suffer from hylophobia",
    "How to play PokeMon Go discreetly at work, school, or during sex",
    "Tinder and Grindr for grandparents",
    "Talking to teenagers, with a primer on how loud you should yell",
    "Communism 101 for Bernie fans: comrades with benefits",
    "Windsurfing for Noobs - full of sound and fury, signifying nothing",
    "How to become a web developer: not for arachnophobes",
    "Music Production for the deaf",
    "Coach-surfing, a guide for professional mooches and layabouts",
    "Launching a Startup - Yes it counts as employment mom!",
    "An introduction to Neocolonialism in Black Africa",
    "Multiple Inheritance: there will be blood",
    "Bootstrapping Primer: We already have less!"
]
LAUNCHLIST_DESCRIPTIONS = [
    "I CAUGHT this morning morning's minion, king-	\n",
    "  dom of daylight's dauphin, dapple-dawn-drawn Falcon, in his riding	\n",
    "  Of the rolling level underneath him steady air, and striding	\n",
    "High there, how he rung upon the rein of a wimpling wing	\n",
    "In his ecstasy! then off, off forth on swing,	        \n",
    "  As a skate's heel sweeps smooth on a bow-bend: the hurl and gliding	\n",
    "  Rebuffed the big wind. My heart in hiding	\n",
    "Stirred for a bird,-the achieve of; the mastery of the thing!	\n",
    "Brute beauty and valour and act, oh, air, pride, plume, here	\n",
    "  Buckle! AND the fire that breaks from thee then, a billion	  \n",
    "Times told lovelier, more dangerous, O my chevalier!	\n",
    "  No wonder of it: sheer plod makes plough down sillion	\n",
    "Shine, and blue-bleak embers, ah my dear,	\n",
    "  Fall, gall themselves, and gash gold-vermillion."
]



# NOTE: we should use something else for storing headings
# NOTE: JsonProperty and use a dict to hold the heading?
class LaunchListHeading( ndb.Model ):
    # the name that is displayed to the user
    name = ndb.StringProperty( default="Heading", required=True )
    # the launchlist this heading belongs to
    launchlist = ndb.KeyProperty( required=True )
    # the place in the launchlist of this heading
    index = ndb.IntegerProperty( required=True )
    font_size = ndb.IntegerProperty( default=16 )
    # NOTE: use IntegerProperty instead of string? convert hec to dec?
    font_color = ndb.StringProperty( default="#000000" )



class LaunchList( RestModel ):

    # TODO: do not allow multiline names
    # model information
    topics = ndb.KeyProperty( repeated=True )
    num_topics = ndb.ComputedProperty(
        lambda self: len(self.topics) )
    parent_launchlists = ndb.KeyProperty( repeated=True )
    num_parent_launchlists = ndb.ComputedProperty(
        lambda self: len(self.parent_launchlists) )
    child_launchlists = ndb.KeyProperty( repeated=True )
    num_child_launchlists = ndb.ComputedProperty(
        lambda self: len(self.child_launchlists) )
    resources = ndb.KeyProperty( repeated=True )
    num_resources = ndb.ComputedProperty(
        lambda self: len(self.resources) )
    communities = ndb.KeyProperty( repeated=True )
    num_communities = ndb.ComputedProperty(
        lambda self: len(self.communities) )
    rating = ndb.IntegerProperty( default=-1 )
    headings = ndb.StructuredProperty( LaunchListHeading, repeated=True )


    # Creates set of dummy launchlists for passed object
    @classmethod
    def create_dummy_launchlists( cls, parent_model, parent=None ):
        if parent is None:
            parent = int( ( ( random.random() ) * 10 ) % 3 - 1 )

        launchlists = []
        # entities = [parent_model]
        num_lists = int( ( random.random() * 100 ) % 10 ) + 3

        for num in range( 0 , num_lists ):
            name = LAUNCHLIST_NAMES[
                int( ( random.random() * 100 )
                            % len( LAUNCHLIST_NAMES ) )
            ]
            description = LAUNCHLIST_DESCRIPTIONS[
                int( ( random.random() * 100 )
                            % len( LAUNCHLIST_DESCRIPTIONS ) )
            ]
            launchlist = cls(
                name=name,
                description=description
            )

            added = False
            if type( parent_model ).__name__ == "Topic":
                added = launchlist.edit_topics(
                    topic=parent_model,
                    add=True,
                    safe=True
                )
            elif type( parent_model ) == cls:
                added = launchlist.edit_launchlists(
                    launchlist=parent_model,
                    parent=True,
                    add=True,
                    safe=True
                )

            if not added:
                continue

            # entities.append( launchlist )
            launchlist.put()
            launchlists.append( launchlist.to_dict( includes=[
                "name", "description", "icon", "rating" ]) )

            if type( parent_model ) is not cls:
                parent_model.add_launchlist(
                    launchlist=launchlist
                )
            else:
                parent_model.edit_launchlists(
                    launchlist=launchlist,
                    parent=parent,
                    add=True,
                    safe=True
                )

        # the call to to_dict saves unsaved entities, we just need to save parent
        # logging.log( logging.INFO, entities )
        # save all the new launchlist and their parent
        # ndb.put_multi( entities )
        # logging.log( logging.INFO, parent_model )
        parent_model.put()

        return launchlists


    # Get list of items to exclude from to_dict
    @classmethod
    def get_excludes( cls, new_excludes=None ):
        return super( LaunchList, cls ).get_excludes(
            [
                "resources", "topics", "child_launchlists",
                "parent_launchlists", "headings", "communities"
            ] )


    # Get list of properties necessary to create this model
    @classmethod
    def get_required_properties( cls, new_requires=None ):
        return super( LaunchList, cls ).get_required_properties(
            [
                "description",
                "icon"
            ]
        )


    # Adds topic to the launchlist
    def add_topic( self, topic, safe=False ):
        if not safe:
            if type( topic ).__name__ != "Topic":
                return False

        key = topic.key
        if key in self.topics:
            return  False

        self.topics.append( key )
        self.num_topics += 1

        return True


    # # NOTE: how expensive are these calls to type?
    # # Adds launchlist to launchlist as its parent or child
    # def add_launchlist( self, launchlist, parent=False, safe=False ):
    #     if not safe:
    #         if type( launchlist ) != type( self ):
    #             return False
    #
    #     key = launchlist.key
    #     if key == self.key:
    #         return False
    #
    #     if key in self.parent_launchlists or key in self.child_launchlists:
    #         return False
    #
    #     if parent:
    #         self.parent_launchlists.append( key )
    #     else:
    #         self.child_launchlists.append( key )
    #
    #     return True


    def edit_topics( self, topic, add=True, safe=False ):
        if not safe:
            if type( topic ).__name__ != "Topic":
                return False

        new_list = self.edit_list( self.topics, topic.key, add )

        if new_list is False:
            return False

        self.topics = new_list

        return True


    def edit_launchlists( self, launchlist,
                          parent=False, add=True, safe=False ):
        if not safe:
            if type( launchlist ) != type( self ):
                return False

        key = launchlist.key

        # edit parent launchlists
        if parent:
            old_list = self.parent_launchlists
            new_list = self.edit_list( old_list, key, add )

            if new_list is False:
                return False

            self.parent_launchlists = new_list

        # edit child launchlists
        else:
            old_list = self.child_launchlists
            new_list = self.edit_list( old_list, key, add )

            if new_list is False:
                return False

            self.child_launchlists = new_list

        return True


    def edit_resources( self, topic, add=True, safe=False ):
        if not safe:
            if type( topic ).__name__ != "Resources":
                return False

        new_list = self.edit_list( self.resources, topic.key, add )

        if new_list is False:
            return False

        self.resources = new_list

        return True




class LaunchListApi( RestApi ):

    model_class = LaunchList




class LaunchListsApi( RestApis ):

    model_class = LaunchList

    # Retrieves all the launchlists associated with the model
    @classmethod
    def get( cls, urlsafe_key="", list_type="launchlist" ):
        model = cls.model_class.check_key(
            urlsafe_key=urlsafe_key,
            return_model=True,
            check_model_type=False
        )

        if model is False:
            return cls.make_response_dict(
                status=True,
                msg="Bad key"
            ), 400

        if list_type == "child":

            try:
                launchlists = model.child_launchlists
                num_launchlists = model.num_child_launchlists
            except AttributeError:
                return {"status": False, "msg": "no lists, bad key"}, 400

            list_type = False

        elif list_type == "parent":

            try:
                launchlists = model.parent_launchlists
                num_launchlists = model.num_parent_launchlists
                # logging.info(logging.INFO, launchlists)
            except AttributeError:
                return {"status": False, "msg": "no lists, bad key"}, 400

            list_type = True

        else:
            try:
                launchlists = model.launchlists
                num_launchlists = model.num_launchlists
            except AttributeError:
                return {"status": False, "msg": "no lists, bad type"}, 400

        # logging.info( logging.INFO, launchlists )

        if launchlists == []:
            lists = cls.model_class.create_dummy_launchlists(
                parent_model=model,
                parent=list_type # whether to add to child or parent launchlist
            )
            num_launchlists = len( lists )
        else:
            lists = cls.model_class.convert_keys_to_dicts(
                launchlists,
                includes=[ "name", "rating", "author",
                           "last_update", "num_resoruces" ]
            )

        return { "status": True,
                 "launchlists": lists,
                 "num_launchlists": num_launchlists
        }
