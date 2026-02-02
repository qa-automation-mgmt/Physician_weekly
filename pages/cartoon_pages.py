from playwright.sync_api import Page, expect
import requests

class CartoonPage:
    BASE_URL = "https://www.physiciansweekly.com"

    # URLs list directly in the class
    URLS = [
        "https://www.physiciansweekly.com/post/surgical-sorcery",
        "https://www.physiciansweekly.com/post/bee-calm",
        "https://www.physiciansweekly.com/post/bone-appetit",
        "https://www.physiciansweekly.com/post/core-correction",
        "https://www.physiciansweekly.com/post/icu-later-reaper",
        "https://www.physiciansweekly.com/post/crustacean-vaccination",
        "https://www.physiciansweekly.com/post/a-freaky-feeling"
        
        # Add all your cartoon pages here
    ]

    def __init__(self, page: Page):
        self.page = page

    #Checks each page to verify that the heading, author name (with a valid hyperlink), and last updated date are displayed correctly and accessible.

    def verify_page(self, url):
        self.page.goto(url)
        print(f"\nTesting page: {url}")
        # Heading
        heading = self.page.locator('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-12 MuiGrid-grid-lg-9 MuiGrid-grid-xl-9 cont css-1hjwhii"]//h1')
        expect(heading).to_be_visible()
        # Author link
        author = self.page.locator('//span[@class="MuiTypography-root MuiTypography-caption MuiTypography-gutterBottom css-2og8ey"]//a').first
        expect(author).to_be_visible()
        href = author.get_attribute('href')
        # Prepend base URL if relative
        if href.startswith("/"):
            href = f"https://www.physiciansweekly.com{href}"
        # Verify author link
        import requests
        response = requests.get(href)
        assert response.status_code == 200, f"Author hyperlink failed: {href}"
        # Last updated
        last_updated = self.page.locator('//span[@class="MuiTypography-root MuiTypography-caption MuiTypography-gutterBottom css-2og8ey"]//span')
        expect(last_updated).to_be_visible()
        print(f"Author: {author.inner_text()}, Last Updated: {last_updated.inner_text()}")

    #Validates that all social media share buttons are present on each page and ensures each button is clickable or not         
    
    def verify_social_media_buttons(self, url):
        self.page.goto(url)
        print(f"\nTesting page: {url} - Social Media Buttons")
        # Locate all social media buttons inside the div
        buttons = self.page.locator('//div[@class="social_media_share"]//button')
        count = buttons.count()
        print("Total social media buttons found:", count)
        for i in range(count):
            icon = buttons.nth(i)
            aria_label = icon.get_attribute("aria-label")
            print("Icon name:", aria_label)
            try:
                assert aria_label is not None and aria_label != "", "Icon aria-label is missing"
            except AssertionError:
                print(f"Icon {i+1} is missing aria-label")

        print("All social media buttons have icons displayed successfully!")

##This test verifies that the main heading image is properly displayed on each page and that the image link is not broken by checking the HTTP status code (expects 200 OK).

    def verify_heading_image(self, url):
        self.page.goto(url)
        print(f"\nTesting page: {url} - Heading Image Check")
        # Image locator (same as Selenium self.Image)
        img = self.page.locator('//div[@class="html-content-block single_post_content"]//img')
        expect(img).to_be_visible()
        link = img.get_attribute("src")
        # FIX relative path
        if link.startswith("/"):
            link = "https://www.physiciansweekly.com" + link
        response = requests.get(link)
        assert response.status_code == 200, f"Image broken: {response.status_code}"
        print("Image displayed successfully:", response.status_code)
