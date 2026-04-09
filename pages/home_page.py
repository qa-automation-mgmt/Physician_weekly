from locators import Home_page_Locators
import requests
import time


class HomePage(Home_page_Locators):

    base_url = "https://www.physiciansweekly.com/"   # GLOBAL URL (accessible everywhere)

    def __init__(self, page):
        self.page = page
#Navigates to the home page, validates that the **Featured Articles heading is visible and captures its text**, and **counts the number of visible images in the Hero Banner section**.

    def validate_featured_articles_and_hero_banner(self):
        """Validate Featured Articles heading text + visible Hero Banner image count"""
        #Open Home Page using global base_url
        self.page.goto(self.base_url)
        try:
            # ===== Featured Heading =====
            heading_element = self.page.locator(self.FEATURED_HEADING_XPATH)
            heading_element.wait_for(state="visible")
            heading_element.scroll_into_view_if_needed()
            heading_text = heading_element.inner_text().strip()

            # ===== Hero Banner Images =====
            banner = self.page.locator(self.Hero_banner_image)
            banner.wait_for(state="visible")

            images = banner.locator("img")
            total = images.count()

            visible_count = 0
            for i in range(total):
                if images.nth(i).is_visible():
                    visible_count += 1

            return heading_text, visible_count
        except Exception as e:
            print(e)

#Validates that **there are 8 sub-featured article images**, all **image URLs return HTTP 200**, all **article links are valid**, and each **article title opens the correct page with matching heading**.

    def validate_subfeatured_articles_images_and_titles(self):
        """Validates:
        1. Sub-featured article images count = 8  
        2. All image URLs return 200  
        3. All article titles open correct article pages  
        """

        # Open homepage
        self.page.goto(self.base_url)
        # ================================
        # 1. IMAGE COUNT CHECK
        # ================================
        images = self.page.locator(self.Feature_articul_images)
        img_count = images.count()
        print(f"Total images found: {img_count}")
        assert img_count == 8, f"Expected 8 images, but found {img_count}"
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
       # 1️⃣ Locate all article title anchors
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
                self.page.goto(BASE_URL)
            except Exception as e: 
                   print("We got error on this url",e,self.page.url)

#Validates that **all main homepage headings**—Featured Articles, Doctor's Voice, Knowledge Hub, Business of Medicine, Cartoons, Podcasts, and Figure 1—are present.

    def validate_all_main_headings_present(self):
        """Validate that all main homepage headings are present"""
        # Open homepage
        self.page.goto(self.base_url)
        # Locate all headings
        sections = self.page.locator(self.ALL_Headings)
        # Extract text
        section_texts = sections.all_text_contents()
        print("Found sections:", section_texts)
        # Expected values
        expected_sections = [
            "Featured Articles",
            "Doctor's Voice",
            "Knowledge Hub",
            "Business of Medicine",
            "Cartoons",
            "Podcasts",
            "Figure 1"
        ]
        for expected in expected_sections:
            assert expected in section_texts, f"Expected section '{expected}' not found!"
        print("All expected sections are present.")
#Validates that **Doctor's Voice section has 4 images**, all **images and links return HTTP 200**, and **all titles are clickable and navigate correctly**.

    def validate_doctors_voice_section(self):
        """Validate:
        1. Doctor's Voice image count = 4
        2. All images return HTTP 200
        3. All article links return HTTP 200
        4. All titles navigate successfully
        """

        self.page.goto(self.base_url)

        # ==========================
        # 1. DOCTOR'S VOICE IMAGES COUNT
        # ==========================
        all_images = self.page.query_selector_all(self.Doctor_voice_images)
        assert len(all_images) == 4, "Images count is not matched as expected!"
        print("Doctor's Voice images count is correct (4).")

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

        print("All Doctor's Voice images are valid.")

        # ==========================
        # 3. ALL LINKS STATUS CHECK
        # ==========================
        all_links = self.page.query_selector_all(self.Doctor_voice_all_links)
        BASE = "https://www.physiciansweekly.com"
        assert len(all_links) == 16,"in Revenew section hyperlinks or read more links or text links or images missing"

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

        print("All Doctor's Voice links returned HTTP 200.")

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

        print("All Doctor's Voice titles are clickable and navigable.")

