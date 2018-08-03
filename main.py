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
        if self.session.get("all_images") is None:
            collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')
            all_images = []
            set = {
                'picture': "https://i1.wp.com/www.gogreenexpo.co.nz/wp-content/uploads/2017/02/a-directory-placeholder.jpg",
                'description': "My Picture"
            }
            all_images.append(set)
            collection_dictionary = {
                "all_images": all_images
            }
            self.response.write(collection_template.render(collection_dictionary))
        else:
            all_images = self.session.get('all_images')
            collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')
            collection_dictionary = {
                "all_images": all_images,
                }

            self.response.write(collection_template.render(collection_dictionary))

    def post(self):
        collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')
        picture = self.request.get('add-image')
        description = self.request.get('family-member')

        picture = self.request.get('add-image')
        desc = self.request.get('family-member')

        album = Albums(image_url=picture, description=desc)
        album.put()

        all_images = Albums.query().fetch()
        set = {
            'picture': picture,
            'description': description
        }

        if self.session.get("all_images") is None:
            self.session["all_images"] = []

        self.session["all_images"] += [set]

        self.redirect('/collection')

class Timeline(BaseHandler):
    def get(self):
        if self.session.get("entries") is None:
            entries = []
            timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')
            opening = {
                "name": "Event Name",
                "date": "Event Date",
                "photo": "https://cortescoop.ca/wp-content/themes/gecko/assets/images/placeholder.png"
            }

            entries.append(opening)

            timeline_dictionary = {
                "entries": entries,
                }
            self.response.write(timeline_template.render(timeline_dictionary))
        else:
            entries = self.session.get('entries')
            timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')
            timeline_dictionary = {
                "entries": entries,
                }
            print("This is the timeline dictionary:")
            print(timeline_dictionary)
            self.response.write(timeline_template.render(timeline_dictionary))

    def post(self):
        timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')

        entry = {
            'date': self.request.get('event-date'),
            'name': self.request.get('event-name'),
            'photo': self.request.get('event-photo'),
            'member': self.request.get('event-member'),
            'des': self.request.get('event-des'),
        }

        if self.session.get("entries") is None:
            self.session["entries"] = []

        list_of_entries = self.session.get("entries")

        self.session["entries"] = list_of_entries + [entry]

        self.redirect('/timeline')

class TimelineEvent(BaseHandler):
    def get(self):
        if self.session.get("entries") is None:
            entries = []
            timeline_event_template = JINJA_ENVIRONMENT.get_template('templates/timeline_event.html')

            new = {
                'name': "Event Name",
                "date": "Event Date",
                "photo": "https://hackernest.com/assets/event-placeholder-62e479afe63ad167eb3bb6904efe06033f8b3d6e237983916b52adc98dd6cdb2.png",
                "des": "Describe your event"
            }

            opening = {
                "name": "Event Name",
                "date": "Event Date",
                "photo": "https://cortescoop.ca/wp-content/themes/gecko/assets/images/placeholder.png"
            }

            entries.append(opening)

            timeline_dictionary = {
                "entry": new,
                "entries": entries,
                }
            self.response.write(timeline_event_template.render(timeline_dictionary))
        else:
            timeline_event_template = JINJA_ENVIRONMENT.get_template('templates/timeline_event.html')
            entries = self.session.get('entries')
            print("THIS IS YOUR ID:")
            print(self.request.get("id"))
            timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')
            timeline_dictionary = {
                "entry": entries[int(self.request.get("id"))],
                "entries": entries
                }
            self.response.write(timeline_event_template.render(timeline_dictionary))

class Tree(BaseHandler):
    def get(self):
        if self.session.get("num-layer") is None:
            tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
            member = {
                "name": "Me",
                "picture": "http://www.europe-together.eu/wp-content/themes/sd/images/user-placeholder.svg",
                "description":"That's me! :)"
            }
            orgin = {
                "layers":int(1),
                "member": member
            }
            self.response.write(tree_template.render(orgin))
        elif self.session.get("family_member") is None:
            tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
            print("NUBMER LAYER!")
            print("Layer", self.session.get("num-layer"))
            member = {
                "name": "Me",
                "picture":"http://www.europe-together.eu/wp-content/themes/sd/images/user-placeholder.svg",
                "description":"That's me! :)"
            }
            
            orgin = {
                "layers":int(self.session.get("num-layer")),
                "member": member
            }

            self.response.write(tree_template.render(orgin))
        else:
            tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
            orgin = {
                "layers":int(self.session.get("num-layer")),
                "members": [self.session.get("family_member")],
            }

            self.response.write(tree_template.render(orgin))

    def post(self):
        family_member = {
            "name": self.request.get("family-member-name"),
            "picture": self.request.get("family-member-pic"),
            "description":self.request.get("family-member-des"),
            "layer":int(self.request.get("family-layer"))
        }

        self.session["family_member"] = family_member

        self.redirect('/tree')

class Profile(BaseHandler):
    def get(self):
        profile_template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
        orgin = {
            "layers":int(1),
            "name": "Me",
            "tree_pic":"https://www.f6s.com/images/profile-placeholder-user.jpg",
            "description": "That's me! :)"
        }
        self.response.write(profile_template.render(orgin))

class About(webapp2.RequestHandler):
    def get(self):
        about_template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(about_template.render())

class Settings(BaseHandler):
    def get(self):
        settings_template = JINJA_ENVIRONMENT.get_template('templates/settings.html')
        self.response.write(settings_template.render())

    def post(self):
        self.session["num-layer"] = self.request.get("layer-num")

        self.redirect('/settings')

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
    ('/timeline-event', TimelineEvent),
    ('/settings', Settings)
], debug=True, config=config)