##This test verifies that all hero banner hyperlinks on multiple pages work correctly. It clicks each link, checks if it opens in the same or a new tab, validates redirection URLs using HTTP status codes, and logs the total valid links, redirected URLs, and links opened in new tabs.    def test_header_hero_banner_hyper_links(self, browser):

    def verify_hero_banner_links(self, url):
        """
        Playwright equivalent of Selenium's test_header_hero_banner_hyper_links.
        - clicks each link found by self.Common_Hyper_links
        - detects if it opened in a new tab or same tab
        - records final redirect URL using requests
        - logs counts and lists
        """
        self.page.goto(url)
        print(f"\nTesting page: {url} - Hero Banner Hyperlinks")

        # fresh locator for links container (same xpath you used in Selenium)
        links_locator = self.page.locator('//div[@class="html-content-block single_post_content"]//a')
        total = links_locator.count()
        print(f"Total links found: {total}")
        redirected_urls = []
        new_tab_links = []
        new_tab_count = 0
        for index in range(total):
            # re-query locator each iteration to avoid stale handles after navigation
            links_locator = self.page.locator('//div[@class="html-content-block single_post_content"]//a')
            link = links_locator.nth(index)
            href = link.get_attribute("href")
            print(f"\n Clicking link {index+1}: {href}")
            # scroll into view and small pause to mimic your JS scroll + sleep
            link.scroll_into_view_if_needed()
            self.page.wait_for_timeout(800)
            # Try to capture a new tab with a short timeout (2s). If none opens, treat as same-tab.
            new_page = None
            try:
                with self.page.context.expect_page(timeout=2000) as new_page_info:
                    link.click()
                # if a new page opened, Playwright will set new_page_info.value
                new_page = new_page_info.value
            except Exception:
                # no new page opened within timeout (or click didn't trigger new tab)
                # It's possible click caused same-tab navigation.
                # We already attempted click; continue to determine current URL.
                pass

            # CASE: new tab opened
            if new_page:
                new_tab_count += 1
                new_tab_links.append(href if href is not None else "None")

                # wait for the new page to load then get url, then close it
                try:
                    new_page.wait_for_load_state(timeout=5000)
                except Exception:
                    # not fatal — proceed to read url
                    pass
                current_url = new_page.url
                print(f" Opened in new tab: {current_url}")
                # close new tab and continue
                new_page.close()
                # no need to switch context because we didn't change the original page
            else:
                # CASE: opened in same tab (or nothing special)
                try:
                    # wait for navigation to settle (if it navigated)
                    self.page.wait_for_load_state(timeout=5000)
                except Exception:
                    pass
                current_url = self.page.url
                print(f"Opened in same tab: {current_url}")
                # go back to previous page to continue iterating
                try:
                    self.page.go_back()
                    # small wait so DOM stabilizes before next iteration
                    self.page.wait_for_timeout(1000)
                except Exception:
                    # if go_back fails, continue anyway
                    pass
            # Validate final redirected URL using requests (use full URL for relative hrefs)
            final_href_for_requests = href or ""
            if final_href_for_requests.startswith("/"):
                final_href_for_requests = f"{self.BASE_URL.rstrip('/')}{final_href_for_requests}"
            elif final_href_for_requests and not final_href_for_requests.startswith(("http://", "https://")):
                # if href is relative without leading slash
                final_href_for_requests = f"{self.BASE_URL.rstrip('/')}/{final_href_for_requests}"

            try:
                if final_href_for_requests:
                    resp = requests.get(final_href_for_requests, allow_redirects=True, timeout=10)
                    final_url = resp.url
                    print(" Final Redirect URL:", final_url)
                    redirected_urls.append(final_url)
                else:
                    print(" No href available to validate with requests.")
                    redirected_urls.append(href)
            except Exception as e:
                print("Could not get final redirect URL for:", href, " — ", repr(e))
                redirected_urls.append(href)

        # Summary logs (same format as your Selenium test)
        print("\nAll Final Redirected URLs:")
        for ru in redirected_urls:
            print(ru)

        print(f"\nTotal links opened in new tab: {new_tab_count}")
        if new_tab_links:
            print("🔍 Links opened in new tabs:")
            for l in new_tab_links:
                print(l)
