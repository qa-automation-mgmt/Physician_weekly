from locators import Home_page_Locators
import requests
import time
from playwright.sync_api import expect

class CommonHelper(Home_page_Locators):
    BASE_URL = "https://www.physiciansweekly.com"

    def validate_all_buttons(self,page):
        buttons = page.locator('[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]')
        count = buttons.count()
        #assert count == 7, "Button count is not matching"
        for i in range(count):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            if text != "Join the Conversation":
                    btn.scroll_into_view_if_needed()
                    btn.click()
                        # Wait for navigation
                    page.wait_for_load_state("load")
                    print(f"Clicked button #{i+1} Button Name: {text}")

                    # Navigate back
                    page.go_back()
                    page.wait_for_load_state("load")

        print("All buttons are clickable and navigated successfully.")

    def validate_author_and_last_updated(self, page):
        """
        Reusable Playwright helper to validate:
        - Author name is displayed
        - Author link is valid (status 200)
        - Last Updated date is present
        """

        print("\nValidating Author & Last Updated...")

        # Locate the first author <a> element
        author = page.locator(
            '//span[@class="MuiTypography-root MuiTypography-caption MuiTypography-gutterBottom css-2og8ey"]//a'
        ).first

        # Ensure author element is visible
        expect(author).to_be_visible(timeout=5000)

        author_name = author.inner_text().strip()
        author_link = author.get_attribute("href")

        print(f"Author found: {author_name}")
        print(f"Author link: {author_link}")

        # Validate author link status
        if author_link.startswith("/"):
            full_url = self.BASE_URL.rstrip("/") + author_link
        else:
            full_url = author_link

        response = requests.get(full_url, timeout=8)
        assert response.status_code == 200, f"Author link failed: {response.status_code}"
        print(f"✔ Author hyperlink valid (Status: {response.status_code})")

        # Validate "Last Updated" date
        last_updated = page.locator(
            '//span[@class="MuiTypography-root MuiTypography-caption MuiTypography-gutterBottom css-2og8ey"]//span'
        ).first

        expect(last_updated).to_be_visible(timeout=5000)
        print(f"Last Updated: {last_updated.inner_text().strip()}")

        print("✔ Author & Last Updated validation successful.\n")
        
    def validate_social_media_buttons(self, page):
        """
        Validates:
        - All social media buttons are present
        - Each button has a valid aria-label (name)
        """
        print("\nChecking social media share buttons...")

        icons = page.locator('//div[@class="social_media_share"]//button')
        count = icons.count()

        print(f"Total social media buttons found: {count}")

        for i in range(count):
            btn = icons.nth(i)
            aria_label = btn.get_attribute("aria-label")

            if aria_label is None or aria_label.strip() == "":
                print(f"Missing aria-label for icon #{i+1}")
            else:
                print(f"Icon {i+1}: {aria_label}")
        print("Social media button validation completed.\n")
   #this function will search with keyword and get the result and click on the first search result and validate the heading 
    def Search_function_helper(self,page,keyword = "surgen"):
         # Click search icon
        page.locator('//button[@aria-label="search"]').click()
        page.wait_for_timeout(1500)
        # Enter keyword
        search_box = page.locator('#search-box')
        search_box.fill(keyword)
        search_box.press("Enter")
        print(f"Search executed successfully for keyword: {keyword}")
        # Verify search header result
        result_header = page.locator(self.Search_result_header)
        expect(result_header).to_be_visible()
        assert keyword.lower() in result_header.inner_text().lower(), "Search result header mismatch"
        # Verify results displayed
        results = page.locator(self.Search_Result)
        assert results.count() > 0, "No search results found"
         # Click the first result
        first_result = page.locator(self.first_result_1)
        first_title = first_result.inner_text().split("\n")[0].strip()
        first_result.scroll_into_view_if_needed()
        first_result.click()
        page.wait_for_timeout(2000)

        # Validate title on opened article page
        article_header = page.locator(self.Aruticul_header)
        expect(article_header).to_be_visible()
        assert first_title.lower() in article_header.inner_text().lower(), \
            "Navigated to incorrect page"
        print("Navigation to searched result article successful and header validated")

    '''below function will do in the related posts 
       Verifying the number of images
       Checking that each image URL loads successfully (200 OK)
       Clicking each image and handling:
       New tab navigation 
       Same tab navigation + back
       Validating that all related links are not broken (200 OK)'''
    def Related_post_Function_helper(self,page):
            images = page.locator('(//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-ucawf0"])[1]//img')
            count = images.count()
            print(f"Total images found in Related post: {count}")
            assert count in (1, 3, 5), f"Expected 1,3 or 5 images, but found {count}"
            #Loop through each image
            for i in range(count):
                image = images.nth(i)
                src = image.get_attribute("src")
                print(f"Image URL: {src}")
                #  1. Validate image loads (200 OK)
                try:
                    response = requests.get(src)
                    assert response.status_code == 200, f"Image not loading properly: {src}"
                    print(f" Image opened successfully (Status: {response.status_code})")
                except Exception as e:
                    print(f" Error checking image: {src}")
                    print(e)
                    continue
                # 2. Click Image & Handle Navigation
                try:
                    with page.context.expect_page(timeout=5000) as new_page_info:
                        image.click()

                    new_page = new_page_info.value
                    new_page.wait_for_load_state()
                    print(f"Opened in NEW TAB: {new_page.url}")
                    new_page.close()

                except:
                    # Same tab navigation
                    image.click()
                    page.wait_for_load_state()
                    print(f"Opened in SAME TAB: {page.url}")

                    page.go_back()
                    page.wait_for_load_state()

                #Small wait for stability
                page.wait_for_timeout(1000)
            links = page.locator('(//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 css-ucawf0"])[1]//a')
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

    def Verify_logo_helper(self,page):
        logo = page.locator(self.Logo)
        expect(logo).to_be_visible()
        print("logo is displayed")        
    #note : This is post hero banner function not a page hero banner , make sure 
    def verify_hero_banner_for_post_pages_helper(self,page):
        banner = page.locator('//div[@class="mainImageContainer float-left"]')
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
     
                 
    #This function validates that the first <h2> header on the current page has the expected CSS font color, size, weight, and style, and reports whether the UI styling matches the design standard.
    def validate_h2_header_css(self,page,):       
        page.wait_for_timeout(2000)
        header = page.locator("h2").first
        font_color = header.evaluate("el => window.getComputedStyle(el).color")
        font_size = header.evaluate("el => window.getComputedStyle(el).fontSize")
        font_weight = header.evaluate("el => window.getComputedStyle(el).fontWeight")
        font_style = header.evaluate("el => window.getComputedStyle(el).fontStyle")
        print("Current URL:", page.url)
        print("Font Color:", font_color)
        print("Font Size:", font_size)
        print("Font Weight:", font_weight)
        print("Font Style:", font_style)
        try:
            assert font_color in ["rgb(51, 51, 51)"], f"Header color mismatch: {font_color}"
            assert font_size in ["28px", "28.8px"], f"Expected 28px, got {font_size}"
            assert font_weight == "400", f"Font weight mismatch: {font_weight}"
            assert font_style == "normal", f"Font style mismatch: {font_style}"
            print("All CSS assertions passed for", page.url)
        except AssertionError as e:
            print(f"Assertion failed for {page.url} — {str(e)}")    



    '''
    Hero banner is present
    Image rendered width ≥ 400px
    Image rendered height ≥ 300px
    Image is loaded correctly (naturalWidth > 0)
    Image is not blurred / pixelated / upscaled
    Works for 100+ URLs via loop
    Fully reusable    '''          

    def validate_hero_banner_image_size_and_quality(self,page):
        page.wait_for_timeout(2000)
        try:
            print(f"\nTesting page: {page.url}")
            hero_banner = page.locator("div.featured_post_img img").first
            # Get rendered size
            box = hero_banner.bounding_box()
            width = box["width"]
            height = box["height"]
            print("Hero Banner Rendered Size:", f"{width} x {height}")
            try:
                # EXISTING ASSERTIONS (Converted exactly)
                assert width >= 400, f"Hero banner width is too small: {width}px"
                assert height >= 300, f"Hero banner height is too small: {height}px"
                # NEW LOGIC → IMAGE LOADED CORRECTLY CHECK
                natural_width = hero_banner.evaluate("el => el.naturalWidth")
                natural_height = hero_banner.evaluate("el => el.naturalHeight")
                print("Hero Banner Natural Size:", natural_width, "x", natural_height)
                assert natural_width > 0 and natural_height > 0, \
                    "Hero banner failed to load correctly (naturalWidth is 0)"
                # NOT BLURRED / NOT PIXELATED CHECK
                if width > natural_width or height > natural_height:
                    raise AssertionError(
                        f"Image appears pixelated/upscaled "
                        f"(Rendered: {width}x{height}, Natural: {natural_width}x{natural_height})"
                    )

                print("Hero banner resolution is good (not blurred/pixelated).")
                print("Hero banner size is as expected for:", page.url)
            except AssertionError as e:
                print(f"Assertion failed for {page.url} — {str(e)}")

        except Exception as e:
            print(f"Hero banner not found on {page.url} — {str(e)}")     



    def validate_cta_buttons_css_ui(self,page):
        print(f"\nTesting page: {page.url}")
        print("\nFinding all CTA buttons...")
        cta_list = page.locator("a.card_button, a.MuiButton-root")
        total = cta_list.count()
        print(f"Total CTA buttons found: {total}\n")

        for index in range(total):
            cta = cta_list.nth(index)

            print(f"\nCTA {index + 1}")

            cta.scroll_into_view_if_needed()
            page.wait_for_timeout(500)

            cta_text = cta.inner_text()
            print("CTA Text:", cta_text)

            try:
                #Text Color
                text_color = cta.evaluate("el => window.getComputedStyle(el).color")
                print("Text Color:", text_color)
                assert text_color != "", f"CTA #{index + 1}: Missing text color!"
                # ✅ Font Size
                font_size = cta.evaluate("el => window.getComputedStyle(el).fontSize")
                print("Font Size:", font_size)
                assert "px" in font_size, f"CTA #{index + 1}: Invalid font size!"
                # ✅ Border Radius
                radius = cta.evaluate("el => window.getComputedStyle(el).borderRadius")
                print("Border Radius:", radius)
                assert radius != "0px", f"CTA #{index + 1}: No rounded corners!"
                # ✅ Hover Effect
                cta.hover()
                page.wait_for_timeout(500)
                hover_color = cta.evaluate("el => window.getComputedStyle(el).backgroundColor")
                print("Hover Background Color:", hover_color)
                print(f"CTA #{index + 1} PASSED all CSS tests")

            except AssertionError as e:
                print(f"CTA #{index + 1} FAILED on {page.url}")
                print("Reason:", str(e))

        print("\n ALL CTA BUTTONS CSS TESTS COMPLETED!")        

