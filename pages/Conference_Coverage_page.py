import requests
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators


class Conferece_coverage_page(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com"

    def __init__(self, page):
        self.page = page
        self.CM = CommonHelper()   # store in self
    def Navigate_to_Conference_coverage(self):
        current_url = self.page.url
        # If already on page → skip click
        if "meeting-coverage" in current_url:
            print("Already on Conference Coverage page")
            return
        Conference = self.page.locator("//a[text()='Conference Coverage']")        
        Conference.scroll_into_view_if_needed()
        Conference.click()
        self.page.wait_for_load_state("domcontentloaded")
    def validate_page_title(self, expected_text):
        actual_text = self.page.locator('//div[@class="page_page_title MuiBox-root css-0"]//h1').text_content().strip()        
        assert actual_text == expected_text, f"Expected '{expected_text}', but got '{actual_text}'"
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
            # Get page header
            header = self.page.locator('//div[@class="MuiBox-root css-mm860r"]//h1').first.inner_text().strip()
            print(f"Page Header: {header}")
            assert any(word in header.lower() for word in name.lower().split()), \
                f"Heading mismatch for {name}"
            print(f"Validated: {name}")
            # Go back
            self.page.go_back()
            self.page.wait_for_load_state("load")
    def validate_headings(self):
        print("Validating Conference Coverage headings...")
        expected_sections = [
            "AACE 2025",
            "AASLD: The Liver Meeting",
            "American College of Cardiology (ACC.26)",
            "ADA 2025",
            "ASCO 2025 - SCLC",
            "ASCO 2025 - CLL",
            "ASCO 2025 - ENSCLC",
            "ASCO 2025 - NSCLC",
            "ASH Annual Meeting",
            "CHEST 2025",
            "ESMO 2025",
            "LUGPA 2025",
            "National Lipid Association 2025",
            "Peripheral Nerve Society 2025",
            "San Antonio Breast Cancer Symposium",
            "Society for Urologic Oncology’s Annual Meeting",
            "World Conference on Lung Cancer"
        ]
        self.CM.validate_all_main_headings_present(self.page,expected_sections)
    def validate_buttons(self):        
        self.CM.validate_all_buttons(self.page, 17, "Join the Conversation")
    def validate_images_and_links(self):
        try:
            print("\nStarting Images & Links Validation...\n")

            base_url = self.base_url   # already defined in your page

            # ------------------ IMAGES ------------------
            images = self.page.locator('//div[@class="MuiBox-root css-1mgrf5c"]//img')
            img_count = images.count()

            print(f"Total Images Found: {img_count}")

            # Assertion (your requirement)
            assert img_count > 45, f"Image count is too high: {img_count}"

            img_pass = 0
            img_fail = 0

            for i in range(img_count):
                try:
                    img = images.nth(i)
                    src = img.get_attribute("src")

                    if not src:
                        print(f"\033[91m[FAIL] Image {i+1} has no src\033[0m")
                        img_fail += 1
                        continue

                    # Handle relative URL
                    if src.startswith("/"):
                        src = base_url + src

                    response = requests.get(src, timeout=5)

                    if response.status_code == 200:
                        print(f"[PASS] Image {i+1}")
                        img_pass += 1
                    else:
                        print(f"\033[91m[FAIL] Image {i+1} status: {response.status_code}\033[0m")
                        img_fail += 1

                except Exception as e:
                    print(f"\033[91m[ERROR] Image {i+1}: {e}\033[0m")
                    img_fail += 1

            print(f"\nImages Passed: {img_pass}, Failed: {img_fail}")

            # ------------------ LINKS ------------------
            links = self.page.locator('//div[@class="MuiBox-root css-1mgrf5c"]//a')
            link_count = links.count()

            print(f"\nTotal Links Found: {link_count}")

            link_pass = 0
            link_fail = 0
            failed_links = []   # ✅ store failed links

            for i in range(link_count):
                try:
                    link = links.nth(i)
                    href = link.get_attribute("href")

                    if not href:
                        print(f"\033[91m[FAIL] Link {i+1} has no href\033[0m")
                        failed_links.append(f"Index {i+1} → No href")
                        link_fail += 1
                        continue

                    # Handle relative URL
                    if href.startswith("/"):
                        href = self.base_url + href

                    response = requests.get(href, timeout=5)

                    if response.status_code == 200:
                        print(f"[PASS] Link {i+1}")
                        link_pass += 1
                    else:
                        print(f"\033[91m[FAIL] Link {i+1} | Status: {response.status_code} | URL: {href}\033[0m")
                        failed_links.append(f"{href} → {response.status_code}")
                        link_fail += 1

                except Exception as e:
                    print(f"\033[91m[ERROR] Link {i+1} | URL: {href} | Error: {e}\033[0m")
                    failed_links.append(f"{href} → ERROR: {e}")
                    link_fail += 1

            # 🔥 Summary
            print(f"\nLinks Passed: {link_pass}, Failed: {link_fail}")

            # 🔴 Print all failed links clearly
            if failed_links:
                print("\n\033[91m===== FAILED LINKS LIST =====\033[0m")
                for link in failed_links:
                    print(f"\033[91m{link}\033[0m")

            # Assertion
            assert link_fail == 0, "Some links failed validation"

            # Final Assertions
            assert img_fail == 0, "Some images failed validation"
            assert link_fail == 0, "Some links failed validation"

            print("\nAll Images & Links validated successfully!")

        except Exception as e:
            print(f"\033[91m[CRITICAL ERROR]: {e}\033[0m")
            raise

    def validate_article_titles_navigation(self):
        title_locator = '//div[@class="MuiTypography-root MuiTypography-h6 MuiTypography-gutterBottom card_title text_link_color css-4an0mh"]//a'        
        page_title_locator = '//div[contains(@class,"cont")]//h1'

        self.CM.validate_title_navigation(
            self.page,
            title_locator=title_locator,
            page_title_locator=page_title_locator
        )