from pages.Commentry_page import Commentary_page


class Test_Commentary_page:

    def test_navigation_and_hero_banner(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.verify_Hero_banner()

    def test_buttons_count_and_navigation(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.check_buttons_count_and_navigation()

    def test_validate_headings(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.validate_headings()

    def test_validate_doctor_voice_section(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.validate_Doctor_voice_section()

    def test_validate_peer_to_peer_section(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.validate_Peer_to_peer_section()

    def test_validate_cartoon_section(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.validate_Cartoon_section()

    def test_validate_contribute_button(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.verify_Join_The_Discussion_and_Contribute_to_PW_Contribute()

    def test_validate_buttons(self, page):
        cm = Commentary_page(page)
        cm.Navigate_to_Commentary()
        cm.validate_buttons()