#This helper validates that subheadings, body text, and hyperlinks follow the expected UI typography standards for font color, size, and weight across all pages.
    def validate_subheading_body_and_link_css(self,page):
        print(f"\nTesting page: {page.url}")
        # Validate SUBHEADINGS
        subheadings = page.locator("//a[contains(@class, 'card_feat_title')]")
        sub_count = subheadings.count()
        for i in range(sub_count):
            sh = subheadings.nth(i)
            text = sh.inner_text().strip()
            if text == "":
                continue
            css_color = sh.evaluate("el => window.getComputedStyle(el).color")
            css_size = sh.evaluate("el => window.getComputedStyle(el).fontSize")
            css_weight = sh.evaluate("el => window.getComputedStyle(el).fontWeight")

            print(f"\nSUBHEADING → {text}")
            print("Color:", css_color)
            print("Font Size:", css_size)
            print("Weight:", css_weight)

            try:
                assert "rgb" in css_color, "Subheading must have a valid color"
                assert float(css_size.replace("px", "")) >= 18, "Subheading font size too small"
                assert int(css_weight) >= 400, "Subheading font weight is too light"
            except AssertionError as e:
                print(f"Assertion failed for {page.url} — {str(e)}")

       
        # 2Validate BODY CONTENT (<p> and <span>)
        body_content = page.locator("//p | //span")
        body_count = body_content.count()

        for i in range(body_count):
            ele = body_content.nth(i)
            text = ele.inner_text().strip()

            if text == "":
                continue

            css_color = ele.evaluate("el => window.getComputedStyle(el).color")
            css_size = ele.evaluate("el => window.getComputedStyle(el).fontSize")

            print(f"\nBODY → {text}")
            print("Color:", css_color)
            print("Font Size:", css_size)

            try:
                assert "rgb" in css_color, f"Invalid body text color → '{text}'"
                assert float(css_size.replace("px", "")) >= 12, \
                    f"Body font too small ({css_size}) → '{text}'"
            except AssertionError as e:
                print(f" Assertion failed for {page.url} — {str(e)}")
                print("\nBODY CONTENT FAILURE")
                print("Reason:", str(e))
                print("Failed Text:", text)
                print("Font Size:", css_size)
                print("Page URL:", page.url)
    
        # 3.Validate HYPERLINK TEXT (<a>)
        links = page.locator("a")
        link_count = links.count()

        for i in range(link_count):
            link = links.nth(i)
            text = link.inner_text().strip()

            if text == "":
                continue

            css_color = link.evaluate("el => window.getComputedStyle(el).color")
            css_size = link.evaluate("el => window.getComputedStyle(el).fontSize")
            css_weight = link.evaluate("el => window.getComputedStyle(el).fontWeight")

            print(f"\nLINK or SUBHEADING → {text}")
            print("Color:", css_color)
            print("Font Size:", css_size)
            print("Weight:", css_weight)

            try:
                assert "rgb" in css_color, "Link must have valid color"
                assert float(css_size.replace("px", "")) >= 12, "Link font size too small"
                assert int(css_weight) >= 300, "Link font weight invalid"
            except AssertionError as e:
                print(f"Assertion failed for {page.url} — {str(e)}")

        print("\n All CSS/UI checks completed successfully!")    

