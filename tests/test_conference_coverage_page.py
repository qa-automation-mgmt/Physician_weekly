from pages.Conference_Coverage_page import Conferece_coverage_page


class Test_Conference_coverage_page:

    def test_conference_coverage_navigation_and_title(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.validate_page_title("Conference Coverage")

    def test_buttons_counts_navigation(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.check_buttons_count_and_navigation()

    def test_conference_coverage_headings(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.validate_headings()

    def test_verify_all_buttons(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.validate_buttons()

    def test_images_and_links(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.validate_images_and_links()

    def test_article_title_navigation(self, page):
        cc = Conferece_coverage_page(page)
        cc.Navigate_to_Conference_coverage()
        cc.validate_article_titles_navigation()