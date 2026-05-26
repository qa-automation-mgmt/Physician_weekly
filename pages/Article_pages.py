from playwright.sync_api import Page
import requests
from helpers.common_functions import CommonHelper

URLS = [
    "https://www.physiciansweekly.com/post/from-unknown-cause-to-genetic-clarity-a-kidney-disease-story-every-clinician-should-he",
    #"https://www.physiciansweekly.com/post/stress-cmr-reduces-radiation-exposure-in-ed-chest-pain-evaluation",
#     "https://www.physiciansweekly.com/post/post-ophthalmic-surgery-opioids-tied-to-limited-pain-relief-more-er-visits",
#     "https://www.physiciansweekly.com/post/qa-navigating-guidance-on-use-of-steroids-in-sepsis",
#     "https://www.physiciansweekly.com/post/piv-vasopressors-reduce-aes-cvc-placement-in-hypotension-shock-critical-illness",
        ]


class PostArticlePages:
    BASE_URL = "https://www.physiciansweekly.com"

    def __init__(self, page: Page):
        self.page = page
        self.FromHelper = CommonHelper()

    def verify_author_and_last_updated(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that the **author name and last updated date** "
            "are correctly displayed on the post article page."
        )
        try:
            self.FromHelper.validate_author_and_last_updated(self.page)
            print("Author and Last Updated validation completed successfully.")
        except Exception as e:
            print(f"Error during author and last updated validation: {e}")

    def verify_social_media_buttons(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that **all social media buttons** "
            "are present and functional on the post article page."
        )
        try:
            self.FromHelper.validate_social_media_buttons(self.page)
            print("Social media buttons validation completed successfully.")
        except Exception as e:
            print(f"Error during social media buttons validation: {e}")

    def verify_hero_banner(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that the **Hero Banner** "
            "is correctly displayed with a valid image on the post article page."
        )
        try:
            self.FromHelper.verify_hero_banner_for_post_pages_helper(self.page)
            print("Hero Banner validation completed successfully.")
        except Exception as e:
            print(f"Error during hero banner validation: {e}")

    def verify_related_posts(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that the **Related Posts section** "
            "displays correct articles with valid images and working links on the post article page."
        )
        try:
            self.FromHelper.Related_post_Function_helper(self.page)
            print("Related Posts section validation completed successfully.")
        except Exception as e:
            print(f"Error during related posts validation: {e}")

    def verify_post_tags(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that **Post Tags** "
            "are present and correctly linked on the article page."
        )
        try:
            self.FromHelper.validate_Post_tags_in_articul_pages(self.page)
            print("Post Tags validation completed successfully.")
        except Exception as e:
            print(f"Error during post tags validation: {e}")

    def verify_reference_section(self, url):
        self.page.goto(url)
        print(
            f"\nTesting page: {url} and Test Case: Validates that the **Reference Section** "
            "is present with correctly formatted and accessible references on the post article page."
        )
        try:
            self.FromHelper.Validate_reference_section(self.page)
            print("Reference section validation completed successfully.")
        except Exception as e:
            print(f"Error during reference section validation: {e}")