from locators import Home_page_Locators
import requests
import time
import pytest
from playwright.sync_api import expect
from urls import URLs 
from playwright.sync_api import Page, expect
import requests
import re
from helpers.common_functions import CommonHelper


class E2EFlowPage(Home_page_Locators):
    base_url = "https://www.physiciansweekly.com/"   # GLOBAL URL (accessible everywhere)
    def __init__(self, page):
        self.page = page
        self.FromHelper = CommonHelper()

    def search_function(self):
        self.page.goto(self.base_url) 
        self.FromHelper.Verify_logo_helper(self.page)
        self.FromHelper.Search_function_helper(self.page)
        self.FromHelper.validate_author_and_last_updated(self.page)
        self.FromHelper.validate_social_media_buttons(self.page)
        self.FromHelper.verify_hero_banner_for_post_pages_helper(self.page)
        self.FromHelper.Related_post_Function_helper(self.page)
