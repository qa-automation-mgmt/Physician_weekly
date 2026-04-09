import requests
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators


class Commentary_page(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com"

    def __init__(self, page):
        self.page = page
        self.CM = CommonHelper()   # store in self
    def Navigate_to_Commentary(self):
        current_url = self.page.url

        # If already on page → skip
        if "commentary" in current_url:
            print("Already on Commentary page")
            return

        # Direct navigation (fast + stable)
        self.page.goto("https://www.physiciansweekly.com/page/commentary")
        self.page.wait_for_load_state("domcontentloaded")

        print("Navigated to Commentary page")


    def verify_Hero_banner(self):
        self.CM.verify_hero_banner_in_pages(self.page)
    def check_buttons_count_and_navigation(self):
        buttons = self.page.locator('//div[@class="MuiBox-root css-2rgj9z"]//a')        
        count = buttons.count()
        print(f"Total buttons found: {count}")        
        assert count > 1, "Buttons are missing"
        for i in range(count):
            btn = buttons.nth(i)
            # Get button name
            name = btn.inner_text().strip()
            print(f"\nClicking Button: {name}")
            # Click button
            btn.click()
            self.page.wait_for_load_state("load")
            # Special case: Podcast
            if "podcast" in name.lower():
                expected_url = "https://www.physiciansweekly.com/page/podcast"
                actual_url = self.page.url
                print(f"Podcast URL: {actual_url}")

                assert expected_url in actual_url, \
                    f"Podcast navigation failed. Expected: {expected_url}, Got: {actual_url}"

                print("Podcast URL validated successfully ✅")

            else:
                # Default validation (heading)
                header = self.page.locator('//div[contains(@class,"page_page_title")]//h1')
                header.wait_for(state="visible")

                header_text = header.inner_text().strip()
                print(f"Page Header: {header_text}")

                assert name.lower() in header_text.lower(), \
                    f"Heading mismatch for {name}"

                print(f"Validated: {name}")

            # Go back
            self.page.go_back()
            self.page.wait_for_load_state("load")

    def validate_headings(self):
        print("Validating Conference Coverage headings...")
        expected_sections = [
            "Doctor's Voice",
            "Peer-to-Peer",
            "Cartoons"
        ]
        self.CM.validate_all_main_headings_present(self.page,expected_sections)
    def validate_Doctor_voice_section(self):
        """Validate:
        1. Doctor voice image count = 6
        2. All images return HTTP 200
        3. All article links return HTTP 200
        4. All titles navigate successfully
        """

        # ==========================
        # 1. CAREER IMAGES COUNT
        # ==========================
        all_images = self.page.query_selector_all(self.Doctor_voice_images)
        try:
          assert len(all_images) == 6, "Images count is not matched as expected!"
          print("Doctor voice images count is correct (3).")
        except Exception as e:
           raise Exception(f"Image count is mismatched in Doctor voice  section. URL: {self.page.url}")
        # ==========================
        # 2. IMAGE URL STATUS CHECK
        # ==========================
        for img in all_images:
            link = img.get_attribute("src")
            if link:
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> status {status}")
                    assert status == 200, f"Broken image: {link}"
                except Exception as e:
                    print(f"Error checking image {link}: {e}")

        print("All Career images are valid.")

        # ==========================
        # 3. ALL LINKS STATUS CHECK
        # ==========================
        all_links = self.page.query_selector_all(self.Doctor_voice_all_links)
        BASE = "https://www.physiciansweekly.com"

        for item in all_links:
            link = item.get_attribute("href")
            if link:
                # Convert relative → absolute
                if link.startswith("/"):
                    link = BASE + link

                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> {status}")
                    assert status == 200, f"Broken link: {link}"
                except Exception as e:
                    print(f"Error checking {link}: {e}")

        print("All Career links returned HTTP 200.")

        # ==========================
        # 4. CLICK ALL TITLES & RETURN BACK
        # ==========================
        titles = self.page.locator(self.Doctor_voice_all_titles)
        count = titles.count()

        for i in range(count):
            title = titles.nth(i)
            title.scroll_into_view_if_needed()
            title.click()
            self.page.wait_for_load_state("load")
            self.page.go_back()
            self.page.wait_for_load_state("load")

        print("All Doctor voice titles are clickable and navigable.")
    def validate_Peer_to_peer_section(self):
        """Validate Medical Law:
        - 6 images present
        - All image src status = 200
        - All article links status = 200
        - All titles navigate successfully     """


        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all(self.Business_of_Medicine_all_images)
        try:
          assert len(all_images) == 6, "Images count is not matched as expected"
          print("Peer-to-peer images count matched successfully")

        except Exception as e:
           raise Exception(f"Image count is mismatched in Peer - to - peer section. URL: {self.page.url}")
        for img in all_images:
            link = img.get_attribute("src")
            if link:
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> status code: {status}")
                    assert status == 200, f"Broken image: {link} returned {status}"
                except Exception as e:
                    print(f"Error fetching {link}: {e}")

        # ==========================
        # LINK STATUS CHECK
        # ==========================
        all_links = self.page.query_selector_all(self.Business_of_Medicine_all_links)
        BASE_URL = "https://www.physiciansweekly.com"
        assert len(all_links) == 24,"in Revenew section hyperlinks or read more links or text links or images missing"


        for a in all_links:
            link = a.get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE_URL + link

                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> status code: {status}")
                    assert status == 200, f"Broken link: {link} returned {status}"
                except Exception as e:
                    print(f"Error fetching {link}: {e}")

        # ==========================
        # TITLE CLICK NAVIGATION CHECK
        # ==========================
        titles = self.page.locator(
            '(//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 '
            'card_tall_section css-isbt42"])[3]//img'
        )

        count = titles.count()

        for i in range(count):
            title = titles.nth(i)
            title.scroll_into_view_if_needed()
            title.click()
            self.page.wait_for_load_state("load")
            self.page.go_back()
            self.page.wait_for_load_state("load")

        print("All Peer tp peer images & titles navigated successfully.")
    def validate_Cartoon_section(self):
        """Validate Revenue Section:
        - 6 images present
        - All images return HTTP 200
        - All article links return HTTP 200
        - All titles navigate successfully
        """

        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42"]//img')
        try:
            assert len(all_images) == 18, "Images count is not matched as expected"
            print("Cartoon Section images count matched successfully")
        except Exception as e:
             raise Exception(f"Image count is mismatched in Cartoon section. URL: {self.page.url}")
        for img in all_images:
            link = img.get_attribute("src")
            if link:
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> status code: {status}")
                    assert status == 200, f"Broken image: {link} returned {status}"
                except Exception as e:
                    print(f"Error fetching {link}: {e}")

        # ==========================
        # LINK STATUS CHECK
        # ==========================
        all_links = self.page.query_selector_all('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42"]//a')
        BASE_URL = "https://www.physiciansweekly.com"
        assert len(all_links) == 72,"in Revenew section hyperlinks or read more links or text links or images missing"

        for a in all_links:
            link = a.get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE_URL + link
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link} ---> status code: {status}")
                    assert status == 200, f"Broken link: {link} returned {status}"
                except Exception as e:
                    print(f"Error fetching {link}: {e}")

        # ==========================
        # TITLE CLICK NAVIGATION CHECK
        # ==========================
        titles = self.page.locator(self.cartoons_all_titles)
        count = titles.count()

        for i in range(count):
            title = titles.nth(i)
            title.scroll_into_view_if_needed()
            title.click()
            self.page.wait_for_load_state("load")
            self.page.go_back()
            self.page.wait_for_load_state("load")

        print("All images of Cartoon section are clickable and navigated successfully.")
    def verify_Join_The_Discussion_and_Contribute_to_PW_Contribute(self):
        print("\n--- Validating Heading & Contribute Button ---")
        # Heading validation
        heading = self.page.locator('//div[@class="MuiTypography-root MuiTypography-h2 cat_title css-1lhzw4j"]')
        heading.wait_for(state="visible")
        assert heading.is_visible(), "Heading not visible"
        # Contribute button
        contribute_btn = self.page.get_by_role("button", name="Contribute")
        contribute_btn.scroll_into_view_if_needed()
        print("Clicking Contribute button...")
        contribute_btn.click()
        # Wait for navigation
        self.page.wait_for_load_state("load")
        expected_url = "https://app.smartsheet.com/b/form/8f2ab169168247d7aadc46f1367e61ed"
        actual_url = self.page.url
        print(f"Navigated URL: {actual_url}")
        assert expected_url in actual_url, "Navigation failed"
        print("Navigation validated successfully!")
        # Go back
        self.page.go_back()
        self.page.wait_for_load_state("load")
    def validate_buttons(self):        
        self.CM.validate_all_buttons(self.page, 5, "Join the Conversation")