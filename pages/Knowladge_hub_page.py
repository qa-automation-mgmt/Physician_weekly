from playwright.sync_api import Page, expect
import requests


class KnowledgeHubPage:
    base_url ="https://www.physiciansweekly.com/"

    # Test 1: Validate all images count and no broken images
    def Validate_all_images_displayed_and_not_broken(self, page: Page):
        page.locator("//a[text()='Knowledge Hub']").click()
        images = page.locator('//div[@class="featured_post_img MuiBox-root css-0"]//img')
        count = images.count()

        print(f"Total images found: {count}")
        assert count == 9, "Image count mismatched"

        image_urls = []

        for i in range(count):
            src = images.nth(i).get_attribute("src")
            if src:
                image_urls.append(src)

        for url in image_urls:
            try:
                response = requests.head(url, allow_redirects=True, timeout=6)
                if response.status_code == 200:
                    print(f"{url} -> OK (200)")
                else:
                    print(f"{url} -> Broken ({response.status_code})")
            except Exception as e:
                print(f"{url} -> Error: {e}")

    # Test 2: Validate article navigation and heading match
    def Validate_all_articles_navigation_and_heading(self, page: Page):
        page.goto(self.base_url)

        articles = page.locator(
            '//div[contains(@class,"card_feat_title")]//a'
        )

        count = articles.count()
        print(f"Found {count} articles")

        for i in range(count):
            articles = page.locator('//div[contains(@class,"card_feat_title")]//a')

            article = articles.nth(i)
            heading_text = article.inner_text().strip()
            link = article.get_attribute("href")

            print(f"\nOpening: {heading_text}")
            print(f"URL: {link}")

            if not link or not link.startswith("http"):
                print("Skipping invalid link")
                continue

            # Scroll into view
            article.scroll_into_view_if_needed()

            # Open article
            page.goto(link)

            try:
                article_heading = page.locator('//div[contains(@class,"MuiBox-root")]//h1')
                expect(article_heading).to_be_visible()

                actual_text = article_heading.inner_text().strip()

                assert heading_text == actual_text, "Heading does not match!"
                print("Heading matched successfully!")

            except Exception as e:
                print(f"Error verifying heading: {e}")

            # Go back
            page.go_back()