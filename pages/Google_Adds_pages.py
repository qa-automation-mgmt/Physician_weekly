from playwright.sync_api import Page, expect
import requests
import re
from helpers.common_functions import CommonHelper

class GoogleAddPages:
    BASE_URL = "https://www.physiciansweekly.com"
    # URLs list directly in the class
    URLS = [
    "https://www.physiciansweekly.com/page/allergy-immunology"
    ]
  
    def __init__(self, page: Page):
        self.page = page
        self.Google_add_helper = CommonHelper()

    def verify_google_adds_in_mentioned_urls(self,url):
        self.page.goto(url)
        self.Google_add_helper.validate_Google_adds(self.page)


    def verify_all_pages(self):
        for url in self.URLS:            
            self.verify_google_adds_in_mentioned_urls(url)    

    

