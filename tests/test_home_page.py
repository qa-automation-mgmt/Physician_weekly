import pytest
from pages.home_page import HomePage
from helpers.common_functions import ResponsiveHelper


class TestHomePage:

    def test_home_page_validation(self, page):
        home = HomePage(page)
        heading_text, visible_count = home.validate_featured_articles_and_hero_banner()
        print("Featured heading:", heading_text)
        print("Visible Hero Banner images:", visible_count)
        assert heading_text != "", "Featured Articles heading not found"
        assert 0 < visible_count < 2, "Unexpected number of Hero Banner images"

    def test_subfeatured_articles_heading_validation_Navigation_Again_validate_heading(self, page):
        home = HomePage(page)
        home.validate_subfeatured_articles_images_and_titles()

    def test_main_headings(self, page):
        home = HomePage(page)
        home.validate_all_main_headings_present()    

    def test_doctors_voice_section(self, page):
        home = HomePage(page)
        home.validate_doctors_voice_section()    

    def test_Knowladge_hub__all_links_images_naviagtion_count_and_statuscodes(self,page):
        home = HomePage(page)
        home.Knowladge_hub__all_links_images_naviagtion_count_and_statuscode()    

    def test_business_of_medicine(self, page):
        home = HomePage(page)
        home.validate_business_of_medicine_section()
    
    def test_cartoons_section(self, page):
        home = HomePage(page)
        home.validate_cartoons_section()

    def test_all_buttons(self, page):
        home = HomePage(page)
        home.validate_all_buttons()

    def test_podcast_section(self, page):
        home = HomePage(page)
        home.validate_podcast_section()

    def test_load_more_featured_articles(self, page):
        home = HomePage(page)
        home.validate_load_more_featured_articles()

    def test_load_more_doctor_voice(self, page):
        home = HomePage(page)
        home.validate_load_more_doctor_voice()
    
    def test_load_more_business_of_medicine(self, page):
        home = HomePage(page)
        home.validate_load_more_business_of_medicine()

    def test_specialties_allergy_navigation_K_Articules(self, page):
        home = HomePage(page)
        home.validate_specialties_allergy_navigation()

    def test_breadcrumb_functionality(self, page):
        home = HomePage(page)
        home.validate_breadcrumb_functionality()

    def tst_Figure_1_section(self,page):
        home = HomePage(page)
        home.validate_Figure_1_section()
    #MOBILE AND TABLET Responsive test cases
class TstHomePageViewportResponsive:

    def test_homepage_responsive_header(self, page):
        page.goto("https://www.physiciansweekly.com/")

        # DESKTOP
        ResponsiveHelper.set_viewport(page, ResponsiveHelper.DESKTOP)
        ResponsiveHelper.validate_header_desktop(
            page,
            page.locator("//header")
        )

        # MOBILE
        ResponsiveHelper.set_viewport(page, ResponsiveHelper.MOBILE)
        ResponsiveHelper.validate_header_mobile(
            page,
            page.locator("//button[@aria-label='menu']"),
            page.locator("//nav")
        )

        ResponsiveHelper.assert_no_horizontal_scroll(page)


    def test_article_page_responsive_content(self, page):
        page.goto("https://www.physiciansweekly.com/example-article/")

        ResponsiveHelper.set_viewport(page, ResponsiveHelper.MOBILE)

        ResponsiveHelper.validate_article_readability(
            page,
            "//div[contains(@class,'article-body')]"
        )


    def test_specialty_page_responsive_grid(self, page):
        page.goto("https://www.physiciansweekly.com/category/cardiology/")

        ResponsiveHelper.set_viewport(page, ResponsiveHelper.MOBILE)

        ResponsiveHelper.validate_single_column_layout(
            page,
            "//article"
        )

        ResponsiveHelper.assert_no_horizontal_scroll(page)
