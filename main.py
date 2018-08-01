import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from webapp2_extras import sessions

class Albums(ndb.Model):
    image_url   = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

new_images = []

class MainPage(BaseHandler):
    def get(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/login.html')
        self.response.write(login_template.render())

class frontpage(BaseHandler):
    def get(self):
        front_image = self.session.get('teddy')
        bio_text = self.session.get('family-message')
        family_name = self.session.get('familyName')

        frontpage_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')

        upload_url = blobstore.create_upload_url('/upload_photo')

        front_page_dictionary = {
            "front_image": front_image,
            "bio_text": bio_text,
            "family_name": family_name,
            "upload_url" : upload_url
        }

        self.response.write(frontpage_template.render(front_page_dictionary))

    def post(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')

        front_image = self.request.get('url-front')
        self.session['teddy'] = front_image

        bio_text = self.request.get('bio')
        self.session['family-message'] = bio_text

        family_name = self.request.get('family-name')
        self.session['familyName'] = family_name

        front_page_dictionary = {
            "front_image": front_image,
            "bio_text": bio_text,
            "family_name": family_name
        }

        self.response.write(login_template.render(front_page_dictionary))

class Collection(BaseHandler):
    def get(self):
        collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')

        new_images = self.session.get('new_images')
        family_members = self.session.get('family-members-photo')

        collection_dictionary = {
            "new_images": new_images,
        }

        self.response.write(collection_template.render(collection_dictionary))

    def post(self):
        collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')

        picture = self.request.get('add-image')
        desc = self.request.get('family-member')

        album = Albums(image_url=picture, description=desc)
        album.put()

        all_images = Albums.query().fetch()
        set = {
            'picture': picture,
            'description': desc
        }
        if self.session.get("new_images") is None:
           self.session["new_images"] = []

        self.session.get("new_images").append(set)

        self.session['photo'] = new_images

        family_members = self.request.get('family-member')
        self.session['family-members-photo'] = family_members

        images_descriptions = {
            "new_images": self.session.get("new_images"),
            'all_images': all_images
        }

        self.response.write(collection_template.render(images_descriptions))

class Timeline(webapp2.RequestHandler):
    def get(self):
        timeline_template = JINJA_ENVIRONMENT.get_template('templates/Timeline.html')
        self.response.write(timeline_template.render())

class Tree(webapp2.RequestHandler):
    def get(self):
        tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
        self.response.write(tree_template.render())

class Profile(webapp2.RequestHandler):
    def get(self):
        profile_template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        self.response.write(about_template.render())

class About(webapp2.RequestHandler):
    def get(self):
        about_template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(about_template.render())

class Settings(webapp2.RequestHandler):
    def get(self):
        settings_template = JINJA_ENVIRONMENT.get_template('templates/settings.html')
        self.response.write(settings_template.render())

# class User_info(BaseHandler):
    # def get(self):
    #     user_template = JINJA_ENVIRONMENT.get_template('templates/login.html')
    #     self.response.write(user_template.render())
    # def post(self):
    #     userid = self.request.get('id')
    #     self.session['user'] = userid
    #     print("Working")
    #     self.redirect('/frontpage')

#
#         self.response.out.write(format(upload_url))

# class UserPhoto(ndb.Model):
#     # user = ndb.StringProperty()
#     blob_key = ndb.BlobKeyProperty()

# class PhotoUploadFormHandler(webapp2.RequestHandler):
#     def get(self):
#         upload_url = blobstore.create_upload_url('/upload_photo')
#         self.response.out.write(upload_url)
#
# class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
#     def post(self):
#         upload = self.get_uploads()[0]
#         user_photo = UserPhoto(
#             blob_key=upload.key())
#         user_photo.put()
#         self.response.write(upload)
#         # self.redirect('/view_photo/%s' % upload.key())
#         print(user_photo.blob_key)
#
#
# class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
#     def get(self, photo_key):
#         if not blobstore.get(photo_key):
#             self.error(404)
#         else:
#             self.send_blob(photo_key)



config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '1234',
}



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/frontpage', frontpage),
    ('/collection', Collection),
    ('/timeline', Timeline),
    ('/tree', Tree),
    ('/about', About),
    ('/profile', Profile),
    # ('/userinfo', User_info),
    ('/settings', Settings),
    # ('/', PhotoUploadFormHandler),
    # ('/upload_photo', PhotoUploadHandler),
    # ('/view_photo/([^/]+)?', ViewPhotoHandler),
], debug=True, config=config)
