from google.appengine.ext import ndb

class Family_Member(ndb.Model):
   name = ndb.StringProperty(required=True)
   description = ndb.StringProperty(required=True)
   type = ndb.StringProperty(required=True)

class Picture(ndb.Model):
   title = ndb.StringProperty(required=True)
   url = ndb.StringProperty(required=True)
   tags = ndb.StringProperty(required=True)
