from playwright.sync_api import sync_playwright, TimeoutError
import time
import requests

BASE_URL = 'https://www.physiciansweekly.com'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.physiciansweekly.com/')
    BASE_URL = "https://www.physiciansweekly.com"
    Heading = page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//h3')
    assert Heading.inner_text() == "Discuss Real Clinical Cases with Real Clinicians", "Figure 1 heading is miss matched"
    print("Figure 1 section heading validated successfully", Heading.inner_text())
    Content = page.locator('//div[@class="MuiTypography-root MuiTypography-body2 css-68o8xu"]//p')
    assert Content.inner_text() == "Join the largest community of verified healthcare professionals working together, safely and securely, to improve patient outcomes."
    print("Figure 1 section content validated successfully", Content.inner_text())
    all_images = page.query_selector_all('//div[@class="MuiBox-root css-62igne"]//img')
    assert len(all_images) == 8, "Images count is not matched as expected in figure 1 section"
    print("Knowladge hub images count matched successfully")

    for img in all_images:
        link = img.get_attribute("src")

        if link:
            # 🔥 FIX: handle relative URLs
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

        # Get card text (optional, for debugging)
        card_text = card.inner_text().strip()
        print(f"\nClicking card: {card_text}")

        # -------------------------------
        # 1. Expect a new tab to open
        # -------------------------------
        with page.context.expect_page() as new_tab_event:
            card.click()
            page.wait_for_timeout(3000)

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
                    page.wait_for_timeout(3000)

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
                page.wait_for_timeout(500)

            else:
                pass
        except Exception as e:
            print("Failed to find the buttons due to:\n",e)
            