# linkedin_bot.py
from playwright.sync_api import sync_playwright
import time

LOGIN_URL = "https://www.linkedin.com/login"
MY_NETWORK_URL = "https://www.linkedin.com/mynetwork/invitation-manager/"

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_pending_requests(self):
        profiles = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(LOGIN_URL)
            page.fill('input[name="session_key"]', self.email)
            page.fill('input[name="session_password"]', self.password)
            page.click('button[type="submit"]')
            page.wait_for_selector('input[placeholder="Search"]', timeout=100000)
            print("Logged in, current url: ", page.url)
            # page.wait_for_url("**/feed")
            page.goto(MY_NETWORK_URL)
            time.sleep(5)
            requests = page.query_selector_all('li.invitation-card')
            for req in requests:
                name = req.query_selector('span.invitation-card__title').inner_text().strip()
                headline = req.query_selector('span.invitation-card__headline').inner_text().strip()
                mutual = req.query_selector('span.invitation-card__shared-connections-count')
                mutual = mutual.inner_text().strip() if mutual else "0"
                profiles.append({
                    "name": name,
                    "headline": headline,
                    "mutual_connections": mutual
                })
            browser.close()
        return profiles

    def accept_request(self, name_list):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto(LOGIN_URL)
            page.fill('input[name="session_key"]', self.email)
            page.fill('input[name="session_password"]', self.password)
            page.click('button[type="submit"]')
            page.wait_for_url("**/feed")
            page.goto(MY_NETWORK_URL)
            time.sleep(5)
            requests = page.query_selector_all('li.invitation-card')
            for req in requests:
                name = req.query_selector('span.invitation-card__title').inner_text().strip()
                if name in name_list:
                    btn = req.query_selector('button.artdeco-button--secondary')
                    btn.click()
                    time.sleep(1)
            browser.close()