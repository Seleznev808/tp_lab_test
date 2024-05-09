import asyncio
import time

from playwright.async_api import async_playwright

from config import (
    SCREENSHOT_SIZE,
    SCREENSHOT_SLEEP,
    SCREENSHOT_TIMEOUT,
    EXECUTION_TIME_ROUND
)
from exceptions import InvalidURLError
from logger import logger


async def get_screenshot(url: str, screenshot_path: str) -> tuple[str, float]:
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size(SCREENSHOT_SIZE)

        start_time = time.perf_counter()

        try:
            await page.goto(url)
            await asyncio.sleep(SCREENSHOT_SLEEP)
            await page.screenshot(
                path=screenshot_path,
                timeout=SCREENSHOT_TIMEOUT
            )
        except Exception as e:
            logger.exception(e)
            raise InvalidURLError()

        end_time = time.perf_counter()

        title = await page.title()
        await browser.close()

        execution_time = round(
            end_time - start_time,
            EXECUTION_TIME_ROUND
        )

    return title, execution_time
