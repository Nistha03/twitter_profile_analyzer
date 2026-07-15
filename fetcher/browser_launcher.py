import os
from playwright.sync_api import sync_playwright, BrowserContext

class BrowserLauncher:
    def __init__(self, user_data_dir: str = "browser_profile") -> None:
        self.user_data_dir = user_data_dir
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    def get_context(self, playwright) -> BrowserContext:
        return playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )