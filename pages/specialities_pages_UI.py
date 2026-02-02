from playwright.sync_api import Page, expect
import requests
import re
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators
import time

class SpecialityPagesUI(Home_page_Locators):
    # URLs list directly in the class
    URLS = [
        "https://www.physiciansweekly.com/page/allergy-immunology"
    ]
    def __init__(self, page: Page):
        self.page = page
        self.Fromhelper = CommonHelper()
    def verify_UI(self,url):
        self.page.goto(url)
        self.Fromhelper.validate_hero_banner_image_size_and_quality(self.page)
        self.Fromhelper.validate_h2_header_css(self.page)
        self.Fromhelper.validate_cta_buttons_css_ui(self.page)
        self.Fromhelper.validate_subheading_body_and_link_css(self.page)
        self.Fromhelper.validate_all_images_rendering(self.page)       
    
    def verify_all_pages_UI(self):
        for url in self.URLS:
            self.verify_UI(url)