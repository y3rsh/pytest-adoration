import pytest
from playwright.sync_api import Page

from src.util import timestamp


@pytest.mark.pw
def test_pw(page: Page):
    """
    simple browser actions copied from tutorials
    """
    page.goto("https://example.com")
    assert page.inner_text("h1") == "Example Domain"
    page.click("text=More information")
    page.screenshot(path=f"more-info-{timestamp()}.png")
    page.goto("http://whatsmyuseragent.org/")
    page.screenshot(path=f"browser-{timestamp()}.png")
