from google.appengine.ext import db

class Topic( db.Model ):
    name = db.StringProperty( default="Psuedoscience", multiline=False, required=True )
    discription = db.TextProperty( default="It's real!!!", required=True )
    # display this topic on the front page?
    display_front_page = db.BooleanProperty( default=False )
    # list of SubTopics that under this Topic, only holds refrences
    # empty list by default
    sub_topics = db.ListProperty( item_type=db.ReferenceProperty )
    num_sub_topics = db.IntegerProperty( default=0 )


class SubTopic( db.Model ):
    name = db.StringProperty( default="Phrenology", multiline=False, required=True )
    discription = db.TextProperty( default="Can you feel me?", required=True )
    # list of Topics that this SubTopic belongs to
    # only holds refrences, empty list by default
    topics = db.ListProperty( item_type=db.ReferenceProperty )
    num_topics = db.IntegerProperty( default=1 )
    # list of Tutorials that belong to this SubTopic
    # only holds refrences, empty list by default
    tutorials = db.ListProperty( item_type=db.ReferenceProperty )
    num_tutorials = db.IntegerProperty( default=0 )


class Tutorial( db.Model ):
    name = db.StringProperty( default="How to fleece rubes?", required=True )
    discription = db.TextProperty( default="You will learn.", required=True )
    # list of Resoruce that belong to this Tutorial
    # only holds refrences, empty list by default
    resoruce = db.ListProperty( item_type=db.ReferenceProperty )
    num_resoruce = db.IntegerProperty( default=0 )
    rating = db.RatingProperty()


class Resoruce( db.Model ):
    name = db.StringProperty( default="How to fleece rubes?", required=True )
    discription = db.TextProperty( default="You will learn.", required=True )
    link = db.LinkProperty( default="mta.io/#", required=True)
    # resource_type = db.ReferenceProperty()
    resource_type = db.StringProperty( default="Text", required=True )
    rating = db.RatingProperty()


class Account( db.Model ):
    first_name = db.StringProperty( default="Friedrich", required=True )
    last_name = db.StringProperty( default="Nietzsche", required=True )
    discription = db.TextProperty( default="Iam the UberMentch!", required=True )
    # "A user with a Google account"
    user = UserProperty( auto_current_user=True, auto_current_user_add=True, required=True )
