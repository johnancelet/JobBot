import os

import dotenv

from selenium import webdriver

from bot.LinkedIn.LinkedInBot import LinkedInBot, LinkedInConfig

if __name__ == "__main__":
    # No idea why I have to do this but otherwise an old version of the variable gets used!
    # os.environ.pop("CHROME_DRIVER_PATH")


    dotenv.load_dotenv(dotenv.find_dotenv('.env', True))

    bot = LinkedInBot(
        webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH")),
        LinkedInConfig(os.environ.get('EMAIL'), os.environ.get('LINKEDIN_PASSWORD'))
    )
    bot.login()
    query_string = r'title=University%20Recruiter%20'
    bot.search_people_by_query(query_string)
    bot.close()
