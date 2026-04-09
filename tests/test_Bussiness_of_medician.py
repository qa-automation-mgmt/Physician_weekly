from pages.Bussiness_of_medicain import Bussiness_of_medicaina_Module

class Test_Bussiness_of_medician:

    def test_naviagtion_and_hero_banner(self, page):
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()
        #BN.verify_Hero_banner()   # call your method here
        assert page.url == "https://www.physiciansweekly.com/page/business-of-medicine", \
            "Navigated invalid URL"
    def test_verify_buttons(self, page):
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.check_buttons_count_and_naviagion()
    def test_verify_Relevant_Articles_in_Business_of_Medicine_titles_navigation_header_validation(self,page):
        BN = Bussiness_of_medicaina_Module(page)
        BN.validate_subfeatured_articles_images_and_titles()
        
    def test_validate_main_headings(self, page):
        """
        Test Case:
        Verify all main section headings are present on the page.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.validate_all_main_headings_present()
    def test_validate_career_section(self, page):
        """
        Test Case:
        Verify Career section content, links, and visibility.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.validate_career_section()
    def test_validate_finance_section(self, page):
        """
        Test Case:
        Verify Finance section links, images, navigation, count, and status codes.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.Finance_all_links_images_naviagtion_count_and_statuscode()
    def test_validate_medical_law_section(self, page):
        """
        Test Case:
        Verify Medical Law section content and functionality.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.validate_medical_law_section()

    def test_validate_revenue_section(self, page):
        """
        Test Case:
        Verify Revenue section content, links, and UI elements.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.validate_revenue_section()
    def test_validate_all_buttons_business_module(self, page):
        """
        Test Case:
        Verify all buttons in Business of Medicine module are present and working.
        """
        BN = Bussiness_of_medicaina_Module(page)
        BN.Navigate_to_Bussiness_of_medician()

        BN.validate_all_buttons_in_bussiness_of_medician_module()