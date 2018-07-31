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

        new_image = self.session.get('photo')
        family_members = self.session.get('family-members-photo')

        collection_dictionary = {
            "new_image": new_image,
            "family_members": family_members
        }

        self.response.write(collection_template.render(collection_dictionary))

    def post(self):
        collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')

        new_image = self.request.get('add-image')
        self.session['photo'] = new_image

        family_members = self.request.get('family-member')
        self.session['family-members-photo'] = family_members

        collection_dictionary = {
            "new_image": new_image,
            "family_members": family_members
        }

        self.response.write(collection_template.render(collection_dictionary))

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
