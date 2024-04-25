import asyncio
import time

from playwright.async_api import async_playwright

from config import SCREENSHOT_SIZE
from logger import logger


async def get_screenshot(
    url: str, screenshot_path: str
) -> tuple[str | None, float | None]:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size(SCREENSHOT_SIZE)

        start_time = time.perf_counter()

        try:
            await page.goto(url)
            await asyncio.sleep(0.5)
            await page.screenshot(path=screenshot_path, timeout=5000)
        except Exception as e:
            logger.exception(e)
            return None, None

        end_time = time.perf_counter()

        title = await page.title()
        await browser.close()

        execution_time = round(end_time - start_time, 2)

    return title, execution_time
