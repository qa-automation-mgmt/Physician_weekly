from pages.Google_Adds_pages import GoogleAddPages

class TestGoogleAddPages:
    def test_google_add_in_pages(self, page):
        speciality = GoogleAddPages(page)
        speciality.verify_all_pages()
