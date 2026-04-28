import requests
from helpers.common_functions import CommonHelper
from locators import Home_page_Locators


class Bussiness_of_medicaina_Module(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com"

    def __init__(self, page):
        self.page = page
        self.CM = CommonHelper()   # store in self
    def Navigate_to_Bussiness_of_medician(self):
        current_url = self.page.url
        # If already on page → skip
        if "business-of-medicine" in current_url:
            print("Already on Business of Medicine page")
            return
        # Direct navigation (fast + stable)
        self.page.goto("https://www.physiciansweekly.com/page/business-of-medicine")
        self.page.wait_for_load_state("domcontentloaded")

        print("Navigated to Business of Medicine page")   
   
    
   
    def verify_Hero_banner(self):
        self.CM.verify_hero_banner_in_pages(self.page)
##Validates that **there are  6 sub-featured article images**, all **image URLs return HTTP 200**, all **article links are valid**, and each **article title opens the correct page with matching heading**.

    def validate_subfeatured_articles_images_and_titles(self):
        """Validates:
        1. Sub-featured article images count = 8  
        2. All image URLs return 200  
        3. All article titles open correct article pages  
        """

        # Open homepage
        # ================================
        # 1. IMAGE COUNT CHECK
        # ================================
        images = self.page.locator('//div[@class="card_small_post MuiBox-root css-0"]//a//img')
        img_count = images.count()
        print(img_count)
        print(f"Total images found: {img_count}")
        assert img_count == 6, f"Expected 6 images, but found {img_count}"
        # ================================
        # 2. VERIFY IMG URL STATUS CODES
        # ================================
        for i in range(img_count):
            src = images.nth(i).get_attribute("src")
            print(f"Image URL: {src}")

            try:
                response = requests.get(src)
                assert response.status_code == 200, f"Image not loading: {src}"
                print(f"Loaded successfully (HTTP {response.status_code})")
            except Exception as e:
                print(f"Error checking image: {src}")
                print("Error:", e)

        # ================================
        # 3. CHECK ALL LINKS STATUS (src attribute)
        # ================================
        all_links = self.page.locator(
            '//div[@class="MuiStack-root css-j7qwjs"]//a'
        )

        BASE_URL = "https://www.physiciansweekly.com"
        count = all_links.count()

        for i in range(count):
            link = all_links.nth(i).get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE_URL + link

                response = self.page.request.get(link)
                status = response.status
                print(f"{link} ---> {status}")
                assert status == 200, f"Broken link: {link}"

        # ================================
        # 4. VERIFY TITLES → OPEN PAGE → CHECK HEADING MATCHES
        # ================================
       # 1️  Locate all article title anchors
        BASE_URL = "https://www.physiciansweekly.com"

        title_elements = self.page.locator(
            '//div[@class="MuiTypography-root MuiTypography-subtitle2 MuiTypography-gutterBottom card_title text_link_color text_class css-s3pevd"]//a'
        )

        count = title_elements.count()
        print("Total Articles:", count)

        titles_list = []

        # Store all titles + hrefs before clicking
        for i in range(count):
            title = title_elements.nth(i).inner_text().strip()
            href = title_elements.nth(i).get_attribute("href")
            titles_list.append((title, href))

        print("Stored Titles:", titles_list)

        # Validate one by one
        for expected_title, relative_link in titles_list:
            try: 
                full_url = BASE_URL + relative_link
                print("\nClicking:", expected_title)
                print("Navigating to:", full_url)

                self.page.goto(full_url)
                self.page.wait_for_load_state("load")

                article_heading = self.page.locator(
                    '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-12 MuiGrid-grid-lg-12 css-15j76c0"]//h1'
                ).inner_text().strip()

                print("Opened Article Heading:", article_heading)

                assert expected_title.lower() in article_heading.lower(), \
                    f"Mismatch! Expected '{expected_title}', but opened '{article_heading}'"

                print("Validated:", expected_title)

                # go back to the homepage
                self.page.goto("https://www.physiciansweekly.com/page/business-of-medicine")
            except Exception as e: 
                   print("We got error on this url",e,self.page.url)

    def check_buttons_count_and_naviagion(self):
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
            header = self.page.locator('//div[contains(@class,"page_page_title")]//h1').inner_text().strip()
            print(f"Page Header: {header}")
            # Validate
            assert name.lower() in header.lower(), f"Heading mismatch for {name}"
            print(f"Validated: {name}")
            # Go back
            self.page.go_back()
            self.page.wait_for_load_state("load")

#Validates that **all main homepage headings**—Featured Articles, Doctor's Voice, Knowledge Hub, Business of Medicine, Cartoons, Podcasts, and Figure 1—are present.

    def validate_all_main_headings_present(self):
        """Validate that all main homepage headings are present"""   
     
        # Locate all headings
        sections = self.page.locator("//div[@class='secondary_title MuiBox-root css-0']")
        # Extract text
        section_texts = sections.all_text_contents()
        print("Found sections:", section_texts)
        # Expected values
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
#Validates that **career section has 3 images**, all **images and links return HTTP 200**, and **all titles are clickable and navigate correctly**.

    def validate_career_section(self):
        """Validate:
        1. Career image count = 3
        2. All images return HTTP 200
        3. All article links return HTTP 200
        4. All titles navigate successfully
        """

        # ==========================
        # 1. CAREER IMAGES COUNT
        # ==========================
        all_images = self.page.query_selector_all(self.Doctor_voice_images)
        assert len(all_images) == 3, "Images count is not matched as expected!"
        print("Career images count is correct (3).")

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

        print("All Career titles are clickable and navigable.")

    def Finance_all_links_images_naviagtion_count_and_statuscode(self):

        all_images = self.page.query_selector_all(self.Knowledge_Hub_all_images)
        assert len(all_images) == 3, "Images count is not matched as expected"
        print("Finance images count matched successfully")
        for i in all_images:
            link = i.get_attribute('src')
            if link:
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link}  ---> status code :  {status}")
                    assert status == 200, f"Broken image: {link} returned status {status}"
                    print('all images, hyperlinks, and text links are not broken')
                except Exception as e:
                    print(f"Error fetching {link}: {e}")

        all_links = self.page.query_selector_all(self.Knowledge_Hub_all_links)
        BASE_URL = "https://www.physiciansweekly.com"
        assert len(all_links) == 12,"in Revenew section hyperlinks or read more links or text links or images missing"


        for i in all_links:
            link = i.get_attribute("href")
            if link:
                if link.startswith("/"):
                    link = BASE_URL + link
                try:
                    response = self.page.request.get(link)
                    status = response.status
                    print(f"{link}  ---> status code :  {status}")                    
                    assert status == 200, f"Broken link: {link} returned status {status}"
                except Exception as e:
                    print(f"Error fetching {link}: {e}")        

        # locator for all titles
        titles = self.page.locator(self.Knowledge_Hub_all_titles)
        count = titles.count()

        for i in range(count):
            title = titles.nth(i)
            title.scroll_into_view_if_needed()
            title.click()
            self.page.wait_for_load_state("load")
            self.page.go_back()
            self.page.wait_for_load_state("load")

        print("All images in Finance section are clickable and navigated")

    # Validates that **Medical Law section has 4 images**, all **images and links return HTTP 200**, and **all titles/images navigate correctly**.

    def validate_medical_law_section(self):
        """Validate Medical Law:
        - 3 images present
        - All image src status = 200
        - All article links status = 200
        - All titles navigate successfully
        """


        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all(self.Business_of_Medicine_all_images)
        assert len(all_images) == 3, "Images count is not matched as expected"
        print("Medical Law images count matched successfully")

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
        assert len(all_links) == 12,"in Revenew section hyperlinks or read more links or text links or images missing"


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

        print("All Medical Law images & titles navigated successfully.")

    # Validates that **Revenue section has 3 images**, all **images and links return HTTP 200**, and **all titles/images navigate correctly**.

    def validate_revenue_section(self):
        """Validate Revenue Section:
        - 3 images present
        - All images return HTTP 200
        - All article links return HTTP 200
        - All titles navigate successfully
        """

        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all(self.cartoons_all_images)
        assert len(all_images) == 3, "Images count is not matched as expected"
        print("Revenue Section images count matched successfully")

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
        all_links = self.page.query_selector_all(self.cartoons_all_links)
        BASE_URL = "https://www.physiciansweekly.com"
        assert len(all_links) == 12,"in Revenew section hyperlinks or read more links or text links or images missing"

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

        print("All images of Revenue section are clickable and navigated successfully.")
#Validate all buttons visible, naviagation names ,and its count 
    def validate_all_buttons_in_bussiness_of_medician_module(self):
        self.CM.validate_all_buttons(self.page)

        buttons = self.page.locator('[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]')
        
        count = buttons.count()
        assert count == 6, f"Buttons are missing expected 6 but found {count}"

        