from pages.specialities_pages_UI import SpecialityPagesUI

class TestSpecialityPagesUI:
    def test_speciality_pages_UI(self, page):
        speciality = SpecialityPagesUI(page)
        speciality.verify_all_pages_UI()
