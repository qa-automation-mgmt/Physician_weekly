from playwright.sync_api import Page
from pages.Knowladge_hub_page import KnowledgeHubPage
class TestKnowledgeHub:
    def test_validate_images(self, page):
        kh_page = KnowledgeHubPage()
        kh_page.Validate_all_images_displayed_and_not_broken(page)

    def test_validate_articles(self, page):
        kh_page = KnowledgeHubPage()
        kh_page.Validate_all_articles_navigation_and_heading(page)