import re

from shared.helpers import Const
from shared.models import Person


class Constants(Const):
    WEBSITE_NAME = 'LinkedIn'

    class URL(Const):
        HOST = r'http://www.linkedin.com'
        LOGIN = r'https://www.linkedin.com/uas/login'
        SEARCH_PATH = r'/search/results/people/'

    class Name(Const):
        LOGIN_EMAIL = 'session_key'
        LOGIN_PASSWORD = 'session_password'

    class XPath(Const):
        NEWS_FEED = "//div[contains(@class,'sharing-create-share-view')]"
        SEARCH_RESULTS_LIST = "//ul[contains(@class,'results-list')]"
        NEXT_BUTTON = "//button[@class='next']"

        @staticmethod
        def find_link(link) -> str:
            return "//a[@href='{0}']".format(link)

    class Class(Const):
        SEARCH_RESULT = 'search-result'

        ACTOR_LINK = 'search-result__result-link'
        ACTOR_LOCATION = 'subline-level-2'

    class Regex(Const):
        position_string = re.compile(r"(.*)\sat\s(.*)")

    class String(Const):
        @staticmethod
        def person_visited(person: Person):
            print('Visited {0} : {1}'.format(person.name, person.title))

    class Constraint(Const):
        MAX_VISITS = 50

    class WaitTime(Const):
        LOGIN = 10
        SEARCH = 10
        VISIT = 15
        VIEW = 10

    # A bit against the grain (Of the rest of the page) but I think this is a better way of doing it
    class ProfilePage(Const):
        CLASS_SELECTOR_PERSON_NAME = 'pv-top-card-section__name'
        CLASS_SELECTOR_PERSON_HEADLINE = 'pv-top-card-section__headline'
        CLASS_SELECTOR_PERSON_COMPANY = 'pv-top-card-v2-section__company-name'
        CLASS_SELECTOR_PERSON_LOCATION = 'pv-top-card-section__location'
        CLASS_SELECTOR_CONNECTION_BUTTONS = 'pv-s-profile-actions'