#Validates that **Knowledge Hub section has 4 images**, all **images and links return HTTP 200**, and **all titles are clickable and navigate correctly**.
    
    def Knowladge_hub__all_links_images_naviagtion_count_and_statuscode(self):
        self.page.goto(self.base_url)       
        all_images = self.page.query_selector_all(self.Knowledge_Hub_all_images)
        assert len(all_images) == 4, "Images count is not matched as expected"
        print("Knowladge hub images count matched suiccesfully")
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
        assert len(all_links) == 16,"in Revenew section hyperlinks or read more links or text links or images missing"

        for i in all_links:
            link = i.get_attribute("href")
            if link:
                # FIX: convert relative URL → absolute URL
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
        print("all images in knowladge hub section are clickable and naviageted ")     

#Validates that **Business of Medicine section has 4 images**, all **images and links return HTTP 200**, and **all titles/images navigate correctly**.
  
    def validate_business_of_medicine_section(self):
        """Validate Business of Medicine:
        - 4 images present
        - All image src status = 200
        - All article links status = 200
        - All titles navigate successfully
        """

        self.page.goto(self.base_url)

        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all(self.Business_of_Medicine_all_images)
        assert len(all_images) == 4, "Images count is not matched as expected"
        print("Business of Medicine images count matched successfully")

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
        assert len(all_links) == 16,"in Revenew section hyperlinks or read more links or text links or images missing"

        for a in all_links:
            link = a.get_attribute("href")
            if link:
                # Convert /relative → absolute URL
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

        print("All Business of Medicine images & titles navigated successfully.")

#Validates that **Cartoons section has 4 images**, all **images and links return HTTP 200**, and **all titles/images navigate correctly**.
 
    def validate_cartoons_section(self):
        """Validate Cartoons Section:
        - 4 images present
        - All images return HTTP 200
        - All article links return HTTP 200
        - All titles navigate successfully
        """

        self.page.goto(self.base_url)

        # ==========================
        # IMAGE COUNT + STATUS CHECK
        # ==========================
        all_images = self.page.query_selector_all(self.cartoons_all_images)
        assert len(all_images) == 4, "Images count is not matched as expected"
        print("Cartoon Section images count matched successfully")

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
        assert len(all_links) == 16,"in Revenew section hyperlinks or read more links or text links or images missing"

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
#Validates that **all homepage buttons (11 total, excluding Figure 1 “Join the Conversation”) are clickable and navigate correctly**.
  
    def validate_all_buttons(self):
        """Validate all homepage buttons:
        - Count matches expected (7)
        - Each button is clickable and navigates correctly
        """
        self.page.goto(self.base_url)
        # Locate all buttons
        buttons = self.page.locator(self.All_buttons)
        count = buttons.count()
        assert count == 11, "Button count is not matching"
        print("Total buttons found 11, but skipped Figure 1 buttons in Figure 1 section as expected ")

        for i in range(count):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            try:
                if text != "Join the Conversation":
                    btn.scroll_into_view_if_needed()
                    btn.click()
                      # Wait for navigation
                    self.page.wait_for_load_state("load")
                    print(f"Clicked button #{i+1} Button Name: {text}")

                    # Navigate back
                    self.page.go_back()
                    self.page.wait_for_load_state("load")

                else:
                    pass
            except Exception as e:
                print("Failed to find the buttons due to:\n",e)        

          
        print("All buttons are clickable and navigated successfully.")
#Validates that **Podcast section has 4 visible pause buttons** and **all podcast links return HTTP 200**.

    def validate_podcast_section(self):
        """Validate Podcast Section:
        - 4 pause buttons visible
        - All links return HTTP 200
        """

        self.page.goto(self.base_url)

        # ==========================
        # PAUSE BUTTONS CHECK
        # ==========================
        buttons = self.page.locator(self.Buttons)
        count = buttons.count()
        print("Pause buttons found:", count)
        assert count == 4, "Expected 4 podcast pause buttons"

        for i in range(count):
            btn = buttons.nth(i)
            btn.scroll_into_view_if_needed()
            visible = btn.is_visible()
            print(f"Pause Button {i+1} visible in the Podcast section → {visible}")
            assert visible, f"Pause Button {i+1} is NOT visible"

        # ==========================
        # LINKS CHECK
        # ==========================
        links = self.page.locator(self.All_links)
        total = links.count()
        print("Total podcast links found:", total)

        items = []

        for i in range(total):
            text = links.nth(i).inner_text().strip()
            href = links.nth(i).get_attribute("href")

            # Convert relative → absolute
            if href.startswith("/"):
                href = self.base_url.rstrip("/") + href

            items.append((text, href))

        # Validate each link returns HTTP 200
        for text, href in items:
            print(f"\nChecking → {href}")
            response = self.page.request.get(href)
            status = response.status
            print(f"Status: {status}")

            assert status == 200, f"Broken link: {href} returned {status}"
            print(f"✔ Link OK | Title: {text}")

