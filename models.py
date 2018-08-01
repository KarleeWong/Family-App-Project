from google.appengine.ext import ndb

class Profile(ndb.Model):
    profile_face = nbd.StringProperty(required=True)
    profile_description = nbd.StringProperty(required=True)
    first_name = nbd.StringProperty(required=True)
    last_name = nbd.StringProperty(required=True)
    #full_name = nbd.StringProperty(required=True)
