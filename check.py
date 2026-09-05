import asyncio
import os
import subprocess
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.swroasting.coffee/", wait_until="networkidle")
        
        page_text = await page.evaluate("document.body.innerText")
        await browser.close()

    current_drop = "Unknown"
    for line in page_text.split('\n'):
        if "Current drop is roast date" in line:
            current_drop = line.strip()
            break

    print(f"Live site says: {current_drop}")

    filename = "last_drop.txt"
    last_drop = ""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            last_drop = f.read().strip()

    if current_drop != last_drop:
        print(f"NEW DROP DETECTED! Old: {last_drop} | New: {current_drop}")
        
        with open(filename, "w") as f:
            f.write(current_drop)
            
        # Commit and push the updated file internally before throwing the error
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"])
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])
        subprocess.run(["git", "add", filename])
        subprocess.run(["git", "commit", "-m", "Auto-update last seen drop date"])
        subprocess.run(["git", "push"])
        
        raise Exception(f"ALERT: S&W Roasting updated their drop to: {current_drop}")
    else:
        print("No change in the drop date yet.")

asyncio.run(main())
