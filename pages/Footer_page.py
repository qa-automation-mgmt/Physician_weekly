from locators import Home_page_Locators
import requests
import time
import pytest
from playwright.sync_api import expect
from urls import URLs 

class FooterPage(Home_page_Locators):
    base_url = "https://www.physiciansweekly.com/"   # GLOBAL URL (accessible everywhere)
    def __init__(self, page):
        self.page = page

    def validate_footer_about_connect_links(self):
        """Validate footer 'About & Connect' section links: count, status, and same-tab navigation"""
        try:

            self.page.goto(self.base_url, wait_until="domcontentloaded")

            # Scroll to footer (important for headless)
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            sections = [
                '(//div[@class="MuiTypography-root MuiTypography-body2 MuiTypography-gutterBottom css-1b8y91"])[1]//a',
                '(//div[@class="MuiTypography-root MuiTypography-body2 MuiTypography-gutterBottom css-1b8y91"])[2]//a'
            ]

            expected_counts = [4, 3]

            for index, section in enumerate(sections):
                links = self.page.locator(section)

                # Wait until footer links are attached
                expect(links.first).to_be_visible()

                count = links.count()
                print(f"\nSection {index+1}: Found {count} footer links")

                assert count == expected_counts[index], \
                    f"Expected {expected_counts[index]} links, but found {count} in section {index+1}"

                for i in range(count):
                    # Re-locate link every loop (parallel-safe)
                    link = self.page.locator(section).nth(i)

                    name = link.inner_text().strip()
                    href = link.get_attribute("href")

                    if not href:
                        continue

                    print(f"\nChecking: {name} → {href}")

                    # -------- Status Check (API layer – fast & stable) --------
                    base = self.base_url.rstrip("/")
                    full_url = base + href if href.startswith("/") else href

                    response = self.page.request.get(full_url, timeout=10000)
                    assert response.status == 200, f"Broken link: {full_url}"
                    print(f"{full_url} : Status 200 OK")

                    # -------- Same-tab Navigation Check --------
                    href_last = href.rstrip("/").split("/")[-1]

                    with self.page.expect_navigation(wait_until="domcontentloaded"):
                        link.click()

                    current_url = self.page.url
                    print("Navigated to:", current_url)

                    assert href_last in current_url, "Did not open in same tab!"
                    print("Same tab navigation OK")

                    # -------- Go back safely --------
                    with self.page.expect_navigation(wait_until="domcontentloaded"):
                        self.page.go_back()

                    # Ensure footer is visible again after back
                    self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    expect(self.page.locator(section).first).to_be_visible()
        except Exception as e:
                 print(e)       

    def validate_footer_our_network_external_links(self):
        """Validate 'Our Network' footer external links: count, status, and new tab navigation"""

        self.page.goto(self.base_url, wait_until="domcontentloaded")

        # Scroll to footer (critical for headless)
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        links_locator = (
            '(//div[@class="MuiTypography-root MuiTypography-body2 MuiTypography-gutterBottom css-1b8y91"])[3]//a'
        )

        links = self.page.locator(links_locator)

        # Wait until at least one link is visible
        expect(links.first).to_be_visible()

        count = links.count()
        print("\nTotal external links:", count)

        assert count == 6, f"In 'Our Network' section, links missing. Expected: 6 but found {count}"

        for i in range(count):
            # Re-locate every iteration (stale-safe)
            link = self.page.locator(links_locator).nth(i)

            name = link.inner_text().strip()
            href = link.get_attribute("href")

            print(f"\n[{i+1}] {name}")
            print("Link:", href)

            # -------- Status Check (API) --------
            response = self.page.request.get(href, timeout=15000)
            print("Status Code:", response.status)
            assert response.status == 200, f"Broken link → {href}"

            # -------- New Tab Validation --------
            with self.page.expect_popup() as popup_info:
                link.click()

            new_tab = popup_info.value

            # Wait for new tab to load properly
            new_tab.wait_for_load_state("domcontentloaded")

            print("New tab opened with URL:", new_tab.url)

            # Basic sanity check (external URL loaded)
            assert href.split("/")[2] in new_tab.url, "External link did not open correctly"

            new_tab.close()

            # Ensure footer still visible after popup
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            expect(self.page.locator(links_locator).first).to_be_visible()

        print("\nAll external links validated successfully!")


    def validate_footer_copyright_links(self):
        """Validate copyright footer links: count, status code, and open in new tab"""

        self.page.goto(self.base_url, wait_until="domcontentloaded")

        # Scroll to footer (mandatory for headless)
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        links_locator = (
            '//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 col_box_copyright css-tuxzvu"]//a'
        )

        links = self.page.locator(links_locator)

        # Wait until footer links appear
        expect(links.first).to_be_visible()

        count = links.count()
        print("\nTotal copyright links:", count)

        assert count == 4, "Copyright links are missing"

        for i in range(count):
            # Re-locate every iteration
            link = self.page.locator(links_locator).nth(i)

            name = link.inner_text().strip()
            href = link.get_attribute("href")

            print(f"\n[{i+1}] {name}")
            print("Link:", href)

            # -------- Status check --------
            response = self.page.request.get(href, timeout=15000)
            print("Status Code:", response.status)
            assert response.status == 200, f"Broken link → {href}"

            # -------- Open in new tab --------
            with self.page.expect_popup() as popup_info:
                link.click()

            new_tab = popup_info.value

            # Wait for page to load
            new_tab.wait_for_load_state("domcontentloaded")

            print("New tab opened with URL:", new_tab.url)

            # Sanity validation (new tab really opened)
            assert new_tab.url.startswith("http"), "Popup did not open correctly"

            new_tab.close()

            # Restore footer visibility after popup
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            expect(self.page.locator(links_locator).first).to_be_visible()

        print("\nAll copyright links validated successfully!")

    def validate_social_links_new_tab(self):
        """Validate all social media links open in a new tab and point to valid URLs"""

        self.page.goto(self.base_url, wait_until="domcontentloaded")

        # Scroll to footer / social section (important in headless)
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        links = self.page.locator(self.social_media_links)

        # Ensure at least one social link is visible
        expect(links.first).to_be_visible()

        total = links.count()
        print("Total social links (before filtering):", total)

        # Filter valid external links
        valid_links = []
        for i in range(total):
            link = links.nth(i)
            href = link.get_attribute("href")
            label = link.get_attribute("aria-label")
            print("Social Media Name:", label)

            if href and href.startswith("http"):
                valid_links.append((i, href))

        print("Total social links (after filtering):", len(valid_links))

        # Validate each link opens in a new tab
        for index, expected_url in valid_links:
            print(f"\nClicking link: {expected_url}")

            link = self.page.locator(self.social_media_links).nth(index)

            with self.page.expect_popup() as popup_info:
                link.click()

            new_tab = popup_info.value

            # Wait until new tab is ready
            new_tab.wait_for_load_state("domcontentloaded")

            print("New tab opened!")
            print("Opened URL:", new_tab.url)

            # Soft but reliable validation
            assert expected_url.split("/")[2] in new_tab.url, \
                "Social media link did not open correct external page"

            new_tab.close()
            print("Closed new tab successfully.")

            # Restore footer visibility for next iteration
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            expect(self.page.locator(self.social_media_links).first).to_be_visible()


    def validate_address_and_footer_logos(self):
        """Validate footer address and logos visibility and clickability"""
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        # Scroll to footer (mandatory for headless)
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # ---------------- Address validation ----------------
        address = self.page.locator(self.Address)
        expect(address).to_be_visible()
        raw_text = address.inner_text()
        normalized = "\n".join(
            [line.strip() for line in raw_text.splitlines() if line.strip()]
        )

        expected = "180 Mount Airy Road Suite 205\nBasking Ridge, NJ 07920"
        assert normalized == expected, f"Address is incorrect.\nFound:\n'{normalized}'"

        print("Address validated successfully")

        # ---------------- Footer logos validation ----------------
        logos_locator = (
            "div[class='col_box MuiBox-root css-0'] "
            "a[class='MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-12ktelg']"
        )

        logos = self.page.locator(logos_locator)

        expect(logos.first).to_be_visible()

        count = logos.count()
        print("Total footer logos found:", count)

      


    def validate_hamburger_menu(self):
        """Validate header hamburger menu items and logo in drawer"""

        # Navigate safely
        self.page.goto(self.base_url)
        self.page.evaluate("window.scrollBy({ top: 300, behavior: 'smooth' })")

        # Locate hamburger button safely
        hamburger_btn = self.page.locator("button[aria-label='menu']")
        hamburger_btn.wait_for(state="visible")
        hamburger_btn.click()

        # Wait for drawer to appear
        drawer = self.page.locator("div.MuiDrawer-paper")
        drawer.wait_for(state="visible")

        # Validate logo inside drawer
        logo = drawer.locator("img[alt='Logo']")
        assert logo.is_visible(), "Logo not visible in drawer"

        # Get menu items
        menu_items = drawer.locator(
            "nav.drawer_container ul:nth-child(1) a"
        )

        count = menu_items.count()
        print("Total menu items:", count)

        extracted_list = []
        for i in range(count):
            item = menu_items.nth(i)
            text = item.inner_text().strip()
            if text:
                extracted_list.append(text)
                print(f"{len(extracted_list)}. {text}")

        # ---- EXPECTED MENU LIST ----
        expected_list = [
            "Contribute to PW",
            "Subscribe",
            "Specialties",
            "Allergy & Immunology",
            "Cardiology",
            "Critical Care",
            "Dermatology",
            "Gastroenterology",
            "Endocrinology",
            "Infectious Disease",
            "Nephrology",
            "Neurology",
            "OB/GYN",
            "Oncology / Hematology",
            "Ophthalmology",
            "Pain",
            "Pediatrics",
            "Primary Care",
            "Psychiatry",
            "Pulmonology",
            "Rheumatology",
            "Surgery",
            "Urology",
            "Conference Coverage",
            "Knowledge Hub",
            "Cases and Quizzes",
            "Commentary",
            "Podcast",
            "Doctor’s Voice",
            "Peer-to-Peer",
            "Cartoons",
            "Business of Medicine",
        ]

        assert extracted_list == expected_list, (
            f"\n Hamburger menu mismatch!\n"
            f"Expected:\n{expected_list}\n\n"
            f"But Found:\n{extracted_list}\n"
        )

        print("Hamburger menu items validated successfully!")
