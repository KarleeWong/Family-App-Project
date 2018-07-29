import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))

class ImageImporter(webapp2.RequestHandler):
    def post(self):
        frontpage_template = JINJA_ENVIRONMENT.get_template('Styling/frontpage.html')
        self.response.write(frontpage_template.render())

app = webapp2.WSGIApplication([
    ('/II', ImageImporter)
], debug=True)
