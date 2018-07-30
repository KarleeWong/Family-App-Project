import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        frontpage_template = JINJA_ENVIRONMENT.get_template('templates/frontpage.html')
        self.response.write(frontpage_template.render())


class Collection(webapp2.RequestHandler):
    def get(self):
        collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')
        self.response.write(collection_template.render())

class Timeline(webapp2.RequestHandler):
    def get(self):
        timeline_template = JINJA_ENVIRONMENT.get_template('templates/timeline.html')
        self.response.write(timeline_template.render())

class Tree(webapp2.RequestHandler):
    def get(self):
        tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
        self.response.write(tree_template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/collection', Collection),
    ('/timeline', Timeline),
    ('/tree', Tree)
], debug=True)
