import pytest
from pages.Footer_page import FooterPage
from playwright.sync_api import expect
from urls import URLs 

class TestFooterPage:
    
    def test_footer_about_connect_links_validation_naviagtion_and_count(self,page):
        home = FooterPage(page)
        home.validate_footer_about_connect_links()

    def test_footer_our_network_external_links(self,page):
        home = FooterPage(page)
        home.validate_footer_our_network_external_links()

    def test_footer_copyright_links_opne_newTab_validation_status_code(self,page):
        home = FooterPage(page)
        home.validate_footer_copyright_links()

    def test_social_links_opens_new_tab(self,page):
        home = FooterPage(page)
        home.validate_social_links_new_tab()

    def test_address_and_logo_is_displayed(self,page):
        home = FooterPage(page)
        home.validate_address_and_footer_logos()
 
    def test_hamburger_menu_in_header(self,page):
        home = FooterPage(page)
        home.validate_hamburger_menu()
