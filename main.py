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
        if self.session.get("all_images") is None:
            collection_template = JINJA_ENVIRONMENT.get_template('templates/collection.html')
            all_images = []
            set = {
                'picture': "https://i1.wp.com/www.gogreenexpo.co.nz/wp-content/uploads/2017/02/a-directory-placeholder.jpg",
                'description': "My Picture"
            }
            all_images.append(set)
            collection_dictionary = {
                "all_images": "all_images"
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
        if self.session.get("tree-layer") is 0:
            tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
            orgin = {
            "layers":int(1),
            "name": "Me",
            "tree_pic":"http://www.europe-together.eu/wp-content/themes/sd/images/user-placeholder.svg",
            "description": "That's me! :)"
            }
            self.response.write(tree_template.render(orgin))
        if self.session.get("family-member-name") is None:
            tree_template = JINJA_ENVIRONMENT.get_template('templates/tree.html')
            orgin = {
                "layers":int(self.request.get("tree-layer")),
                "name": "Me",
                "tree_pic":"http://www.europe-together.eu/wp-content/themes/sd/images/user-placeholder.svg",
                "description": "That's me! :)"
            }
            self.response.write(tree_template.render(orgin))
        tree_dictionary = {
            "layers": int(self.request.get("tree-layer")),
            "name": self.request.get("family-member-name"),
            "tree_pic": self.request.get("family-member-pic"),
            "description": self.request.get("family-member-des")
        }
        self.response.write(tree_template.render(tree_dictionary))

    def post(self):
        self.session["tree-layer"] = self.request.get("layer-num")

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
    ('/timeline-event', TimelineEvent),
    ('/settings', Settings)
], debug=True, config=config)
