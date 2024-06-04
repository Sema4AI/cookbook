# Use Playwright for extracting html from website

The example shows how to open a browser (headless or not) and extract website html or portion of it.

```py
from robocorp import browser
```

The browser automation is done with Robocorp Playwright library, making life easier for the developers than just the plain Playwright.

```py
browser.configure(browser_engine="chromium", headless=True)
```

Edit the boolean value for `headless` to either see, or unsee, the browser.

```py
return html
```

Your `@action` can only return text or boolean values for now (more type support coming soon), so remember to dump html as string content.
