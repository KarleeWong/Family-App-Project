import webapp2
import jinja2
import os

from webapp2_extras import sessions

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

        front_page_dictionary = {
            "front_image": front_image,
            "bio_text": bio_text,
            "family_name": family_name
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

        set = {
            'picture': self.request.get('add-image'),
            'description': self.request.get('family-member')
        }

        if self.session.get("new_images") is None:
            self.session["new_images"] = []

        self.session.get("new_images").append(set)

        # self.session['photo'] = new_images
        #
        # family_members = self.request.get('family-member')
        # self.session['family-members-photo'] = family_members

        images_descriptions = {
            "new_images": self.session.get("new_images")
        }

        self.response.write(collection_template.render(images_descriptions))

class Timeline(BaseHandler):
    def get(self):
        timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')

        entries = self.session.get('entries')

        timeline_dictionary = {
            "entries": entries,
        }

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

        self.session.get("entries").append(entry)
        
        entry_dictionary = {
            "entries": self.session.get("entry")
        }

        self.response.write(timeline_template.render(entry_dictionary))

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
    ('/settings', Settings)
], debug=True, config=config)
