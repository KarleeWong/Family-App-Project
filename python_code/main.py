import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class EnterInfoHandler(webapp2.RequestHandler):
    def get(self):
        Welcome_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')
        self.response.write(frontpage_template.render())


class ImageImporter(webapp2.RequestHandler):
    def get(self):
        frontpage_template = JINJA_ENVIRONMENT.get_template('pages_outline/frontpage.html')
        self.response.write(frontpage_template.render())
    def post(self):
        self.response.write('hi')

app = webapp2.WSGIApplication([
    ('/ok', EnterInfoHandler),
    ('/', ImageImporter)
], debug=True)
