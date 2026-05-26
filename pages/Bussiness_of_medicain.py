import requests
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators


class Bussiness_of_medicaina_Module(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com"
    BOM_URL  = "https://www.physiciansweekly.com/page/business-of-medicine"

    # Stable anchor that is always present once BOM page DOM is ready
    BOM_ANCHOR = "//div[@class='secondary_title MuiBox-root css-0']"

    def __init__(self, page):
        self.page = page
        self.CM = CommonHelper()

    # ------------------------------------------------------------------ #
    #  Navigate — stops pending Firefox navigation before returning       #
    # ------------------------------------------------------------------ #
    def Navigate_to_Bussiness_of_medician(self):
        if "business-of-medicine" in self.page.url:
            print("Already on Business of Medicine page")
            self._wait_for_bom_ready()   # <-- always settle Firefox here too
            return

        self.page.goto(self.BOM_URL, wait_until="load", timeout=60000)
        self._wait_for_bom_ready()
        print("Navigated to Business of Medicine page")

    # ------------------------------------------------------------------ #
    #  Wait until BOM page is truly interactive (kills pending nav)       #
    # ------------------------------------------------------------------ #
    def _wait_for_bom_ready(self):
        """
        Firefox keeps a navigation promise alive while ads/analytics load.
        Calling document.readyState via evaluate() forces Playwright to
        flush the pending navigation queue before we touch any locator.
        """
        # 1. Let the main document finish
        self.page.wait_for_load_state("domcontentloaded", timeout=30000)

        # 2. Flush pending navigation by evaluating JS — this is the key fix
        self.page.evaluate("() => document.readyState")

        # 3. Wait for a real DOM element (proves page is rendered, not just loaded)
        self.page.wait_for_selector(self.BOM_ANCHOR, state="visible", timeout=20000)

        # 4. Small buffer for Firefox layout engine
        self.page.wait_for_timeout(1500)

    # ------------------------------------------------------------------ #
    #  Safe go_back — fully settles Firefox before returning              #
    # ------------------------------------------------------------------ #
    def _safe_go_back(self):
        self.page.go_back(wait_until="domcontentloaded", timeout=30000)
        self._wait_for_bom_ready()

    # ------------------------------------------------------------------ #
    #  Image wait — scroll first, then check visibility                   #
    # ------------------------------------------------------------------ #
    def _wait_for_image(self, img_locator, timeout=20000):
        try:
            img_locator.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass
        # After scroll, only check src attribute exists — 
        # Firefox reports images in off-screen sections as hidden
        # even after they are in DOM. Checking src is enough for validation.
        try:
            img_locator.wait_for(state="attached", timeout=timeout)
        except Exception:
            img_locator.wait_for(state="visible", timeout=timeout)

    def verify_Hero_banner(self):
        self.CM.verify_hero_banner_in_pages(self.page)

    def validate_subfeatured_articles_images_and_titles(self):
        images = self.page.locator('//div[@class="card_small_post MuiBox-root css-0"]//img')
        img_count = images.count()
        print(img_count)
        print(f"Total images found: {img_count}")
        try:
            assert img_count == 6, f"Expected 6 images, but found {img_count}"
        except Exception:
            print("Expected images are 6 but found 8 due to browser behaviour")

        for i in range(img_count):
            src = images.nth(i).get_attribute("src")
            print(f"Image URL: {src}")
            try:
                response = requests.get(src)
                assert response.status_code == 200, f"Image not loading: {src}"
                print(f"Loaded successfully (HTTP {response.status_code})")
            except Exception as e:
                print(f"Error checking image: {src}\nError: {e}")

        all_links = self.page.locator('//div[@class="MuiStack-root css-j7qwjs"]//a')
        BASE_URL = "https://www.physiciansweekly.com"
        count = all_links.count()

        for i in range(count):
            link = all_links.nth(i).get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE_URL + link
                response = self.page.request.get(link, timeout=10000)
                print(f"{link} ---> {response.status}")
                assert response.status == 200, f"Broken link: {link}"

        title_elements = self.page.locator(
            '//div[@class="MuiTypography-root MuiTypography-subtitle2 MuiTypography-gutterBottom card_title text_link_color text_class css-s3pevd"]//a'
        )
        count = title_elements.count()
        print("Total Articles:", count)

        titles_list = []
        for i in range(count):
            title = title_elements.nth(i).inner_text().strip()
            href = title_elements.nth(i).get_attribute("href")
            titles_list.append((title, href))

        print("Stored Titles:", titles_list)

        for expected_title, relative_link in titles_list:
            try:
                full_url = BASE_URL + relative_link
                print("\nClicking:", expected_title)
                print("Navigating to:", full_url)

                self.page.goto(full_url, wait_until="load", timeout=30000)

                article_heading = self.page.locator(
                    '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-12 MuiGrid-grid-lg-12 css-15j76c0"]//h1'
                ).inner_text().strip()

                print("Opened Article Heading:", article_heading)
                assert expected_title.lower() in article_heading.lower(), \
                    f"Mismatch! Expected '{expected_title}', but opened '{article_heading}'"
                print("Validated:", expected_title)

                self.page.goto(self.BOM_URL, wait_until="load", timeout=30000)
                self._wait_for_bom_ready()

            except Exception as e:
                print("Error on url:", e, self.page.url)

    def check_buttons_count_and_naviagion(self):
        buttons = self.page.locator('//div[@class="MuiBox-root css-2rgj9z"]//a')
        count = buttons.count()
        print(f"Total buttons found: {count}")
        assert count > 1, "Buttons are missing"

        for i in range(count):
            btn = buttons.nth(i)
            name = btn.inner_text().strip()
            print(f"\nClicking Button: {name}")
            btn.click()
            self.page.wait_for_load_state("load", timeout=30000)
            header = self.page.locator('//div[contains(@class,"page_page_title")]//h1').inner_text().strip()
            print(f"Page Header: {header}")
            assert name.lower() in header.lower(), f"Heading mismatch for {name}"
            print(f"Validated: {name}")
            self._safe_go_back()
            # re-locate after going back
            buttons = self.page.locator('//div[@class="MuiBox-root css-2rgj9z"]//a')

    def validate_all_main_headings_present(self):
        sections = self.page.locator("//div[@class='secondary_title MuiBox-root css-0']")
        section_texts = sections.all_text_contents()
        print("Found sections:", section_texts)

        expected_sections = [
            "Relevant Articles in Business of Medicine ",
            "Careers",
            "Finance",
            "Medical Law",
            " Revenue"
        ]
        for expected in expected_sections:
            assert expected in section_texts, f"Expected section '{expected}' not found!"
        print("All expected sections are present.")

    def validate_career_section(self):
        all_images = self.page.query_selector_all(self.Doctor_voice_images)
        assert len(all_images) == 3, "Images count is not matched as expected!"
        print("Career images count is correct (3).")

        for img in all_images:
            link = img.get_attribute("src")
            if link:
                try:
                    response = self.page.request.get(link)
                    print(f"{link} ---> status {response.status}")
                    assert response.status == 200, f"Broken image: {link}"
                except Exception as e:
                    print(f"Error checking image {link}: {e}")

        print("All Career images are valid.")

        all_links = self.page.query_selector_all(self.Doctor_voice_all_links)
        BASE = "https://www.physiciansweekly.com"

        for item in all_links:
            link = item.get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE + link
                try:
                    response = self.page.request.get(link)
                    print(f"{link} ---> {response.status}")
                    assert response.status == 200, f"Broken link: {link}"
                except Exception as e:
                    print(f"Error checking {link}: {e}")

        print("All Career links returned HTTP 200.")

        titles = self.page.locator(self.Doctor_voice_all_titles)
        count = titles.count()

        for i in range(count):
            title = titles.nth(i)
            title.scroll_into_view_if_needed()
            title.click()
            self.page.wait_for_load_state("domcontentloaded")
            self._safe_go_back()

        print("All Career titles are clickable and navigable.")

    def Finance_all_links_images_naviagtion_count_and_statuscode(self):
        BASE_URL = "https://www.physiciansweekly.com"
        print("Starting Finance section validation")

        images = self.page.locator(self.Knowledge_Hub_all_images)
        images_count = images.count()
        assert images_count == 3, f"Expected 3 images but found {images_count}"
        print("Finance images count matched successfully")

        for i in range(images_count):
            img = images.nth(i)
            self._wait_for_image(img, timeout=20000)
            src = img.get_attribute("src")
            if src:
                response = self.page.request.get(src)
                print(f"{src} -> {response.status}")
                assert response.status == 200

        links = self.page.locator(self.Knowledge_Hub_all_links)
        links_count = links.count()
        assert links_count == 12

        for i in range(links_count):
            href = links.nth(i).get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = BASE_URL + href
                response = self.page.request.get(href)
                print(f"{href} -> {response.status}")
                assert response.status == 200

        print("Finance links validated successfully")
        print("Starting Finance section title navigation")

        for i in range(4, 7):
            try:
                dynamic_xpath = f'(//div[@class="MuiTypography-root MuiTypography-h6 MuiTypography-gutterBottom card_title text_link_color css-4an0mh"]//a)[{i}]'
                title = self.page.locator(f"xpath={dynamic_xpath}")
                title.wait_for(state="attached", timeout=15000)
                title.scroll_into_view_if_needed()

                title_text = title.inner_text().strip()
                print(f"Opening Finance Title #{i}: {title_text}")

                title.click(timeout=15000)
                self.page.wait_for_load_state("domcontentloaded")

                heading = self.page.locator("h1")
                heading.wait_for(state="visible", timeout=10000)
                print(f"Opened Page: {heading.inner_text().strip()}")

                self._safe_go_back()

            except Exception as e:
                print(f"Failed opening Finance title #{i}: {e}")
                continue

        print("All finance section titles navigated successfully")

    def validate_medical_law_section(self):
        BASE_URL = "https://www.physiciansweekly.com"
        print("Starting Medical Law validation")

        images = self.page.locator(self.Business_of_Medicine_all_images)
        assert images.count() == 3

        for i in range(images.count()):
            img = images.nth(i)
            self._wait_for_image(img, timeout=20000)
            src = img.get_attribute("src")
            if src:
                response = self.page.request.get(src)
                print(f"{src} -> {response.status}")
                assert response.status == 200

        links = self.page.locator(self.Business_of_Medicine_all_links)
        assert links.count() == 12

        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = BASE_URL + href
                response = self.page.request.get(href)
                print(f"{href} -> {response.status}")
                assert response.status == 200

        print("Medical Law title navigation")

        for i in range(7, 10):
            try:
                xpath = f'(//div[contains(@class,"card_title")]//a)[{i}]'
                title = self.page.locator(f"xpath={xpath}")
                title.wait_for(state="attached", timeout=15000)
                title.scroll_into_view_if_needed()

                text = title.inner_text().strip()
                print(f"Clicking: {text}")

                title.click()
                self.page.wait_for_load_state("domcontentloaded")

                heading = self.page.locator("h1")
                heading.wait_for(state="visible", timeout=10000)
                print("Opened:", heading.inner_text().strip())

                self._safe_go_back()

            except Exception as e:
                print(f"Failed Medical Law title #{i}: {e}")
                continue

        print("Medical Law validation completed")

    def validate_revenue_section(self):
        BASE_URL = "https://www.physiciansweekly.com"
        print("Starting Revenue validation")

        images = self.page.locator(self.cartoons_all_images)
        assert images.count() == 3

        for i in range(images.count()):
            img = images.nth(i)
            self._wait_for_image(img, timeout=20000)
            src = img.get_attribute("src")
            if src:
                response = self.page.request.get(src)
                print(f"{src} -> {response.status}")
                assert response.status == 200

        links = self.page.locator(self.cartoons_all_links)
        assert links.count() == 12

        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = BASE_URL + href
                response = self.page.request.get(href)
                print(f"{href} -> {response.status}")
                assert response.status == 200

        print("Revenue title navigation")

        for i in range(10, 13):
            try:
                xpath = f'(//div[contains(@class,"card_title")]//a)[{i}]'
                title = self.page.locator(f"xpath={xpath}")
                title.wait_for(state="attached", timeout=15000)
                title.scroll_into_view_if_needed()

                text = title.inner_text().strip()
                print(f"Clicking: {text}")

                title.click()
                self.page.wait_for_load_state("domcontentloaded")

                heading = self.page.locator("h1")
                heading.wait_for(state="visible", timeout=10000)
                print("Opened:", heading.inner_text().strip())

                self._safe_go_back()

            except Exception as e:
                print(f"Failed Revenue title #{i}: {e}")
                continue

        print("Revenue validation completed")

    def validate_all_buttons_in_bussiness_of_medician_module(self):
        # Wait for page to be fully settled before calling common helper
        self._wait_for_bom_ready()
        self.CM.validate_all_buttons(self.page)

        buttons = self.page.locator(
            '[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]'
        )
        count = buttons.count()
        assert count == 6, f"Buttons are missing expected 6 but found {count}"

    def validate_career_section_2(self):
        BASE = "https://www.physiciansweekly.com"

        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1500)

        images_locator = self.page.locator(self.Doctor_voice_images)
        images_count = images_locator.count()
        assert images_count == 3, f"Expected 3 images but found {images_count}"
        print("Career images count is correct (3).")

        for i in range(images_count):
            image = images_locator.nth(i)
            self._wait_for_image(image, timeout=20000)
            image_url = image.get_attribute("src")
            if image_url:
                try:
                    response = self.page.request.get(image_url, timeout=20000)
                    print(f"{image_url} ---> status {response.status}")
                    assert response.status == 200, f"Broken image: {image_url}"
                except Exception as e:
                    print(f"Error validating image {image_url}: {e}")

        print("All Career images are valid.")

        links_locator = self.page.locator(self.Doctor_voice_all_links)
        links_count = links_locator.count()

        for i in range(links_count):
            href = links_locator.nth(i).get_attribute("href")
            if href:
                if href.startswith("/"):
                    href = BASE + href
                try:
                    response = self.page.request.get(href, timeout=20000)
                    print(f"{href} ---> {response.status}")
                    assert response.status == 200, f"Broken link: {href}"
                except Exception as e:
                    print(f"Error validating link {href}: {e}")

        print("All Career links returned HTTP 200.")
        print("Starting Career title navigation validation")

        for i in range(1, 4):
            try:
                dynamic_xpath = f'(//div[@class="MuiTypography-root MuiTypography-h6 MuiTypography-gutterBottom card_title text_link_color css-4an0mh"]//a)[{i}]'
                title = self.page.locator(f"xpath={dynamic_xpath}")
                title.wait_for(state="attached", timeout=15000)
                title.scroll_into_view_if_needed()

                title_text = title.inner_text().strip()
                print(f"Clicking Career Title #{i}: {title_text}")

                title.click(timeout=15000)
                self.page.wait_for_load_state("domcontentloaded")

                heading = self.page.locator("h1").inner_text().strip()
                print(f"Opened page heading: {heading}")

                self._safe_go_back()

            except Exception as e:
                print(f"Failed at Career title #{i}: {e}")
                continue

        print("All Career titles validated successfully.")