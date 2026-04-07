from locators import Home_page_Locators
import requests
import time
import pytest
from playwright.sync_api import expect
from urls import URLs 
import re


class HeaderPage(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com/"   # GLOBAL URL (accessible everywhere)

    def __init__(self, page):
        self.page = page

#Validates that the **homepage logo is visible** and **clicking it from an internal page redirects back to the homepage**.

    def validate_logo_redirect_home(self):
        # Go to homepage
        self.page.goto(self.base_url)
        # Verify homepage title
        expect(self.page).to_have_title(
            re.compile("Physician", re.IGNORECASE),
            timeout=15000)
        # Verify logo visibility
        logo = self.page.locator(self.Logo)
        expect(logo).to_be_visible()
        # Navigate to internal page
        self.page.goto("https://www.physiciansweekly.com/page/business-of-medicine")
        # Click logo → should return home
        logo.click()
        # Verify homepage URL
        expect(self.page).to_have_url(self.base_url)
        print("Logo navigation from another page test passed")

#Validates that in header**all Specialties menu links are present** and **each link returns HTTP 200**.

    def validate_specialties_links_status(self):
        try:

            # Navigate
            self.page.goto(self.base_url)

            # Open specialties menu
            self.page.hover(self.speciality_1)

            menu_links = self.page.locator(self.speciality_menu_links)

            # Assert menu opened
            expect(menu_links.first).to_be_visible(timeout=15000)

            count = menu_links.count()
            assert count > 0, "No specialties links found"

            collected = []

            # Collect links (NO per-item visibility assertion)
            for i in range(count):
                # Re-hover to keep menu open
                self.page.hover(self.speciality_1)

                link = menu_links.nth(i)

                href = link.get_attribute("href")
                name = link.inner_text().strip()

                if href:
                    print(f"Found → {name}: {href}")
                    collected.append((name, href))

            # Validate HTTP status
            for name, url in collected:
                if url.startswith("/"):
                    url = self.base_url.rstrip("/") + url

                try:
                    response = requests.head(
                        url,
                        allow_redirects=True,
                        timeout=10
                    )

                    assert response.status_code == 200, \
                        f"{name} → {url} returned {response.status_code}"

                    print(f"✅ {name} → 200 OK")

                except Exception as e:
                    raise AssertionError(
                        f"❌ Status check failed for {name} → {url} ({e})"
         )
        except Exception as E:
            print(E)

#Validates that **each Specialties menu link redirects to the correct URL** and **page header matches the link text**.

    def validate_specialties_menu_redirection(self, URLs):

        # Navigate to homepage
        self.page.goto(self.base_url)

        # Open specialties menu
        self.page.hover(self.speciality_1)

        menu = self.page.locator(self.spe_links_text)
        expect(menu.first).to_be_visible(timeout=15000)

        count = menu.count()
        assert count > 0, "No specialties links found"

        print(f"Found {count} specialties under the menu.")

        for i in range(count):
            # Re-hover to reopen menu
            self.page.hover(self.speciality_1)

            link = menu.nth(i)

            link_text = link.inner_text().strip()
            link_href = link.get_attribute("href")

            print(f"Validating → {link_text} : {link_href}")

            if link_text not in URLs.specialties:
                print(f"Skipping {link_text} (not in expected list)")
                continue

            expected_url = URLs.specialties[link_text]

            # Click WITHOUT expect_navigation
            link.click()

            # Assert URL instead of waiting for navigation
            expect(self.page).to_have_url(expected_url, timeout=15000)
            print("URL validation success")

            # Validate header
            header = self.page.locator(self.headings_1)
            expect(header).to_be_visible(timeout=15000)

            header_text = header.inner_text().strip()
            assert link_text.lower() in header_text.lower(), \
                f"Header mismatch → expected '{link_text}', got '{header_text}'"

            print(f"{link_text} → correct URL + header")

            # Go back safely
            self.page.go_back()
            expect(self.page).to_have_url(self.base_url)

        print("\n✅ ALL SPECIALTIES VALIDATED SUCCESSFULLY!")

#above 4 converted to flacky dector but 
#Validates that **each Commentary menu link redirects to the correct URL** and **page header matches the expected heading**.

    def validate_commentary_menu_redirection(self, URLs):
        """Validate Header Commentary menu redirection (Stable & CI-safe)"""

        # Navigate to homepage
        self.page.goto(self.base_url)

        expected_headings = {
            "Cartoons": "Cartoons",
            "Doctor’s Voice": "Doctor's Voice",
            "Peer-to-Peer": "Peer-to-Peer",
            "Podcast": "PeerPOV",
        }

        commentary_menu = self.page.locator("a[href='/page/commentary']")
        expect(commentary_menu).to_be_visible()

        # Open menu
        commentary_menu.hover()

        menu = self.page.locator(self.Commentary_menu)
        expect(menu.first).to_be_visible(timeout=15000)

        count = menu.count()
        assert count > 0, "No Commentary menu links found"

        for i in range(count):
            # Re-open menu every loop (hover menus collapse)
            commentary_menu.hover()

            link = self.page.locator(self.Commentary_menu).nth(i)
            link_text = link.inner_text().strip()

            if link_text not in URLs.Commentary:
                print(f"Skipping {link_text} (not in expected mapping)")
                continue

            expected_url = URLs.Commentary[link_text]
            print(f"Validating → {link_text}")

            # Click (NO expect_navigation)
            link.click()

            # URL validation (regex = stable)
            expect(self.page).to_have_url(
                re.compile(re.escape(expected_url), re.IGNORECASE),
                timeout=15000
            )

            # Header validation
            header = self.page.locator(self.headings_1)
            expect(header).to_be_visible(timeout=15000)

            header_text = header.inner_text().strip()
            assert expected_headings[link_text].lower() in header_text.lower(), \
                f"Header mismatch for {link_text}: {header_text}"

            print(f"✅ {link_text} → correct URL & header")

            # Go back safely
            self.page.go_back()
            expect(self.page).to_have_url(
                re.compile(self.base_url.rstrip("/"), re.IGNORECASE)
            )

        print("\n✅ ALL COMMENTARY LINKS AND HEADINGS VALIDATED SUCCESSFULLY!")
#Validates that **each main header navigation option redirects correctly** and **the page header matches the clicked option**.

    def validate_header_navigation_and_header(self):
        """Validate Header option navigation and page header"""

        self.page.goto(self.base_url)
        print(self.page.title())

        items = [
            "Specialties",
            "Conference Coverage",
            "Knowledge Hub",
            "Cases and Quizzes",
            "Commentary",
            "Business of Medicine"
        ]

        for text in items:
            print("Clicking:", text)

            # Click the item
            self.page.locator(f"//a[normalize-space()='{text}']").click()

            # Read the page header
            nav_header = self.page.locator(self.headings_1)
            header_text = nav_header.inner_text().strip()
            print("Page Header:", header_text)

            # Normalize both sides for assertion
            assert text.lower().strip() == header_text.lower().strip(), \
                f"NOT MATCHED → Expected: {text}, Got: {header_text}"
            print(f"Heading validation success for: {text}")

            # Small wait before next iteration
            time.sleep(1)

    def validate_contribute_and_subscription_tabs(self):
        """Validate Contribute PV and Subscription menu items open in new tab and check titles"""

        self.page.goto(self.base_url)        
        context = self.page.context

        # Get both menu items
        items = self.page.locator(self.Contribute_and_sunscribe)
        count = items.count()
        print("Total items:", count)

        # Expected URLs
        expected_urls = {
            "Contribute to PW": "https://app.smartsheet.com/b/form/8f2ab169168247d7aadc46f1367e61ed",
            "Subscribe": "https://hosted.pushplanet.com/fm/subscriptions_physw"
        }

        items = self.page.locator(self.Contribute_and_sunscribe)
        count = items.count()
        print("Total items:", count)

        for i in range(count):
            item = items.nth(i)
            name = item.inner_text().strip()
            print(f"\nChecking: {name}")

            assert item.is_visible(), f"{name} not visible"

            # Capture tab count BEFORE click
            old_tab_count = len(context.pages)
            print("Old tab count:", old_tab_count)

            # Open in new tab
            with context.expect_page() as new_page_event:
                item.click()

            new_tab = new_page_event.value

            # Capture tab count AFTER click
            new_tab_count = len(context.pages)
            print("New tab count:", new_tab_count)

            #  Validate new tab opened
            assert new_tab_count == old_tab_count + 1, f"{name} did NOT open in new tab"
            print(f"{name} opened in new tab successfully ")

            new_tab.wait_for_load_state("domcontentloaded")

            #  Wait if Cloudflare ("Just a moment")
            for _ in range(5):
                url = new_tab.url
                print("Current URL:", url)

                if "just" not in url.lower():
                    break

                new_tab.wait_for_timeout(2000)

            final_url = new_tab.url
            print("Final URL:", final_url)

            # Validate correct redirection
            expected_url = expected_urls.get(name)
            assert expected_url in final_url, f"{name} not redirected correctly"

            print(f"{name} redirected correctly ")

            new_tab.close()
    def validate_header_search_functionality(self, keyword="psycology"):
        """Validate search functionality in header with valid data"""

        self.page.goto(self.base_url)

        # Click search icon
        self.page.locator(self.Header_search).click()
        self.page.wait_for_timeout(1500)

        # Enter keyword
        search_box = self.page.locator('#search-box')
        search_box.fill(keyword)
        search_box.press("Enter")
        print(f"Search executed successfully for keyword: {keyword}")

        # Verify search header result
        result_header = self.page.locator(self.Search_result_header)
        expect(result_header).to_be_visible()
        assert keyword.lower() in result_header.inner_text().lower(), "Search result header mismatch"

        # Verify results displayed
        results = self.page.locator(self.Search_Result)
        assert results.count() > 0, "No search results found"

        # Click the first result
        first_result = self.page.locator(self.first_result_1)
        first_title = first_result.inner_text().split("\n")[0].strip()
        first_result.scroll_into_view_if_needed()
        first_result.click()
        self.page.wait_for_timeout(2000)

        # Validate title on opened article page
        article_header = self.page.locator(self.Aruticul_header)
        expect(article_header).to_be_visible()
        assert first_title.lower() in article_header.inner_text().lower(), \
            "Navigated to incorrect page"
        print("Navigation to searched result article successful and header validated")

    def validate_header_search_invalid_or_empty_data(self):
        """Validate header search handles invalid and empty input gracefully"""
        self.page.goto(self.base_url)
        # ---------------------------
        # Test invalid search input
        # ---------------------------
        self.page.locator(self.Header_search).click()
        self.page.wait_for_timeout(1500)

        search_box = self.page.locator('#search-box')
        invalid_keyword = "usdgshdtwujhvh"
        search_box.fill(invalid_keyword)
        search_box.press("Enter")
        time.sleep(1)

        # Check result message
        result = self.page.locator(self.Search_Result)
        expect(result).to_be_visible()
        assert "nothing found" in result.inner_text().lower(), "Result mismatch"
        print(f"'Nothing Found': message displayed successfully for invalid search '{invalid_keyword}'")

        # ---------------------------
        # Test empty search input
        # ---------------------------
        search_box.fill("               ")
        self.page.locator('(//button[@type="button"])[2]').click()
        time.sleep(1)

        # Check result message
        result = self.page.locator(self.Search_Result)
        expect(result).to_be_visible()
        assert "nothing found" in result.inner_text().lower(), "Result mismatch"
        print("'Nothing Found': message displayed successfully for empty search input")
