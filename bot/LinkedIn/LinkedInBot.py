import time

from typing import NamedTuple

import peewee

from selenium import common, webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from bot.LinkedIn.constants import Constants as LC
from bot.LinkedIn.LinkedInParser import LinkedInParser

from shared.models import Person
from shared.selenium_helpers import scroll_infinitely, open_link_new_tab, adjust_zoom
from shared.helpers import sleep_after_function


class LinkedInConfig(NamedTuple):
    email: str
    password: str


class LinkedInBot:
    def __init__(self, driver: webdriver.Chrome, config: LinkedInConfig):
        self.config = config
        self.driver = driver
        self.parser = LinkedInParser()

        # Create necessary tables
        self._create_tables()

    def _create_tables(self):
        Person.create_table(fail_silently=True)

    def login(self):
        self.driver.get(LC.URL.LOGIN)
        element_login = self.driver.find_element(By.NAME, LC.Name.LOGIN_EMAIL)
        element_login.send_keys(self.config.email)

        self.driver.find_element(By.NAME, LC.Name.LOGIN_PASSWORD).send_keys(self.config.password)

        element_login.submit()

        # Wait for login to finalize
        WebDriverWait(self.driver, LC.WaitTime.LOGIN).until(
            EC.presence_of_element_located((By.XPATH, LC.XPath.NEWS_FEED))
        )

    def search_people_by_query(self, query_string: str):
        full_url = LC.URL.HOST + \
                   LC.URL.SEARCH_PATH + \
                   '?' + query_string
        self.driver.get(full_url)
        WebDriverWait(self.driver, LC.WaitTime.SEARCH).until(
            EC.presence_of_element_located((By.XPATH, LC.XPath.SEARCH_RESULTS_LIST))
        )

        count_visits = 0
        while True:
            scroll_infinitely(self.driver)
            adjust_zoom(self.driver, 50)
            person_links = self.parser.get_person_links_from_results_page(self.driver)

            for person_link in person_links:
                try:
                    p = Person.get(Person.link == person_link)
                    print(p)
                except peewee.DoesNotExist:
                    self.visit_profile(person_link)
                    count_visits += 1

            try:
                self.driver.find_element(By.XPATH, LC.XPath.NEXT_BUTTON).send_keys(Keys.ENTER)
                adjust_zoom(self.driver, 200)
            except common.exceptions.NoSuchElementException as e:
                print("Reached last page after: {0} visits".format(count_visits))
                break

            if count_visits > LC.Constraint.MAX_VISITS:
                break

    @sleep_after_function(LC.WaitTime.VISIT)
    def visit_profile(self, link: str):
        print("Visiting link: {0}".format(link))

        old_tab = self.driver.window_handles[0]
        open_link_new_tab(self.driver, link)

        new_tab = self.driver.window_handles[1]
        self.driver.switch_to.window(new_tab)

        self.parser.save_person_from_profile_page(self.driver, link)

        time.sleep(LC.WaitTime.VIEW)
        self.driver.close()
        self.driver.switch_to.window(old_tab)

    @sleep_after_function(LC.WaitTime.VIEW)
    def send_connection_request(self, person: Person):
        pass

    def close(self):
        self.driver.close()