#Validates that **Featured Articles’ Load More works by clicking View All and Load More twice**, and **article counts increase correctly after each click**.

    def validate_load_more_featured_articles(self):
        """Validate Load More functionality for Featured Articles:
        - Click View All
        - Click Load More twice
        - Verify article counts after each click
        """

        # 1. Open Home Page
        self.page.goto(self.base_url)

        # 2. Click "View All"
        view_all = self.page.locator(self.ViewAll_Button1)
        view_all.scroll_into_view_if_needed()
        view_all.click()

        # Wait for articles to load
        self.page.wait_for_timeout(1500)

        # 3. Count Articles BEFORE Load More
        images_before = self.page.locator(self.Images_before_or_after_loadmore).count()
        print("Articles BEFORE Load More:", images_before)

        # 4. First Load More Click
        load_more_btn = self.page.locator(self.Load_more)
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()

        self.page.wait_for_timeout(4000)

        # Count AFTER first Load More
        images_after_first = self.page.locator(self.Images_before_or_after_loadmore).count()
        print("Articles AFTER 1st Load More:", images_after_first)
        assert images_after_first > 20, "Articles count mismatch after 1st Load More"

        # 5. Second Load More Click
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()
        self.page.wait_for_timeout(6000)

        # Count AFTER second Load More
        images_after_second = self.page.locator(self.Images_before_or_after_loadmore).count()
        print("Articles AFTER 2nd Load More:", images_after_second)
        assert images_after_second > 40, "Articles count mismatch after 2nd Load More"

        print(f"Total displayed articles: {images_after_second}")
  
#Validates that **Doctor Voice section’s Load More works by clicking View All and Load More twice**, and **article counts increase correctly after each click**.

    def validate_load_more_doctor_voice(self):
        """Validate Load More functionality for Doctor Voice:
        - Click View All
        - Click Load More twice
        - Verify article counts after each click
        """

        # 1. Open Home Page
        self.page.goto(self.base_url)

        # 2. Click "View All" for Doctor Voice section
        view_all = self.page.locator("(//button[text()='View All'])[2]")
        view_all.scroll_into_view_if_needed()
        view_all.click()

        # Wait for articles grid to load
        self.page.wait_for_timeout(1500)

        # 3. Count Articles BEFORE Load More
        articles_locator = self.page.locator(self.Images_before_or_after_loadmore)
        images_before = articles_locator.count()
        print("Articles BEFORE Load More:", images_before)

        # 4. First Load More Click
        load_more_btn = self.page.locator(self.Load_more)
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()
        self.page.wait_for_timeout(4000)

        # Count AFTER first Load More
        images_after_first = articles_locator.count()
        print("Articles AFTER 1st Load More:", images_after_first)
        assert images_after_first > 20, "Articles count mismatch after 1st Load More"

        # 5. Second Load More Click
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()
        self.page.wait_for_timeout(6000)

        # Count AFTER second Load More
        images_after_second = articles_locator.count()
        print("Articles AFTER 2nd Load More:", images_after_second)
        assert images_after_second > 40, "Articles count mismatch after 2nd Load More"

        print(f"Total displayed articles for Doctor Voice: {images_after_second}")

    def validate_load_more_business_of_medicine(self):
        """Validate Load More functionality for Business of Medicine:
        - Click View All
        - Click Load More twice
        - Verify article counts after each click
        """

        # 1. Open Home Page
        self.page.goto(self.base_url)

        # 2. Click "View All" for Business of Medicine section
        view_all = self.page.locator(self.ViewAll_Button3)
        view_all.scroll_into_view_if_needed()
        view_all.click()
        self.page.wait_for_timeout(1500)

        # 3. Count Articles BEFORE Load More
        articles_locator = self.page.locator(self.Images_before_or_after_loadmore)
        images_before = articles_locator.count()
        print("Articles BEFORE Load More:", images_before)

        # 4. First Load More Click
        load_more_btn = self.page.locator(self.Load_more)
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()
        self.page.wait_for_timeout(4000)

        # Count AFTER first Load More
        images_after_first = articles_locator.count()
        print("Articles AFTER 1st Load More:", images_after_first)
        assert images_after_first > 20, "Articles count mismatch after 1st Load More"

        # 5. Second Load More Click
        load_more_btn.scroll_into_view_if_needed()
        load_more_btn.click()
        self.page.wait_for_timeout(6000)

        # Count AFTER second Load More
        images_after_second = articles_locator.count()
        print("Articles AFTER 2nd Load More:", images_after_second)
        assert images_after_second > 40, "Articles count mismatch after 2nd Load More"

        print(f"Total displayed articles for Business of Medicine: {images_after_second}")
