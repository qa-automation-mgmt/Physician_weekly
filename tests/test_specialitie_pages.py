import pytest
from pages.specialities_pages import SpecialityPages, URLS


class Test_Specilaities_page:

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_hero_banner(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_speciality_articles_hero_banner(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_article_images(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_speciality_articles_images_and_status(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_doctor_voice(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_doctor_voice_images_and_links(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_business_of_medicine(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_business_of_medicine_images_and_links(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_cartoons(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_cartoons_images_and_links(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_buttons(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_all_Buttons_in_speciality_pages(url)

    @pytest.mark.parametrize("url", URLS)
    def test_speciality_breadcrumb(self, page, url):
        speciality = SpecialityPages(page)
        speciality.verify_specialty_breadcrumb_flow(url)
