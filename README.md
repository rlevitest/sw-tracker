# S&W Roasting Drop Tracker

A free, automated serverless tracker that monitors [S&W Craft Roasting](https://www.swroasting.coffee/) for new coffee drop updates using Python, Playwright, and GitHub Actions.

## How It Works
* **Scheduled Execution:** Runs automatically every 12 hours via GitHub Actions workflow triggers.
* **Headless Rendering:** Boots a headless Chromium browser via Playwright to fully parse the JavaScript-driven Square Online storefront.
* **Text Extraction:** Scrapes the page inner text to isolate the active drop date string (e.g., *Current drop is roast date 9-1-26*).
* **State Comparison:** Compares the live site string against the local tracking state stored in `last_drop.txt`.
* **Alert Trigger:** If a new drop is identified, it updates the text file, commits the change back to the repository, and throws an exception to fail the workflow, triggering your notification pipeline.

## Repository Structure
* `check.py`: The asynchronous Python script that manages scraping, logic verification, file updates, and internal git auto-commits.
* `.github/workflows/monitor.yml`: The workflow configuration file defining the cron schedule, Python setup, and Playwright dependencies.
* `last_drop.txt`: A flat text file tracking the last seen drop identifier to prevent duplicate alerts.

## Quick Setup Guide
1. Create a new repository on GitHub named `sw-tracker`.
2. Add the `check.py` script and `.github/workflows/monitor.yml` configuration to your repository files.
3. Grant write permissions to the runner by navigating to your repository **Settings > Actions > General > Workflow permissions**, select **Read and write permissions**, and save.
4. Create a `last_drop.txt` file in the root directory containing the current drop string to initialize tracking.
