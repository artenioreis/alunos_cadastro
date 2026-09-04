import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        print("Navigating to login page...")
        await page.goto("http://127.0.0.1:5000/login")

        print("Logging in...")
        await page.fill("#username", "admin")
        await page.fill("#password", "1234")
        await page.click("button[type='submit']")

        print("Waiting for dashboard to load...")
        await page.wait_for_selector(".main-content")

        # We need an alert to test the close button. Let's trigger one by submitting a form with empty required fields (to cause a flash message) or navigating to a specific URL that generates an error.
        # Alternatively, let's just trigger a logout then login with bad credentials to see the error message.
        print("Logging out to trigger an error message for testing the dismiss button...")
        await page.goto("http://127.0.0.1:5000/logout")

        print("Logging in with bad credentials...")
        await page.fill("#username", "admin")
        await page.fill("#password", "wrongpassword")
        await page.click("button[type='submit']")

        print("Checking for alert and dismiss button...")
        await page.wait_for_selector(".alert")

        # Verify the close button has the correct aria-label and data-bs-dismiss attribute
        close_btn = await page.query_selector(".btn-close")
        aria_label = await close_btn.get_attribute("aria-label")
        data_dismiss = await close_btn.get_attribute("data-bs-dismiss")

        if aria_label == "Fechar" and data_dismiss == "alert":
            print("SUCCESS: Close button has correct attributes (aria-label='Fechar', data-bs-dismiss='alert')")
        else:
            print(f"FAILED: Close button has incorrect attributes (aria-label='{aria_label}', data-bs-dismiss='{data_dismiss}')")

        print("Clicking the close button...")
        await close_btn.click()

        # Now let's log back in and test the sidebar toggle
        print("Logging in with correct credentials...")
        await page.fill("#username", "admin")
        await page.fill("#password", "1234")
        await page.click("button[type='submit']")

        print("Waiting for dashboard to load...")
        await page.wait_for_selector(".main-content")

        # Verify the sidebar toggle button has the correct aria-label
        sidebar_btn = await page.query_selector("#sidebarCollapse")
        sidebar_aria_label = await sidebar_btn.get_attribute("aria-label")

        if sidebar_aria_label == "Alternar menu":
            print("SUCCESS: Sidebar button has correct aria-label ('Alternar menu')")
        else:
            print(f"FAILED: Sidebar button has incorrect aria-label ('{sidebar_aria_label}')")

        print("Clicking sidebar collapse button...")
        await sidebar_btn.click()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