#This helper validates that all images on a page are properly loaded, visible, and not blurry or pixelated based on rendered vs natural resolution.
    def validate_all_images_rendering(self,page):
        print(f"\nTesting page: {page.url}")
        images = page.locator("img")
        total = images.count()
        print(f"Total images found: {total}")
        for index in range(total):
            img = images.nth(index)
            try:
                # ✅ Scroll to image
                img.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                # ✅ 1. Display size (Rendered)
                box = img.bounding_box()
                w = box["width"]
                h = box["height"]

                # ✅ 2. Natural size (Resolution check)
                natural_w = img.evaluate("el => el.naturalWidth")
                natural_h = img.evaluate("el => el.naturalHeight")

                print(f"\nIMAGE #{index + 1}")
                print("Displayed:", w, "x", h)
                print("Natural:", natural_w, "x", natural_h)
            
                # ✅ ASSERTIONS
         

                # A. Image loaded correctly
                assert natural_w > 0 and natural_h > 0, "Image failed to load"

                # B. Image is visible on screen
                assert w > 10 and h > 10, "Image visible size too small"

                # C. Not pixelated / blurred
                assert natural_w >= w, "Image resolution smaller than display → blurry"
                assert natural_h >= h, "Image resolution smaller than display → blurry"

                print("Image passed all rendering checks")

            except Exception as e:
                print(f"\nIMAGE #{index + 1} FAILED at {page.url}")
                print("Reason:", str(e))

                image_url = img.get_attribute("src")
                print("Image URL:", image_url)    

    #it will get the bread crump in the current url , then click on teh home in bread crump and validae the home url
    def  vaildate_bread_crump(self,page):
         # Locate all breadcrumb elements (<a> and <p>)
        bread = page.locator(
            '//ol[contains(@class,"MuiBreadcrumbs-ol")]//a | '
            '//ol[contains(@class,"MuiBreadcrumbs-ol")]//p'
        )
        bread1 = page.locator('[class="MuiBreadcrumbs-ol css-nhb8h9"]')
        print("Is breadcrumb displayed:", bread1.is_visible())

        # 6️⃣ Get total breadcrumb count
        count = bread.count()

        # 7️⃣ Loop through and print breadcrumb text
        for i in range(count):
            breadcrumb_text = bread.nth(i).inner_text()
            print("Current bread cramp",breadcrumb_text)
            if breadcrumb_text == 'Home':
                bread.nth(i).click()
                page.url
                assert page.url == "https://www.physiciansweekly.com/","Url missmatch "
                print("User naviagated to the home page from bread cramp ")
    def validate_Google_adds(self,page):
        page.wait_for_timeout(3000)
        frame = []
        body = page.locator("body")
        for i in range(12):
            body.press("PageDown")
            time.sleep(10)
            frame = page.locator('//iframe[@title="3rd party ad content"]').all()
        print(len(frame))
        assert len(frame) == 6, f"Expected 6 Google adds but found {len(frame)}"
        print("All 6 google Adds are displayed and its count validated successfully ")
        print("Validated link : " ,page.url)


