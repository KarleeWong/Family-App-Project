import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ImageImporter(webapp2.RequestHandler):
    def post(self):
        frontpage_template = JINJA_ENVIRONMENT.get_template('Styling/frontpage.html')
        self.response.write(frontpage_template.render())