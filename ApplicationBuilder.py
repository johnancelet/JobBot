from models import Blurb, Tag
from userconfig import UserConfig
import helpers
import nltk
import re


class ABConfig(helpers.Const):
    """
    The two regex captures in this class determine how you should
    format your file that contains tags and blurbs
    """
    REGEX_TAGS_CAPTURE = re.compile(r"'''(.*?)'''", re.DOTALL)
    REGEX_BLURB_CAPTURE = re.compile(r'"""(.*?)"""', re.DOTALL)
    START_TAG = 'start_tag'
    END_TAG = 'end_tag'
    REPLACE_COMPANY_STRING = r'{COMPANY}'
    BULLET_POINT = "-"


class ApplicationBuilder:
    def __init__(self, userConfig):
        # Create tables
        Blurb.create_table(fail_silently=True)
        Tag.create_table(fail_silently=True)
        self.userConfig = userConfig
        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    # TODO: Implement a function that can decide which resume to send
    def generateResume(self, description):
        pass

    def generateMessage(self, description, company, containMinBlurbs=False):
        """
        Returns a generated message based on the job description and company
        If 'containMinBlurbs' == True, then return None if not enough tags are in description
        --Useful to see if you are decent fit for the job
        :param description:
        :param company:
        :param containMinBlurbs:
        :return:
        """
        introTag = Tag.get(Tag.text == ABConfig.START_TAG)
        endTag = Tag.get(Tag.text == ABConfig.END_TAG)

        blurbIntro = Blurb.get(Blurb.id == introTag.blurb.id)
        blurbEnd = Blurb.get(Blurb.id == endTag.blurb.id)

        bestBlurbIds = self.pickBestBlurbs(description)
        messageBody = ''
        # If not enough blurbs
        if containMinBlurbs and len(set(bestBlurbIds)) < self.userConfig.MIN_BLURBS:
            return None

        for bId in bestBlurbIds:
            blurb = Blurb.get(Blurb.id == bId)
            messageBody += ABConfig.BULLET_POINT + blurb.text + "\n"

        finalMessage = "{0}\n{1}\n\n{2}".format(blurbIntro.text, messageBody, blurbEnd.text)
        return finalMessage.replace(ABConfig.REPLACE_COMPANY_STRING, company)

    def pickBestBlurbs(self, jobDescription):
        tokens = nltk.word_tokenize(jobDescription)
        words = set([word.lower() for word in tokens if word.isalpha()])
        words = [self.lemmatizer.lemmatize(word) for word in words]
        blurbIdList = []
        for word in words:
            tagQuery = Tag.select().where(Tag.text == word)
            for tag in tagQuery:
                blurbIdList.append(tag.blurb.id)

        # Avoid blurb repeats
        return sorted(set(blurbIdList))

    def readTagBlurbs(self, filePath):
        with open(filePath, "r") as f:
            content = f.read()
            list_list_tags = re.findall(ABConfig.REGEX_TAGS_CAPTURE, content)
            list_blurbs = re.findall(ABConfig.REGEX_BLURB_CAPTURE, content)
            if len(list_list_tags) == len(list_blurbs):
                for i in range(0, len(list_blurbs)):
                    list_tags = list_list_tags[i].split(',')
                    blurbId = self.createBlurb(list_blurbs[i].strip())
                    self.addTagsToBlurb(list_tags, blurbId)
            else:
                print('Length of tags and blurbs do not match. Perhaps you have a formatting error?')

    def getBlurbs(self):
        return Blurb.select()

    def getTags(self):
        return Tag.select()

    def createBlurb(self, blurb):
        b = Blurb.create(text = blurb)
        return b.id

    def addTagsToBlurb(self, tags, blurbId):
        query = Blurb.select().where(Blurb.id == blurbId)
        if query.exists():
            for tag in tags:
                self._addTagToBlurb(tag, blurbId)
        else:
            print('Blurb id: {0} is not in the database!'.format(blurbId))

    def _addTagToBlurb(self, tag, blurbId):
        b = Blurb.select().where(Blurb.id == blurbId)
        t = Tag.create(text=tag.lower().strip(), blurb=b)

    def resetAllTables(self):
        Tag.drop_table()
        Blurb.drop_table()

        Blurb.create_table(fail_silently=True)
        Tag.create_table(fail_silently=True)

if __name__ == "__main__":
    a = ApplicationBuilder(UserConfig)
    desc = '''Lokafy is an early-stage startup based in Toronto that has a mission to change the way people travel, to make it more about the people we met and not just the places we see. We connect travellers with passionate locals - offering an experience that’s like having a friend show you around the city. You can see a one-minute video that explains the concept here: https://lkfy.co/2a9oCUR
Lokafy is expanding to cities all over the world and is starting to gain some good traction. If you’d like to get in on the ground level of a promising startup, this is the opportunity you’ve been waiting for.
We would like to add 1-2 developers (front/back and full stack) to the team so that we can make complete our website re-design project and start moving forward with new functionality based on our growth objectives.
You would be working closely with a small team (Founder, Back-end Developer, Designer/Front-End Developer and other marketing and business development interns) where you have the opportunity to brainstorm ideas, try out new ways of doing things and learn from a team with diverse experience.
This internship would be a great opportunity to work on an early stage startup to really shape the user experience as opposed to just making incremental improvements at more established companies or startups. There is a designer on the team along with 3 other developers (including the founder). The designs are all ready to go and a lot of the front end development is ready so we'd like to add someone to the team who can hit the ground running and allow us to launch the re-designed website quickly. For those are a bit more experience, there is opportunity to take a lead the development team to build up experience for more senior roles.
We'd love to work with someone who:
- Has experience with Django or Angular JS
- Is interested in learning and is resourceful (can figure stuff out by researching online)
- Is proud of their work and loves challenges
- Is willing to meet in person regularly
- Loves to share knowledge and exchange ideas
What we have to offer:
- A chance to learn from an early stage startup that you could use to build your own (or find work at a more established startup)
- Opportunity to contribute to laying the foundation of a startup
- A collaborative environment where we set ambitious goals
- Work with a small team and learn from people with diverse skills and backgrounds
- A travel stipend of $150/month for full time interns
- Excellent experience that should allow you to show employers solid skills as a developer in 2-3 months
Job Type: Internship
Job Location:
Toronto, ON
Required experience:
Angularjs: 1 year
Django: 1 year'''
    a.resetAllTables()
    a.readTagBlurbs('blurbs.txt')
    print(a.generateMessage(desc, 'comp'))