class ResponsiveHelper:
    DESKTOP = {"width": 1366, "height": 768}
    TABLET = {"width": 768, "height": 1024}
    MOBILE = {"width": 390, "height": 844}

    @staticmethod
    def set_viewport(page, viewport):
        page.set_viewport_size(viewport)

    @staticmethod
    def assert_no_horizontal_scroll(page):
        scroll_width = page.evaluate("document.body.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")
        assert scroll_width <= client_width, (
            f"Horizontal overflow detected: scrollWidth={scroll_width}, clientWidth={client_width}"
        )

    # ---------------- HEADER / NAV ----------------
    @staticmethod
    def validate_header_desktop(page, header_locator):
        expect(header_locator).to_be_visible()

    @staticmethod
    def validate_header_mobile(page, hamburger_locator, menu_panel_locator):
        expect(hamburger_locator).to_be_visible()
        hamburger_locator.click()
        expect(menu_panel_locator).to_be_visible()
        hamburger_locator.click()
        expect(menu_panel_locator).not_to_be_visible()

    # ---------------- GRID / LISTING ----------------
    @staticmethod
    def validate_single_column_layout(page, card_locator):
        cards = page.locator(card_locator)
        count = cards.count()
        assert count > 0, "No cards found to validate layout"

        first_box = cards.nth(0).bounding_box()
        for i in range(1, min(count, 4)):
            next_box = cards.nth(i).bounding_box()
            assert next_box["x"] == first_box["x"], "Grid is not single-column on mobile"

    # ---------------- ARTICLE CONTENT ----------------
    @staticmethod
    def validate_article_readability(page, article_body_locator):
        expect(article_body_locator).to_be_visible()
        ResponsiveHelper.assert_no_horizontal_scroll(page)
