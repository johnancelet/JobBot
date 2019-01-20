import os

from Shared.constants import Const


class UserConfig(Const):
    EMAIL = os.environ['EMAIL']
    PASSWORD = os.environ['PASSWORD']

    class Path(Const):
        JSON_TAG_BLURBS = r'blurbs.json'
        # TODO: Add this as an arguement
        DEFAULT_RESUME = os.environ.get('DEFAULT_RESUME') or '' 

    class Settings(Const):
        # Booleans
        USE_ALT_END_TAG = True
        USE_LONG_TEXT = False
        IS_DRY_RUN = False
        WILL_RELOAD_TAGS_AND_BLURBS = True

        MINIMUM_NUMBER_MATCHING_KEYWORDS = 1

    class Default(Const):
        EXPERIENCE = 2
        CITY = 'Vancouver'