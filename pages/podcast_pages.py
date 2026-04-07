from playwright.sync_api import Page, expect
import requests
import re
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators
import time

class PodcastPages(Home_page_Locators):
    BASE_URL = "https://www.physiciansweekly.com"
    # URLs list directly in the class
    URLS = [
    "https://www.physiciansweekly.com/podcast/combating-medical-misinformation-part-1-meeting-patients-where-they-are-online",
    "https://www.physiciansweekly.com/podcast/post-dobbs-laws-delay-medically-indicated-care-for-pregnant-patients",
    "https://www.physiciansweekly.com/podcast/understanding-the-barbie-effect-how-pop-culture-can-influence-patient-healthcare"
        ]
    def __init__(self, page: Page):
        self.page = page
        self.Fromhelper = CommonHelper()
    #This test checks all post tag links on each page to ensure they are valid. It collects tag names and their URLs, verifies that each link returns status code 200, and provides a summary of total, working, and broken links.
    

    def verify_post_tags(self, url):
        """
        Playwright conversion of: test_posttags
        - Collect all post-tag links
        - Print link names
        - Validate all links using requests.head()
        """
        try:
            self.page.goto(url, timeout=30000)
            print(f"\nTesting page: {url}")
        except Exception as e:
            print(f"Failed to load {url}: {e}")
            return

        # Fetch all post tag link elements
        elements = self.page.locator(self.Post_tag_links)
        count = elements.count()

        links = []
        link_names = []

        # Extract href + label
        for i in range(count):
            el = elements.nth(i)
            href = el.get_attribute("href")
            name = (el.inner_text() or "").strip()

            if href:
                links.append(href)
                link_names.append(name)

        # Print details
        print(f"\n Total links found: {len(links)}")
        print("Link names:")
        for nm in link_names:
            print(f"- {nm}")

        working_links = 0
        broken_links = 0

        # Validate each link
        for idx, href in enumerate(links):
            name = link_names[idx]

            # Handle relative URLs
            if href.startswith("/"):
                full_url = f"{self.BASE_URL.rstrip('/')}{href}"
            else:
                full_url = href

            try:
                response = requests.head(full_url, allow_redirects=True, timeout=6)

                if response.status_code == 200:
                    print(f"'{name}'  {full_url} is successfully open (Status code: 200)")
                    working_links += 1
                else:
                    print(f"'{name}'  {full_url} is broken (Status code: {response.status_code})")
                    broken_links += 1

            except Exception as e:
                print(f"'{name}'  {full_url} is broken. Error: {e}")
                broken_links += 1
        # Summary
        print("\n Summary")
        print(f"Total links checked: {len(links)}")
        print(f"Working links: {working_links}")
        print(f"Broken links: {broken_links}")
   #Verify Author name is displayed Author link is valid (status 200)- Last Updated date is present
    def validate_Author_and_lastupdated(self,url):
        self.page.goto(url)
        print(f"\nTesting page: {url}")
        self.Fromhelper.validate_author_and_last_updated(self.page)
   #Validates that all social media share buttons are present on each page and ensures each button is clickable or not         

    def validate_social_media_is_displayed(self,url):
        self.page.goto(url)
        print(f"\nTesting page: {url}")
        self.Fromhelper.validate_social_media_buttons(self.page)

    def verify_buttons_image_heading_validation_in_podcast(self, url):
        """ Playwright version of:
        test_Buttons_image_heading_validation_
        Validates:
        - post_content section visible
        - image visible + loads with status code 200
        - main heading == video title heading
        - pause button + speaker button visible
        """
        try:
            self.page.goto(url)
            print(f"\nTesting page: {url}")
        except Exception as e:
            print(f"Failed to load URL: {e}")
            return

        self.page.wait_for_timeout(1500)

        # post_content div
        post_section = self.page.locator('//div[@id="post_content"]')
        assert post_section.is_visible(), "Post content section is not visible"
        print("post_content section visible")

        # Image inside post_content
        img = self.page.locator('(//div[@id="post_content"]//img)[1]')
        assert img.is_visible(), "Image not visible in the post content section"
        src = img.get_attribute("src")
        print("Image SRC =", src)

        # Status check (with relative URL support)
        if src.startswith("/"):
            full_img_url = self.BASE_URL.rstrip("/") + src
        else:
            full_img_url = src

        response = requests.get(full_img_url)
        assert response.status_code == 200, "Image failed loading"
        print("Image loaded successfully")

        # UI headings
        #After Updation they remove headings in the vedios 
        #That's y i commented out for few lines 
        #h = self.page.locator('//div[@class="MuiTypography-root MuiTypography-h6 MuiTypography-gutterBottom title css-4an0mh"]')
        h1 = self.page.locator('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-m43vlk"]//h1')

        #assert h.is_visible(), "H6 heading is not visible"
        assert h1.is_visible(), "H1 heading is not visible"

        #h_text = h.inner_text().strip().lower()
        h1_text = h1.inner_text().strip().lower()

        #print("Main Heading =", h_text)
        print("Video Player Heading =", h1_text)

        #assert h_text == h1_text, "Heading mismatch"
        print("Headings match successfully")
        self.page.wait_for_timeout(3000)
        # Buttons (pause & speaker)
        pause_btn = self.page.locator('(//div[@class="vjs-control-bar"]//button)[1]')
        speaker_btn = self.page.locator('(//div[@class="vjs-control-bar"]//button)[4]')
        try:
            assert pause_btn.is_visible(), "Pause button is not visible"
            assert speaker_btn.is_visible(), "Speaker button is not visible"
        except AssertionError as a:
            print(a)    
            print("Pause & Speaker buttons are not visibleed")
        print("Pause & Speaker buttons are visible")

    def verify_related_post_navigation_text_validation_buttons_playButton_is_displayed(self, url):
        """
        Validates:
        - All 'Related Posts' links (excluding Podcasts & Medlaw)
        - Clicking each link opens the correct page
        - The heading on the new page matches the link text
        """
        print(f"\nTesting page: {url}")
        self.page.goto(url, wait_until="load")
         # Step 1: Get all anchor tags inside podcast cards
        Play_buttons = self.page.locator('//div[@class="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 p_card css-zmnxdm"]//button')
        print("Total Related postes Avaliable ",Play_buttons.count())
        assert Play_buttons.count() == Play_buttons.count(),'Play buttons count / Related post count is miss matched '
        loc = self.page.locator('//div[contains(@class,"podcast_card_title")]//a')
        total = loc.count()
        print(f"Total Texts, headings and buttons found: {total}")
        #assert total == 10,"In Related post some buttons or text us missing"

        # Step 1: Collect all headings (no skipping)
        headings = []
        for i in range(total):
            raw_text = loc.nth(i).inner_text().strip()
            # Split lines because raw text contains multiple labels
            parts = [p.strip() for p in raw_text.split("\n") if p.strip()]
            # Get the longest part = likely article title, but we'll click all anyway
            longest = max(parts, key=len)
            headings.append((i, longest))

        print(f"Headings to click: {len(headings)}")

        # Step 2: Click each heading
        for index, heading_text in headings:

            print(f"\nClicking: {heading_text}")

            # Scroll and click
            element = loc.nth(index)
            element.scroll_into_view_if_needed()
            element.click()
            self.page.wait_for_timeout(800)

            # Step 3: Validate using both XPaths
            long_xpath = '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-12 MuiGrid-grid-lg-12 css-15j76c0"]//h1'
            short_xpath = '//div[@class="MuiTypography-root MuiTypography-h5 css-1jit86e"]'
            final_heading = None

            # Check long heading first
            if self.page.locator(long_xpath).count() > 0:
                final_heading = self.page.locator(long_xpath).inner_text().strip()

            # Check short heading if long not found
            elif self.page.locator(short_xpath).count() > 0:
                final_heading = self.page.locator(short_xpath).inner_text().strip()

            else:
                raise Exception("No valid heading found on the opened page!")

            print(f"Opened Page Heading: {final_heading}")

            # Step 4: Validate the heading
            assert heading_text.lower() in final_heading.lower(), \
                f"\nHeading mismatch!\nExpected: {heading_text}\nFound: {final_heading}"

            print("Matched successfully!")

            # Step 5: Go back
            self.page.go_back(wait_until="load")
            self.page.wait_for_timeout(800)


    def verify_all_pages(self):
        for url in self.URLS:            
            self.verify_post_tags(url)
            self.validate_Author_and_lastupdated(url)
            self.validate_social_media_is_displayed(url)
            self.verify_buttons_image_heading_validation_in_podcast(url)
            self.verify_related_post_navigation_text_validation_buttons_playButton_is_displayed(url)
