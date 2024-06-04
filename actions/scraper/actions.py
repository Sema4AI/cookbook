from sema4ai.actions import action
from robocorp import browser

@action
def scrape(url: str, selector: str = "", timeout: int = 3000) -> str:
    """Extract site html

    Args:
        url (str): Url to extract html from
        selector (str): Section of the html to extract by selector
        timeout (int): Timeout for waiting page or selector to load

    Returns:
        str: page or section html.
    """

    browser.configure(browser_engine="chromium", headless=True)
    page = browser.goto(url)

    if selector != "":
        page.wait_for_selector(selector, timeout=timeout)
        partials = page.locator(selector).all()

        html_partials = [partial.evaluate("el => el.outerHTML") for partial in partials]
        html = '\n'.join(html_partials)
    else:
        page.wait_for_timeout(timeout)
        html = page.content()

    page.close()
    return html