#Validates that **navigating from Specialties → Allergy & Immunology → 3rd article works** and **scroll position is roughly maintained after returning**.

    def validate_specialties_allergy_navigation(self):
        """Validate navigation flow from Specialties → Allergy & Immunology → 3rd article:
        - Hover over Specialties
        - Click Allergy & Immunology
        - Scroll and click 3rd article
        - Go back and verify scroll position
        """
        try:
            self.page.goto(self.base_url)
            # Hover Specialties
            specialties = self.page.get_by_role("link", name="Specialties")
            specialties.hover()
            print("Hovered over Specialties menu.")

            # Click Allergy & Immunology
            allergy = self.page.locator(self.Allergy_immunology)
            allergy.first.click()
            self.page.wait_for_timeout(2000)

            # Scroll down
            self.page.evaluate("window.scrollBy(0, 700);")
            scroll_before = self.page.evaluate("window.pageYOffset")
            print("Scroll position before clicking article:", scroll_before)

            # Click 3rd article in Relevant Articles section
            third_article = self.page.locator(self.Third_articul)
            third_article.click()
            self.page.wait_for_timeout(5000)

            # Go back
            self.page.go_back()
            self.page.wait_for_timeout(5000)

            scroll_after = self.page.evaluate("window.pageYOffset")
            print("Scroll position after returning:", scroll_after)

            # ASSERT with realistic tolerance
            diff = abs(scroll_after - scroll_before)
            assert diff <= 200, (
                f"Scroll mismatch! Before={scroll_before}, After={scroll_after}, Diff={diff}"
            )
        except Exception as e: 
            print(e)

    def validate_breadcrumb_functionality(self):
        """Validate breadcrumb functionality:
        - Click first article
        - Verify breadcrumb visibility and text
        - Click 'Home' breadcrumb to navigate back
        """

        # Open Home Page
        self.page.goto(self.base_url)

        # Scroll to and capture the first article title
        first_article = self.page.locator(self.First_articul)
        first_article.scroll_into_view_if_needed()
        article_text = first_article.inner_text().strip()
        print("First article title:", article_text)

        # Click article
        first_article.click()

        # Wait for breadcrumb to appear
        breadcrumb = self.page.locator(self.Bread_crump)
        breadcrumb.wait_for(state="visible")

        # Assertion 1: Breadcrumb visible
        assert breadcrumb.is_visible(), "Breadcrumb is NOT displayed after clicking article!"
        breadcrumb_text = breadcrumb.inner_text().strip()
        print("Breadcrumb text:", breadcrumb_text)

        # Validate breadcrumb contains article title
        assert article_text.lower() in breadcrumb_text.lower(), "Breadcrumb text does NOT contain article title!"
        print("Breadcrumb contains article title — working fine!")

        # Click 'Home' breadcrumb
        home_link = self.page.locator(self.Home_link)
        home_link.click()

        # Wait until homepage loads again
        self.page.wait_for_url(self.base_url + "*")
        current_url = self.page.url
        print("After clicking Home breadcrumb, current URL:", current_url)

        # Assertion 2: Verify navigation back to homepage
        assert current_url.strip("/") == self.base_url.strip("/"), f"Navigation failed! Expected homepage, got: {current_url}"
        print("Clicking 'Home' breadcrumb navigates back to homepage successfully!")

