from typing import List

from bs4 import BeautifulSoup

from selenium import webdriver

from bot.LinkedIn.constants import Constants as LC

from shared.models import Person, ConnectionState
from shared.selenium_helpers import get_rendered_html


class LinkedInParser:
    def get_person_links_from_results_page(self, driver: webdriver.Chrome) -> List[str]:
        rendered_html = get_rendered_html(driver)
        soup = BeautifulSoup(rendered_html, 'html.parser')
        list_results_soup = soup.find_all('div', attrs={'class': LC.Class.SEARCH_RESULT})

        links: List[str] = []
        for soup in list_results_soup:
            relative_link = soup.find('a', attrs={'class': LC.Class.ACTOR_LINK})['href']
            link = LC.URL.HOST + relative_link
            links.append(link)

        return links

    def save_person_from_profile_page(self, driver: webdriver.Chrome, person_link: str):
        def calculate_connection_state(pageSoup: BeautifulSoup)-> ConnectionState:
            all_text = ''.join([
                element_soup.text for element_soup in
                pageSoup.findAll(
                    'button', attrs={'class': LC.ProfilePage.CLASS_SELECTOR_CONNECTION_BUTTONS}
                )
            ])

            if 'Message' in all_text:
                return ConnectionState.Connected
            elif 'Connect' in all_text:
                return ConnectionState.CanConnect
            else:
                return connection_state.CannotConnect

        rendered_html = get_rendered_html(driver)
        soup = BeautifulSoup(rendered_html, 'html.parser')

        connection_state = ConnectionState.CannotConnect
        soup.find('button', attrs={'class': LC.ProfilePage.CLASS_SELECTOR_CONNECTION_BUTTONS})

        p = (Person
          .insert(
            link=person_link,
            name=soup.find('h1', attrs={'class': LC.ProfilePage.CLASS_SELECTOR_PERSON_NAME}).text.strip(),
            headline=soup.find('h2',attrs={'class': LC.ProfilePage.CLASS_SELECTOR_PERSON_HEADLINE}).text.strip(),
            company=soup.find('span',attrs={'class': LC.ProfilePage.CLASS_SELECTOR_PERSON_COMPANY}).text.strip(),
            location=soup.find('h3', attrs={'class':LC.ProfilePage.CLASS_SELECTOR_PERSON_LOCATION}).text.strip(),
            visited=True,
            connection_state=calculate_connection_state(soup).value
        )
          .on_conflict('replace')
          .execute())
