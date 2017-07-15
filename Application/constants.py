from helpers import Const
import re


class ApplicationBuilderConstants(Const):
    """
    The two regex captures in this class determine how you should
    format your file that contains tags and blurbs
    """
    REGEX_TAGS_CAPTURE = re.compile(r"'''(.*?)'''", re.DOTALL)
    REGEX_BLURB_CAPTURE = re.compile(r'"""(.*?)"""', re.DOTALL)
    START_TAG = 'start_tag'
    END_TAG = 'end_tag'
    END_TAG_ALT = 'end_tag_alt'
    REPLACE_COMPANY_STRING = r'{COMPANY}'
    BULLET_POINT = "-"

    # Possible websites
    INDEED = 'Indeed'

    class QuestionNeedle(Const):
        """
        Constants used to determine which question type the question is
        """
        RESUME = 'resume'
        MESSAGE = 'cover letter'
        LIST_LOCATION = ['located', 'are you in']
        EXPERIENCE = 'experience'
        LANGUAGE = 'do you speak'
        CERTIFICATION = 'do you have'
        LIST_EDUCATION = ['education', 'have you completed']
        LIST_CONTACT_INFO = ['name', 'email', 'phone number']

    # TODO: Use custom field in peewee
    class QuestionTypes(Const):
        RESUME = 'resume'
        MESSAGE = 'message'
        LOCATION = 'location'
        EXPERIENCE = 'experience'
        CERTIFICATION = 'certification'
        CONTACT_INFO = 'contact_info'
        LANGUAGE = 'language'
        EDUCATION = 'education'
