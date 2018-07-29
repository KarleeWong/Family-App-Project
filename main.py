import webapp2
from google.appengine.api import urlfetch
import json
import os
import jinja2

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    # # extensions=['jinja2.ext.autoescape'],
    # autoescape=True


class SeedPage(webapp2.RequestHandler):
    #def get(self):

class MainPage(webapp2.RequestHandler):

    def get(self):
        template_info = jinja_current_dir.get_template("Page Outlines/frontpage.html")

        self.response.write(template_info.render())
        # self.response.write("<script>alert(\"hi\")</script>")

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/seed-page', SeedPage)
], debug=True)