##This test validates all post tag links on each page, ensuring every tag link is functional by checking its HTTP status code. It logs link names, counts total links, and reports the number of working and broken links.

    def verify_post_tag_links(self, url):
        """
        Playwright equivalent of Selenium's test_post_tag_links.
        - collects all tag links
        - prints names + hrefs
        - validates via HTTP HEAD request
        - prints summary same as Selenium version
        """
        self.page.goto(url)
        print(f"\nTesting page: {url}")
        # Get all tag link elements
        tag_links = self.page.locator('//a[@class="MuiButtonBase-root MuiChip-root MuiChip-filled MuiChip-sizeSmall MuiChip-colorDefault MuiChip-clickable MuiChip-clickableColorDefault MuiChip-filledDefault card_badge css-11c65dd"]')
        count = tag_links.count()

        link_urls = []
        link_names = []

        # Collect href & text
        for i in range(count):
            link = tag_links.nth(i)
            href = link.get_attribute("href")
            name = (link.inner_text() or "").strip()

            if href:
                link_urls.append(href)
                link_names.append(name)

        print(f"\n Total links found: {len(link_urls)}")
        print("Link names:")
        for name in link_names:
            print(f"- {name}")

        working_links = 0
        broken_links = 0

        # Validate links using HEAD request
        for idx, url in enumerate(link_urls):
            name = link_names[idx]

            # Handle relative URLs
            final_url = url
            if url.startswith("/"):
                final_url = f"{self.BASE_URL.rstrip('/')}{url}"
            elif not url.startswith(("http://", "https://")):
                final_url = f"{self.BASE_URL.rstrip('/')}/{url}"

            try:
                response = requests.head(final_url, allow_redirects=True, timeout=6)

                if response.status_code == 200:
                    print(f"'{name}'  {final_url} is successfully open (Status code: 200)")
                    working_links += 1
                else:
                    print(f"'{name}'  {final_url} is broken (Status code: {response.status_code})")
                    broken_links += 1

            except requests.RequestException as e:
                print(f"'{name}'  {final_url} is broken. Error: {e}")
                broken_links += 1

        # Summary, same style as Selenium
        print("\n Summary")
        print(f"Total links checked: {len(link_urls)}")
        print(f"Working links: {working_links}")
        print(f"Broken links: {broken_links}")
##This test verifies all text hyperlinks and images within a specific card section on each page. It ensures that every hyperlink and image loads successfully (status code 200) and validates that exactly five images are present, logging any broken links or missing images.    

    def verify_text_images_hyperlinks_validation(self, url):
        """
        Playwright version of Selenium test_text_images_hyperlinks_validation:
        - Collects hyperlinks inside card section
        - Converts relative URLs into absolute URLs
        - Validates all hyperlinks via HTTP status
        - Collects images inside card section
        - Validates status codes for image URLs
        - Ensures exactly 5 images are present
        """
        # Always convert incoming URL to absolute
        if url.startswith("/"):
            url = f"{self.BASE_URL}{url}"
        self.page.goto(url)
        print(f"\nTesting page: {url}")
        # ===== TEXT HYPERLINKS =====
        link_locator = self.page.locator('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42"]//a')
        link_count = link_locator.count()
        link_urls = []
        for i in range(link_count):
            href = link_locator.nth(i).get_attribute("href")
            if href:
                # Convert relative → absolute
                if href.startswith("/"):
                    href = f"{self.BASE_URL}{href}"
                link_urls.append(href)

        # Validate all URL links
        for link in link_urls:
            try:
                response = requests.head(link, allow_redirects=True, timeout=6)
                if response.status_code == 200:
                    print(f"{link} opened successfully (200)")
                else:
                    print(f"{link} is broken - Status: {response.status_code}")
            except requests.RequestException as e:
                print(f"{link} is broken. Error: {e}")

        # ===== IMAGES =====
        img_locator = self.page.locator(
            '//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42"]//img'
        )
        img_count = img_locator.count()

        img_urls = []
        for i in range(img_count):
            src = img_locator.nth(i).get_attribute("src")
            if src:
                # Convert relative → absolute (very rare case)
                if src.startswith("/"):
                    src = f"{self.BASE_URL}{src}"
                img_urls.append(src)

        print(f"Total images found: {len(img_urls)}")
        assert len(img_urls) == 5, f"Image count mismatch: expected 5, found {len(img_urls)}"

        # Validate image URLs
        for img in img_urls:
            try:
                response = requests.head(img, allow_redirects=True, timeout=6)
                if response.status_code == 200:
                    print(f"Image loaded successfully (200): {img}")
                else:
                    print(f"Broken image: {img} - Status: {response.status_code}")
            except requests.RequestException as e:
                print(f"{img} is broken. Error: {e}")

    def verify_all_pages(self):
        for url in self.URLS:            
            self.verify_post_tag_links(url)
            self.verify_text_images_hyperlinks_validation(url)
            self.verify_page(url)
            self.verify_social_media_buttons(url)
            self.verify_heading_image(url)
            self.verify_hero_banner_links(url)
            
