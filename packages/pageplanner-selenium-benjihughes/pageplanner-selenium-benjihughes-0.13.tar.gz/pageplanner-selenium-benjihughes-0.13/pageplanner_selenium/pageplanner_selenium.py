import os
import json
import urllib.parse
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import url_matches
from bs4 import BeautifulSoup as bsoup
from selenium.webdriver.chrome.options import Options


class GooglerChrome:

    search_url = 'https://www.google.com/?newwindow=1&num=100&gl=US'
    trigger_el_id = 'selenium-trigger-56789'
    js_location = os.path.join(os.path.dirname(__file__), 'controls.js')

    def __init__(self, path_to_driver):
        self.path_to_driver = path_to_driver
        self.driver = self.get_driver()

        self.focus_kw = None
        self.variant_kws = None
        self.pages = None

    def get_driver(self):
        driver_path = self.path_to_driver
        options = Options()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3163.100 Safari/537.36')
        base_driver = selenium.webdriver.Chrome(driver_path, options=options)
        return base_driver

    def run(self, query=None):

        self.driver.get(self.search_url)

        # If we were passed a query, type it in and execute it.
        if query:
            search_input = self.driver.find_element_by_name('q')
            search_input.send_keys(query)
            search_input.send_keys(u'\ue007') # Enter

        # Wait til the user navigates to a search url.
        WebDriverWait(self.driver, 2**30).until(url_matches(r'((https://)?www.)?google.com/search(.*)'))

        # Inject our javascript controls on to the search page.
        self.inject_javascript()

        # Wait for the transfer element to be added to the DOM.
        trigger_el_exists = EC.presence_of_element_located((By.ID, self.trigger_el_id))
        WebDriverWait(self.driver, 2**30).until(trigger_el_exists)

        # At this point, the trigger has been added by the Analyze button, so we can start to get to work.
        self.parse_serp()

        # End the browser - we're done!
        self.driver.quit()

    def parse_serp(self):

        source = self.driver.page_source
        soup = bsoup(source, 'lxml')

        # The focus kw is in the search bar!
        search_bar = soup.select_one('input[name=q]')
        self.focus_kw = search_bar.get('value')

        # Grab our bold words (aka variants)
        bold = soup.select('#res .rc b, #res .rc strong, #res .rc em')
        self.variant_kws = list(set([x.text for x in bold]))
        self.variant_kws.sort(key=lambda x: len(x.split()), reverse=True)

        # The trigger element holds the JSON representation of the selected links.
        trigger_element = soup.select_one('#' + self.trigger_el_id)
        json_links = json.loads(trigger_element.text)
        self.pages = json_links

        # Close the driver, we're done.
        self.driver.quit()

    def inject_javascript(self):

        # If we're on a google page, inject our controls.
        host = urllib.parse.urlparse(self.driver.current_url).hostname
        if 'google' in host:
            with open(self.js_location, 'r') as js_file:
                js_contents = js_file.read()
                self.driver.execute_script(js_contents)

    def get_pages(self):
        return self.pages

    def get_focus_kw(self):
        return self.focus_kw

    def get_variant_kws(self):
        return self.variant_kws
