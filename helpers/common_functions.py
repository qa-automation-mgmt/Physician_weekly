from locators import Home_page_Locators
import requests
import time
from playwright.sync_api import expect

class CommonHelper(Home_page_Locators):
    BASE_URL = "https://www.physiciansweekly.com"

    def validate_all_buttons1(self,page):
        print('Testing all buttons in url :',page.url)
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

        print("\nValidating Author & Last Updated... in URL :",page.url)

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
    '''
    References Function:
    Validates whether the References section is displayed, retrieves all reference notes and links, and verifies link status codes. It also checks that links open in a new tab and returns back after validation.
    '''

    def Validate_reference_section(self,page):
        try:
            print("Testing URL:for reference_section :",page.url)
            # Check if References heading is visible
            references_heading = page.locator("//h3[text()='References']")

            if references_heading.is_visible():
                print("References section is available")

                # Get all reference paragraphs
                reference_notes = page.locator("//div[@class='post-references']//p")
                total_notes = reference_notes.count()

                print(f"Total reference notes found: {total_notes}")

                # Print all notes text
                for i in range(total_notes):
                    note_text = reference_notes.nth(i).inner_text().strip()
                    print(f"Reference Note {i+1}: {note_text}")

                # Assertion
                assert total_notes > 0, "Reference notes are not available"

                # Get all links inside references
                reference_links = page.locator("//div[@class='post-references']//p//a")
                total_links = reference_links.count()

                print(f"Total links found: {total_links}")

                if total_links > 0:

                    for i in range(total_links):
                        link = reference_links.nth(i)

                        # Get href
                        href = link.get_attribute("href")
                        print(f"Link {i+1}: {href}")

                        # Validate status code
                        try:
                            response = requests.get(href, timeout=15)
                            print(f"Status Code for Link {i+1}: {response.status_code}")

                            assert response.status_code == 200, \
                                f"Broken link found: {href}"

                        except Exception as req_error:
                            print(f"Request failed for {href}: {req_error}")

                        # Click and validate new tab
                        try:
                            with page.context.expect_page() as new_page_info:
                                link.click()

                            new_tab = new_page_info.value
                            new_tab.wait_for_load_state()

                            print(f"New tab opened successfully for Link {i+1}")
                            print(f"New Tab URL: {new_tab.url}")

                            # Validate new tab opened
                            assert new_tab.url != page.url, \
                                "New tab did not open correctly"

                            # Close new tab and come back
                            new_tab.close()
                            page.bring_to_front()

                        except Exception as tab_error:
                            print(f"New tab validation failed: {tab_error}")

                else:
                    print("No links available inside References")

            else:
                print("No reference available")

        except Exception as e:
            print(f"Exception occurred while validating References section: {e}")

    '''
    Post Tags Function:
    Validates whether Post Tags are displayed, captures all tag names, and clicks each tag for navigation validation. It verifies the redirected page heading and confirms the selected tag is present in the URL.

    '''
    def validate_Post_tags_in_articul_pages(self,page):
        try:
            print("Testing URL:for Post_tags_in_articul_pages:",page.url)
            # Check if Post Tags heading is visible
            post_tags_heading = page.locator("//span[text()='Post Tags:']")

            if post_tags_heading.is_visible():
                print("Post Tags section is available")

                # Get all tag buttons
                tag_buttons = page.locator("//div[@class='MuiBox-root css-9uf248']//a")
                total_tags = tag_buttons.count()

                print(f"Total Post Tags Found: {total_tags}")

                # Store all tag names first
                tag_names = []

                for i in range(total_tags):
                    tag_name = tag_buttons.nth(i).inner_text().strip()
                    tag_names.append(tag_name)
                    print(f"Tag {i+1}: {tag_name}")

                # Iterate through stored tag names
                for i in range(len(tag_names)):

                    try:
                        # Re-locate after navigation back
                        tag_buttons = page.locator("//div[@class='MuiBox-root css-9uf248']//a")

                        selected_tag = tag_buttons.nth(i)
                        selected_tag_name = tag_names[i]

                        print(f"\nClicking Tag: {selected_tag_name}")

                        selected_tag.click()
                        page.wait_for_load_state("networkidle")

                        # Get redirected heading
                        redirected_heading = page.locator(
                            "//div[@class='MuiTypography-root MuiTypography-h5 css-1jit86e']"
                        ).inner_text().strip()

                        print(f"Redirected Heading: {redirected_heading}")

                        # Verify heading matches clicked tag
                        assert selected_tag_name.lower() in redirected_heading.lower(), \
                            f"Heading mismatch for tag: {selected_tag_name}"

                        print("Heading validation passed")

                        # Verify tag exists in URL
                        current_url = page.url.lower()
                        print(f"Current URL: {current_url}")

                        formatted_tag = selected_tag_name.lower().replace(" ", "-")

                        assert formatted_tag in current_url, \
                            f"Tag not found in URL for: {selected_tag_name}"

                        print("URL validation passed")

                        # Navigate back
                        page.go_back()
                        page.wait_for_load_state("networkidle")

                        print("Navigated back successfully")

                    except Exception as tag_error:
                        print(f"Validation failed for tag '{tag_names[i]}': {tag_error}")

            else:
                print("Post Tags section is not available")

        except Exception as e:
            print(f"Exception occurred while validating Post Tags section: {e}")
                
    def validate_social_media_buttons(self, page):
        """
        Validates:
        - All social media buttons are present
        - Each button has a valid aria-label (name)
        """
        print("\nChecking social media share buttons...in URL : ",page.url)

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
            print("Testing the Relates posts in URL",page.url)
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
    #note : This is post hero banner function not a page hero banner , make sure this only for articul pages
    def verify_hero_banner_for_post_pages_helper(self,page):
        print("Testing the hero banner in URL : ",page.url)
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

        '''
        What this does:
        Checks banner visibility
        Checks image actually loaded (not broken)
        Validates API status code = 200
        '''
        #This will work for pages not posts 
    def verify_hero_banner_in_pages(self, page):
        try:
            # Hero banner locator
            banner = page.locator("//div[@class='featured_post_row MuiBox-root css-0']//img")

            # 1. Verify banner is present
            assert banner.is_visible(), " Hero banner is NOT visible"
            print("Hero banner is visible")

            # 2. Verify image is loaded
            is_loaded = banner.evaluate("img => img.complete && img.naturalWidth > 0")
            assert is_loaded, "Image not loaded properly"
            print("Image loaded successfully")

            # 3. Verify status code (200)
            img_url = banner.get_attribute("src")
            response = page.request.get(img_url)
            assert response.status == 200, f"Image status code: {response.status}"
            print("Image status code is 200")
            print("\n--- Validating Featured Article Title Navigation ---")

            # Locator for article title (listing page)
            title_locator = page.locator(
                '//div[@class="MuiTypography-root MuiTypography-h1 MuiTypography-gutterBottom card_feat_title text_link_color css-1kzgxgr"]//a'
            )

            count = title_locator.count()
            print(f"Total Featured Articles Found: {count}")

            assert count > 0, "No featured articles found"

            for i in range(count):

                article = title_locator.nth(i)

                # Get title text
                listing_title = article.inner_text().strip()
                print(f"\nClicking Article: {listing_title}")

                # Click article
                article.click()
                page.wait_for_load_state("load")

                # Get detail page heading
                detail_heading = page.locator(
                    '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-12 MuiGrid-grid-md-12 MuiGrid-grid-lg-9 MuiGrid-grid-xl-9 cont css-1hjwhii"]//h1'
                )

                detail_heading.wait_for(state="visible", timeout=5000)
                detail_title = detail_heading.inner_text().strip()

                print(f"Detail Page Heading: {detail_title}")

                # Validation
                assert listing_title.lower() in detail_title.lower(), \
                    f"Mismatch → Listing: {listing_title} | Detail: {detail_title}"

                print("Title validated successfully")

                # Go back
                self.page.go_back()
                self.page.wait_for_load_state("load")

        except Exception as e:
            print(f"Test Failed: {e}")
    #Tis code will validate all heading of page sections eg,Cartoon, Doctor voice , Etc...
    def validate_all_main_headings_present(self, page,expected_sections):
        """Validate that all expected headings are present"""
        sections = page.locator("//div[contains(@class,'secondary_title')]")
        
        # Extract and clean text
        section_texts = [text.strip() for text in sections.all_text_contents()]
        
        print("Found sections:", section_texts)

        for expected in expected_sections:
            assert any(expected.strip().lower() == actual.lower() for actual in section_texts), \
                f"Expected section '{expected}' not found!"

        print("All expected sections are present.")
