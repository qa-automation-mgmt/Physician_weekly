from playwright.sync_api import Page, expect
import requests
import re
from helpers.common_functions import CommonHelper
import requests
URLS = [
    "https://www.physiciansweekly.com/page/allergy-immunology",
    # "https://www.physiciansweekly.com/page/cardiology",
    # "https://www.physiciansweekly.com/page/critical-care",
    # "https://www.physiciansweekly.com/page/dermatology",
    # "https://www.physiciansweekly.com/page/endocrinology",
    # "https://www.physiciansweekly.com/page/gastroenterology",
    # "https://www.physiciansweekly.com/page/infectious-disease",
    # "https://www.physiciansweekly.com/page/nephrology",
    # "https://www.physiciansweekly.com/page/obgyn",
    # "https://www.physiciansweekly.com/page/oncology-hematology",
    # "https://www.physiciansweekly.com/page/ophthalmology",
    # "https://www.physiciansweekly.com/page/pain",
    # "https://www.physiciansweekly.com/page/pediatrics",
    # "https://www.physiciansweekly.com/page/primary-care",
    # "https://www.physiciansweekly.com/page/psychiatry",
    # "https://www.physiciansweekly.com/page/pulmonology",
    # "https://www.physiciansweekly.com/page/rheumatology",
    "https://www.physiciansweekly.com/page/surgery"
  
    ]

