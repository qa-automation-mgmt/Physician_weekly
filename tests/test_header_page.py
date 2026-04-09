import pytest
from pages.Header_page import HeaderPage
from playwright.sync_api import expect
from urls import URLs 

class TestHeaderPage:
   def test_logo_redirect_to_homepage(self, page):
      home = HeaderPage(page)
      home.validate_logo_redirect_home()
   def test_specialties_status_and_navigation(self,page):
      home = HeaderPage(page)
      home.validate_specialties_links_status()

   def test_specialties_menu_redirection(self,page):
      from urls import URLs   #URLs.specialties dictionary is imported
      home = HeaderPage(page)
      home.validate_specialties_menu_redirection(URLs)

   def test_header_commentary_menu_redirection(self,page):
      from urls import URLs   #URLs.specialties dictionary is imported
      home = HeaderPage(page)
      home.validate_commentary_menu_redirection(URLs)

   def test_header_option_navigation_and_header_validation(self,page):
      home = HeaderPage(page)
      home.validate_header_navigation_and_header()

   def test_contribute_PV_and_subscription_navigations_another_tab(self,page):
      home = HeaderPage(page)
      home.validate_contribute_and_subscription_tabs()

   def test_header_search_functionality_valid_data(self,page):
      home = HeaderPage(page)
      home.validate_header_search_functionality(keyword="psycology")

   def test_header_search_functionality_invalid_data(self,page):
      home = HeaderPage(page)
      home.validate_header_search_invalid_or_empty_data()
