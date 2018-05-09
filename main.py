import os

import dotenv

from selenium import webdriver

from Bot.LinkedIn.LinkedInBot import LinkedInBot, LinkedInConfig

if __name__ == "__main__":
    dotenv.load_dotenv(".env")

    bot = LinkedInBot(
        webdriver.Chrome(os.environ.get("CHROME_DRIVER_PATH")),
        LinkedInConfig(os.environ.get('EMAIL'), os.environ.get('LINKEDIN_PASSWORD'))
    )
    bot.login()
    query_string = r'title=University%20Recruiter%20'
    bot.search_people_by_query(query_string)
    bot.shut_down()
