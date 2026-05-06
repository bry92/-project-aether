from playwright.async_api import async_playwright

class BrowserWrapper:
    async def capture_page(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)
            content = await page.content()
            screenshot_path = f"screenshots/{url.replace('https://', '').replace('/', '_')}.png"
            # os.makedirs("screenshots", exist_ok=True)
            # await page.screenshot(path=screenshot_path)
            await browser.close()
            return {"url": url, "content_length": len(content)}

browser = BrowserWrapper()
