from pages.Cases_and_Quizzes_page import Cases_and_Quizzes_page


class Test_Cases_and_Quizzes_page:

    def test_navigation_and_title(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_page_title("Cases and Quizzes")

    def test_buttons_count_and_navigation(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.check_buttons_count_and_navigation()

    def test_validate_headings(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_headings()

    def test_validate_buttons(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_buttons()

    def test_validate_images_and_links(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_images_and_links()

    def test_validate_article_titles_navigation(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_article_titles_navigation()
    def test_see_more_cases_and_quizzes(self, page):
        cq = Cases_and_Quizzes_page(page)
        cq.Navigate_to_Cases_and_quizzes()
        cq.validate_See_more_cases_and_more_Quizzes_buttons_functionality()