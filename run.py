import argparse
from enum import Enum
import urllib.parse as urlparse

from Bot.AngelBot import AngelBot
from Bot.LinkedIn.LinkedInBot import LinkedInBot

from userconfig import UserConfig


class JobBot(Enum):
    AngelBot = 1
    LinkedInBot = 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run JobBot')
    parser.add_argument('option', type=int, help="Pick JobBot, by typing it's option number")

    unformatted_display_query = "Bot being initialized with this query:\n\n {0}"

    args = parser.parse_args()

    if args.option == JobBot.AngelBot.value:
        query_parameters = {"types": "internship",
                            "roles": [
                                "Software Engineer"
                                ],
                            "last_active" : "30",
                            "excluded_keywords": ["unpaid"]
                            }
        print(unformatted_display_query.format(query_parameters))

        bot = AngelBot(UserConfig())
        bot.login()
        #bot.gather(query_parameters)
        bot.apply()
        bot.shut_down()

    elif args.option == JobBot.LinkedInBot.value:
        bot = LinkedInBot(UserConfig())
        bot.login()
        query_string = r'company=NOT%20TEKsystems&' \
                       r'facetGeoRegion=%5B"ca%3A0"%5D&' \
                       r'facetNetwork=%5B"S"%2C"O"%5D&' \
                       r'origin=FACETED_SEARCH&' \
                       r'title=Technical%20Recruiter%20'
        bot.search_people_by_query(query_string)
        bot.shut_down()
    else:
        print('Pick one of these options:')
        for bot in JobBot:
            print('{0} : {1}'.format(bot.value, bot.name))