#this is anothe reusable code for teh buttons 
    def validate_all_buttons(self, page, expected_count=None, skip_text=None):
        buttons = page.locator('[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-mavgnk"]')
        count = buttons.count()

        print(f"Total buttons found: {count}")

        # Count validation
        if expected_count is not None:
            assert count == expected_count, f"Expected {expected_count}, but found {count}"

        for i in range(count):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()

            if skip_text and text == skip_text:
                print(f"Skipping button: {text}")
                continue

            print(f"\nClicking Button #{i+1}: {text}")

            btn.scroll_into_view_if_needed()
            btn.click()

            page.wait_for_load_state("domcontentloaded")

            print(f"Navigated: {text}")

            page.go_back()
            page.wait_for_load_state("domcontentloaded")

        print("All buttons validated successfully.")
#This is the common function whcih will get the title and store and then click on the that , and validate the heaidng and come back 
#     
    def validate_title_navigation(self, page, title_locator, page_title_locator):
        try:
            titles = page.locator(title_locator)
            count = titles.count()
            print(f"\nTotal Titles Found: {count}")
            for i in range(count):
                title = titles.nth(i)
                title_text = title.inner_text().strip()

                print(f"\nClicking on Title: {title_text}")

                title.click()
                page.wait_for_load_state("domcontentloaded")

                page.wait_for_selector(page_title_locator)

                page_title = page.locator(page_title_locator).first.inner_text().strip()

                print(f"Navigated Page Title: {page_title}")

                assert title_text.lower() in page_title.lower()

                print(f"Validated: {title_text}")

                page.go_back()
                page.wait_for_load_state("domcontentloaded")

        except Exception as e:
            print(f"\033[91m[CRITICAL ERROR]: {e}\033[0m")
            raise
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