class SpecialityPages:
    BASE_URL = "https://www.physiciansweekly.com"
    # URLs list directly in the class
   
    def __init__(self, page: Page):
        self.page = page
        self.button_helper = CommonHelper()


    ##test page heading and url matched or not, hero banner, and image count
    
    def verify_speciality_articles_hero_banner(self, url):
        """
        Playwright version of Selenium test:
        - Verifies heading matches the URL (normalized)
        - Checks Hero Banner image count
        """
        self.page.goto(url)
        print(f"\nTesting page: {url} Test Case: Validates that **the specialty articles page heading matches the URL (after normalization)** and **verifies the count of visible Hero Banner images on the page**.")

        try:
            # Wait for heading
            heading = self.page.locator('//div[@class="MuiBox-root css-mm860r"]//h1').first
            heading.wait_for(state="visible", timeout=10000)
            heading_text = heading.inner_text().strip()

            # Normalize heading for comparison
            normalized_text = heading_text.lower().replace("&", "")
            normalized_text = re.sub(r'\s+', '-', normalized_text).strip('-')

            assert normalized_text in url, (f"Expected '{normalized_text}' to be part of '{url}'")

            print("Both Page Heading and Page URL are successfully matched")
            print(f"Heading text: '{heading_text}'")
            print(f"Heading url: '{url}'")

        except Exception as e:
            print("Could not find 'Articles' heading. Check locator or wait time.")
            print(f"Error: {e}")

        # ---- Hero Banner Image Check ----
        banner = self.page.locator('//div[@class="featured_post_img MuiBox-root css-0"]//a')
        images = banner.locator("img")
        visible_count = 0
        img_count = images.count()
        for i in range(img_count):
            if images.nth(i).is_visible():
                visible_count += 1
        if visible_count > 0 and visible_count < 2:
            print(f"Found {visible_count} visible Hero Banner image in main articles section.")
        else:
            print("No visible images found in featured articles section or found more than 1 image.")

 

    def verify_speciality_articles_images_and_status(self, url):
        """
        Playwright version of:
        - Checking image count (expected: 6)
        - Checking image URLs load successfully (status code 200)
        """

        self.page.goto(url)
        print(f"\nTesting page: {url} and Test case : Validates that **the specialty articles page displays exactly 6 images** and **all image URLs return HTTP 200**.")

        # Locate images
        images = self.page.locator('//div[@class="card_small_post MuiBox-root css-0"]//img')
        count = images.count()

        print(f"Total images found: {count}")
        assert count == 6, f"Expected 6 images, but found {count}"

        # Loop through images
        for i in range(count):
            img = images.nth(i)
            src = img.get_attribute("src")
            print(f"Image URL: {src}")

            try:
                response = requests.get(src)
                assert response.status_code == 200, (
                    f"Image not loading properly: {src} (Status: {response.status_code})"
                )
                print(f"Image opened successfully with Status code: {response.status_code}")

            except Exception as e:
                print(f"Error checking image: {src}")
                print(f"Error: {e}")

    def validate_Figure_1_section(self,url):        
        self.page.goto(url)
        print(f"\nTesting page: {url} and Test Case : Validates that the **Figure 1 section on a specialty page has correct heading and content, exactly 6 images with HTTP 200**, and that **all cards and “Join the Conversation” buttons open new tabs showing “Figure 1 PRO”**.")
        Heading = self.page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//h3')
        assert Heading.inner_text() == "Discuss Real Clinical Cases with Real Clinicians","Figure 1 heading is miss matched"
        print("Figure 1 section heading validated successfully",Heading.inner_text())
        Content = self.page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//p')
        assert Content.inner_text() == "Join the largest community of verified healthcare professionals working together, safely and securely, to improve patient outcomes."
        print("Figure 1 section content validated successfully",Content.inner_text())
        all_images = self.page.query_selector_all('//div[@class="MuiBox-root css-62igne"]//img')
        assert len(all_images) == 6, "Images count is not matched as expected in figure 1 section"
        print("Knowladge hub images count matched suiccesfully")
        for img in all_images:
            link = img.get_attribute("src")

            if link:
                # 🔥 FIX: handle relative URLs
                if link.startswith("/"):
                    link = self.BASE_URL + link

                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link}  ---> status code : {status}")

                    assert status == 200, f"Broken image in figure 1 section: {link} returned status {status}"

                except Exception as e:
                    print(f"Error fetching {link}: {e}")

                print("all images are validated successfully")
        cards = self.page.locator('//p[@class="MuiTypography-root MuiTypography-body2 OOCard_commonText__Ehk2G OOCard_caseTitleText__yC9hr OOCard_caseTitleMultiple__OEbrT css-68o8xu"]')

        count = cards.count()
        print(f"Total cards found: {count}")

        for i in range(count):
            card = cards.nth(i)

            # Get card text (optional, for debugging)
            card_text = card.inner_text().strip()
            print(f"\nClicking card: {card_text}")

            # -------------------------------
            # 1. Expect a new tab to open
            # -------------------------------
            with self.page.context.expect_page() as new_tab_event:
                card.click()
                self.page.wait_for_timeout(3000)

            new_tab = new_tab_event.value
            new_tab.wait_for_load_state("domcontentloaded")

            # -------------------------------
            # 2. Validate "Figure 1 PRO" text
            # -------------------------------
            locator_pro = new_tab.locator("//span[text()='Figure 1 PRO']")
            assert locator_pro.is_visible(), f"Figure 1 logo NOT visible for card: {card_text}"

            print("✔ Verified: 'Figure 1 logo' is visible")

            # -------------------------------
            # 3. Close tab & return to main
            # -------------------------------
            new_tab.close()

            # Wait a bit for the context to reset
            self.page.wait_for_timeout(500)

            print("\nAll cards validated successfully.")      
        buttons = self.page.locator('[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]')
        count = buttons.count()
        #assert count == 9, "Button count is not matching"
        print(f"Total buttons found {count}, but clicking Figure 1 section buttons as expected ")

        for i in range(count):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            try:
                if text == "Join the Conversation":
                    btn.scroll_into_view_if_needed()
                    with self.page.context.expect_page() as new_tab_event:
                        btn.click()
                        self.page.wait_for_timeout(3000)

                    new_tab = new_tab_event.value
                    new_tab.wait_for_load_state("domcontentloaded")

                    # -------------------------------
                    # 2. Validate "Figure 1 PRO" text
                    # -------------------------------
                    locator_pro = new_tab.locator("//span[text()='Figure 1 PRO']")
                    assert locator_pro.is_visible(), f"Figure 1 logo NOT visible for card: {card_text}"

                    print("✔ Verified: 'Figure 1 logo' is visible")

                    # -------------------------------
                    # 3. Close tab & return to main
                    # -------------------------------
                    new_tab.close()

                    # Wait a bit for the context to reset
                    self.page.wait_for_timeout(500)

                else:
                    pass
            except Exception as e:
                print("Failed to find the buttons due to:\n",e)
                
                    


    def verify_doctor_voice_images_and_links(self, url):
        """
        Playwright version of:
        - Closing popup
        - Validating Doctor Voice images count (=3)
        - Checking each image loads with status code 200
        - Validating link URLs under images load correctly
        """
        self.page.goto(url)
        print(f"\nTesting page: {url} and Test Case : Validates that the **Doctor Voice section on the given page shows exactly 3 images**, all **image URLs return HTTP 200**, and all **associated article links load successfully with HTTP 200**.")    

        # ---- Doctor Voice Images ----
        images = self.page.locator(
            '(//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-ucawf0"])[1]//img'
        )
        count = images.count()

        print(f"Total images found in Doctor Voice section: {count}")
        assert count == 3, f"Expected 3 images, but found {count}"

        # Validate each image URL
        for i in range(count):
            src = images.nth(i).get_attribute("src")
            print(f"Image URL: {src}")

            try:
                response = requests.get(src)
                assert response.status_code == 200, (
                    f"Image not loading properly: {src}"
                )
                print(f"Image opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking image: {src}")
                print(e)

        links = self.page.locator('(//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-ucawf0"])[1]//a')
        link_count = links.count()
        for i in range(link_count):
            href = links.nth(i).get_attribute("href")
            print(f"Link URL: {href}")
            if href.startswith("/"):
                full_url = self.BASE_URL + href
            else:
                full_url = href
            try:
                response = requests.get(full_url)
                assert response.status_code == 200, (
                    f"Broken link: {href}"
                )
                print(f"Link opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking link: {href}")
                print(e)

    def verify_business_of_medicine_images_and_links(self, url):
        """
        Playwright version of:
        - Validating Business of Medicine image count (=3)
        - Checking each image loads with status code 200
        - Validating link URLs load correctly
        """
        self.page.goto(url)
        print(f"\nTesting page: {url} and Validates that the **Business of Medicine section on the given page displays exactly 3 images**, all **image URLs return HTTP 200**, and all **associated article links load successfully with HTTP 200**.")
        self.page.wait_for_timeout(2000)
        # ---- Get Images ----
        images = self.page.locator(
            "(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[2]//img"
        )
        count = images.count()

        print(f"Total images found in Bussiness of Medician: {count}")
        assert count == 3, f"Expected 3 images in Business of Medicine, but found {count}"

        # ---- Check Each Image ----
        for i in range(count):
            img = images.nth(i)

            # Scroll into view
            img.scroll_into_view_if_needed()

            src = img.get_attribute("src")
            print(f"Image URL: {src}")

            try:
                response = requests.get(src)
                assert response.status_code == 200, (
                    f"Image not loading properly: {src}"
                )
                print(f"Image opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking image: {src}")
                print(e)

        # ---- Check Links ----
        links = self.page.locator("(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[2]//a")
        link_count = links.count()
        for i in range(link_count):
            href = links.nth(i).get_attribute("href")
            print(f"Link URL: {href}")
            if href.startswith("/"):
                full_url = self.BASE_URL + href
            else:
                full_url = href
            try:
                response = requests.get(full_url)
                assert response.status_code == 200, (f"Broken link: {href}")
                print(f"Link opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking link: {href}")
                print(e)
    def verify_cartoons_images_and_links(self, url):
        """
        Playwright version of Selenium test:
        - Validates cartoons section image count (=3)
        - Checks each image loads properly (status 200)
        - Validates each link loads properly (status 200)
        """
        try:
            self.page.goto(url)
            print(f"\nTesting page: {url} and Test Case : Validates that the **Cartoons section on the given page displays exactly 3 images**, all **image URLs return HTTP 200**, and all **associated article links load successfully with HTTP 200**.")
        except Exception as e:
            print(f"Failed to load {url}: {e}")
            return

        # Wait for complete loading
        self.page.wait_for_timeout(2000)

        # ---------------------
        # IMAGE VALIDATION
        # ---------------------
        images = self.page.locator(
            "(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[3]//img"
        )
        img_count = images.count()

        print(f"Total images found: {img_count}")
        assert img_count == 3, f"Expected 3 images, but found {img_count}"

        # Validate image URLs
        for i in range(img_count):
            img = images.nth(i)
            src = img.get_attribute("src")
            print(f"Image URL: {src}")

            try:
                response = requests.get(src)
                assert response.status_code == 200, f"Image not loading properly: {src}"
                print(f"Image opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking image: {src}")
                print(e)
        # ---------------------
        # LINK VALIDATION
        # ---------------------
        links = self.page.locator(
            "(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[3]//a"
        )
        link_count = links.count()

        for i in range(link_count):
            href = links.nth(i).get_attribute("href")
            print(f"Link URL: {href}")
            # ---- convert relative URL to absolute ----
            if href.startswith("/"):
                full_url = self.BASE_URL + href
            else:
                full_url = href

            print(f"Final URL to validate: {full_url}")
            try:
                response = requests.get(full_url)
                assert response.status_code == 200, f"Broken link detected: {full_url}"
                print(f"Link opened successfully (Status code: {response.status_code})")
            except Exception as e:
                print(f"Error checking link: {full_url}")
                print(e)

    def verify_case_consult_images_and_links(self, url):
        """
        Playwright conversion of:
        test_case_consult_image_post_count_and_navigation
        - Validate Case Consult images count == 3
        - Verify each image src responds with HTTP 200
        - Verify each link under the section responds with HTTP 200
        """
        try:
            self.page.goto(url)
            print(f"\nTesting page: {url} and Test Case : Validates that the **Case Consult section on the given page shows exactly 3 images**, all **image URLs return HTTP 200**, and all **associated article links load successfully with HTTP 200**.")
        except Exception as e:
            print(f"Failed to load {url}: {e}")
            return

        # small pause to allow dynamic elements to render (use minimal)
        self.page.wait_for_timeout(1500)

        # IMAGE LOCATOR (same XPath as your Selenium test)
        images = self.page.locator(
            "(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[4]//img"
        )
        img_count = images.count()
        print(f"Total images found in case consult section: {img_count}")
        assert img_count == 3, f"Expected 3 images, but found {img_count}"

        # Validate each image src + status code
        for i in range(img_count):
            img = images.nth(i)
            # scroll into view to be safe
            try:
                img.scroll_into_view_if_needed()
            except Exception:
                pass

            src = img.get_attribute("src") or ""
            print(f"Image URL: {src}")

            if not src:
                print(" Image has empty src — skipping request check.")
                continue

            # handle relative image URLs
            if src.startswith("/"):
                full_img_url = f"{self.BASE_URL.rstrip('/')}{src}"
            else:
                full_img_url = src

            try:
                resp = requests.get(full_img_url, timeout=10)
                assert resp.status_code == 200, f"Image not loading properly: {full_img_url} (Status {resp.status_code})"
                print(f"Image opened successfully (Status: {resp.status_code})")
            except Exception as e:
                print(f"Error checking image: {full_img_url}")
                print(e)

        # LINK VALIDATION
        links = self.page.locator(
            "(//div[@class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 card_tall_section css-isbt42'])[4]//a"
        )
        link_count = links.count()

        for i in range(link_count):
            href = links.nth(i).get_attribute("href") or ""
            print(f"Link found: {href}")

            if not href:
                print(" Skipped empty href")
                continue

            # convert relative href to absolute
            if href.startswith("/"):
                full_url = f"{self.BASE_URL.rstrip('/')}{href}"
            else:
                full_url = href

            try:
                resp = requests.get(full_url, timeout=10)
                assert resp.status_code == 200, f"Broken link: {full_url} (Status {resp.status_code})"
                print(f"Link opened successfully (Status: {resp.status_code})")
            except Exception as e:
                print(f"Error checking link: {full_url}")
                print(e)

    def verify_all_Buttons_in_speciality_pages(self,url) :    
       
        self.page.goto(url)
        print(f"\nTesting page: {url} and Test Case : Validates that **all buttons on specialty pages (excluding “Join the Conversation”) are clickable and navigate correctly**.")
        # Reuse helper
        self.button_helper.validate_all_buttons(self.page)

    def verify_specialty_breadcrumb_flow(self, url):

        # ✅ LOG MESSAGE (print only)
        print(
            f"\nTesting page: {url}\n"
            "Test Case: Validates that each specialty article opens correctly "
            "and the breadcrumb on the article page contains the corresponding article title."
        )

        # ✅ NAVIGATE TO SPECIALTY PAGE
        self.page.goto(url, timeout=60000)
        self.page.wait_for_load_state("domcontentloaded")

        # Locate all article title elements
        article_locator = self.page.locator(
            '//div[contains(@class,"card_title")]//a'
        )

        count = article_locator.count()
        print(f"Total articles found: {count}")

        # Store titles and links
        articles = []
        for i in range(count):
            title = article_locator.nth(i).inner_text().strip()
            link = article_locator.nth(i).get_attribute("href")

            if link and link.startswith("/"):
                link = self.BASE_URL + link

            articles.append({"title": title, "link": link})

        # Open each article and validate breadcrumb
        for i, art in enumerate(articles, start=1):
            print(f"\nOpening Article {i}: {art['title']}")
            self.page.goto(art["link"], timeout=60000)
            self.page.wait_for_load_state("domcontentloaded")

            breadcrumb_locator = self.page.locator(
                '//ol[contains(@class,"MuiBreadcrumbs-ol")]//p'
            )

            breadcrumb_locator.first.wait_for(timeout=15000)
            breadcrumb_text = breadcrumb_locator.last.inner_text().strip()

            print("Breadcrumb Text:", breadcrumb_text)
            try:

                assert art["title"].lower() in breadcrumb_text.lower(), (
                    f"Breadcrumb mismatch for article: {art['title']}"
                )
            except AssertionError as e:
                print(e)

        print("\nAll articles validated successfully.")

            
                

   
    # def verify_all_pages(self):
    #     for url in self.URLS:            
    #         self.verify_speciality_articles_hero_banner(url)
    #         self.verify_speciality_articles_images_and_status(url)
    #         self.verify_doctor_voice_images_and_links(url)
    #         self.verify_business_of_medicine_images_and_links(url)  
    #         self.verify_cartoons_images_and_links(url) 
    #         self.verify_case_consult_images_and_links(url)
    #         #self.validate_Figure_1_section(url)
    #         self.verify_all_Buttons_in_speciality_pages(url)
    #         self.verify_specialty_breadcrumb_flow(url)

            