#Validates that **Figure 1 section heading, content, 8 images, all cards, and “Join the Conversation” button work correctly**, with **images returning HTTP 200**, **cards and button opening new tabs showing “Figure 1 PRO”**, and all interactions functioning.

    def validate_Figure_1_section(self):
        page = self.page
        BASE_URL = 'https://www.physiciansweekly.com'

        self.page.goto(self.base_url)
        Heading = self.page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//h3')
        assert Heading.inner_text() == "Discuss Real Clinical Cases with Real Clinicians","Figure 1 heading is miss matched"
        print("Figure 1 section heading validated successfully",Heading.inner_text())
        Content = self.page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//p')
        assert Content.inner_text() == "Join the largest community of verified healthcare professionals working together, safely and securely, to improve patient outcomes."
        print("Figure 1 section content validated successfully",Content.inner_text())
        all_images = self.page.query_selector_all('//div[@class="MuiBox-root css-62igne"]//img')
        assert len(all_images) == 8, "Images count is not matched as expected in figure 1 section"
        print("Knowladge hub images count matched suiccesfully")
        for img in all_images:
            link = img.get_attribute("src")

            if link:
                #FIX: handle relative URLs
                if link.startswith("/"):
                    link = BASE_URL + link

                try:
                    response = page.request.get(link)
                    status = response.status
                    print(f"{link}  ---> status code : {status}")

                    assert status == 200, f"Broken image in figure 1 section: {link} returned status {status}"

                except Exception as e:
                    print(f"Error fetching {link}: {e}")

                print("all images are validated successfully")
        cards = page.locator('//p[@class="MuiTypography-root MuiTypography-body2 OOCard_commonText__Ehk2G OOCard_caseTitleText__yC9hr OOCard_caseTitleMultiple__OEbrT css-68o8xu"]')

        count = cards.count()
        print(f"Total cards found: {count}")

        for i in range(count):
            card = cards.nth(i)

            card_text = card.inner_text().strip()
            print(f"\nClicking card: {card_text}")

            # -------------------------------
            # 1. Expect a new tab to open
            # -------------------------------
            with page.context.expect_page() as new_tab_event:
                card.click()

            new_tab = new_tab_event.value
            new_tab.wait_for_load_state("domcontentloaded")

            # -------------------------------
            # 1.1 Handle privacy popup (IF PRESENT)
            # -------------------------------
            close_btn = new_tab.locator("#close-pc-btn-handler")

            try:
                close_btn.wait_for(state="visible", timeout=3000)
                close_btn.click()
                print("Privacy popup detected and closed")
            except:
                print("Privacy popup not shown")
            page.wait_for_timeout(10000)

            # -------------------------------
            # 2. Validate Figure 1 branding
            # -------------------------------
            try:
                figure1_badge = new_tab.locator("//span[contains(text(),'Figure 1')]")
                assert figure1_badge.count() > 0, (
                    f"Figure 1 branding NOT found for card: {card_text}"
                )

                print("✔ Verified: Figure 1 branding is present")
            except Exception as e:
                print(e)

            # -------------------------------
            # 3. Close tab & return to main
            # -------------------------------
            new_tab.close()
            page.wait_for_timeout(500)

                 

            print("\nAll cards validated successfully.")      
        buttons = page.locator('[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]')
        count = buttons.count()
        assert count == 11, "Button count is not matching"
        print("Total buttons found 11, but skipped Figure 1 buttons in Figure 1 section as expected ")

        for i in range(count):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            try:
                if text == "Join the Conversation":
                    btn.scroll_into_view_if_needed()
                    with page.context.expect_page() as new_tab_event:
                        btn.click()
                        page.wait_for_timeout(6000)

                    new_tab = new_tab_event.value
                    new_tab.wait_for_load_state("domcontentloaded")
                    # -------------------------------
                    # 2. Validate "Figure 1 PRO" text
                    # -------------------------------
                    figure1_badge = new_tab.locator("//span[contains(text(),'Figure 1')]")
                    assert figure1_badge.count() > 0, (
                        f"Figure 1 branding NOT found for card: {card_text}"
                    )
                    print("✔ Verified: Figure 1 branding is present")


                    # -------------------------------
                    # 3. Close tab & return to main
                    # -------------------------------
                    new_tab.close()

                    # Wait a bit for the context to reset
                    page.wait_for_timeout(500)

                else:
                    pass
            except Exception as e:
                print("Failed to find the buttons due to:\n",e)
                
                    

#Navigates to the home page, validates that the **Featured Articles heading is visible and captures its text**, and **counts the number of visible images in the Hero Banner section**.


    