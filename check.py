import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch a headless browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Go to the S&W site and wait for the network to idle (loads JS)
        await page.goto("https://www.swroasting.coffee/", wait_until="networkidle")
        
        # Extract all visible text from the fully rendered page
        page_text = await page.evaluate("document.body.innerText")
        
        await browser.close()
        
        target_phrase = "Current drop is roast date"
        
        if target_phrase in page_text:
            print("Success: Found the roast drop text on the rendered page.")
        else:
            raise Exception("ALERT: Roast drop text not found or changed!")

asyncio.run(main())
