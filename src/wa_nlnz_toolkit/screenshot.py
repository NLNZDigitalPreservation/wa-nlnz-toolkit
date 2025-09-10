import asyncio
from playwright.async_api import async_playwright
import validators

async def take_screenshot_async(website_url: str):
    if not validators.url(website_url):
        print(f"Invalid URL: {website_url}. Aborting...")
        return

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True, viewport={"width": 1920, "height": 4000})
        try:
            await page.goto(website_url)

            # await page.evaluate("""() => {
            #     window.scrollBy(0, document.body.scrollHeight);
            # }""")
            # await page.wait_for_timeout(2000)  # wait for lazy-loaded content

        except Exception as e:
            print(f"Failed to load URL: {website_url}. Error: {e}")
        else:
            screenshot_filename = f"{website_url.replace('https://', '').replace('/', '_')}.png"
            await page.screenshot(path=screenshot_filename, full_page=True)
            print(f"Screenshot saved as {screenshot_filename}")
        await browser.close()


# TEST - Run the async function in Jupyter
# await take_screenshot_async("https://ndhadeliver.natlib.govt.nz/webarchive/20250401004141/https://covid19.govt.nz/")
