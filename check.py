import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.swroasting.coffee/", wait_until="networkidle")
        
        # Extract the specific text block containing the drop date
        page_text = await page.evaluate("document.body.innerText")
        await browser.close()

    # Isolate the line or phrase (e.g., "Current drop is roast date 9-1-26")
    current_drop = "Unknown"
    for line in page_text.split('\n'):
        if "Current drop is roast date" in line:
            current_drop = line.strip()
            break

    print(f"Live site says: {current_drop}")

    # Read the previously saved drop from file
    filename = "last_drop.txt"
    last_drop = ""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            last_drop = f.read().strip()

    # If this is the first time running, save it and exit successfully
    if not last_drop:
        with open(filename, "w") as f:
            f.write(current_drop)
        print(f"Initialized tracking with: {current_drop}")
        return

    # Check if the drop has changed
    if current_drop != last_drop:
        print(f"NEW DROP DETECTED! Old: {last_drop} | New: {current_drop}")
        # Update the file to the new drop
        with open(filename, "w") as f:
            f.write(current_drop)
        # Raise an exception to fail the workflow and trigger your email alert
        raise Exception(f"ALERT: S&W Roasting updated their drop to: {current_drop}")
    else:
        print("No change in the drop date yet.")

asyncio.run(main())
