@ -2,31 +2,13 @@ import webapp2
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
class MainPage(webapp2.RequestHandler):
    def get(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/login.html')
        self.response.write(login_template.render())
@ -35,28 +17,20 @@ class MainPage(BaseHandler):
        login_template = JINJA_ENVIRONMENT.get_template('templates/login.html')
        self.response.write(login_template.render())

class frontpage(BaseHandler):
class frontpage(webapp2.RequestHandler):
    def get(self):
        front_image = self.session.get('teddy')
        frontpage_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')

        front_page_dictionary = {
            "front_image": front_image,
        }

        self.response.write(frontpage_template.render(front_page_dictionary))
        self.response.write(frontpage_template.render())

    def post(self):
        login_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')

        front_image = self.request.get('url-front')
        self.session['teddy'] = front_image

        front_page_dictionary = {
            "front_image": front_image,
        }



        self.response.write(login_template.render(front_page_dictionary))

class Collection(webapp2.RequestHandler):
        about_template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(about_template.render())


class Settings(webapp2.RequestHandler):
    def get(self):
        about_template = JINJA_ENVIRONMENT.get_template('templates/settings.html')
        self.response.write(about_template.render())


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '1234',
}

        settings_template = JINJA_ENVIRONMENT.get_template('templates/settings.html')
        self.response.write(settings_template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/collection', Collection),
    ('/timeline', Timeline),
    ('/tree', Tree),
    ('/about', About),
    ('/settings', Settings)
], debug=True, config=config)
