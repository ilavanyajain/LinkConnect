from playwright.sync_api import sync_playwright, Page, Browser, Playwright, TimeoutError
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Selectors:
    LOGIN_URL = "https://www.linkedin.com/login"
    MY_NETWORK_URL = "https://www.linkedin.com/mynetwork/invitation-manager/"
    
    # Login Page
    EMAIL_INPUT = 'input[name="session_key"]'
    PASSWORD_INPUT = 'input[name="session_password"]'
    LOGIN_BUTTON = 'button[type="submit"]'
    
    # Feed Page (Post-Login)
    FEED_SEARCH_INPUT = 'input[placeholder="Search"]'
    
    # Invitation Manager Page
    INVITATION_LIST = 'ul.artdeco-list'
    INVITATION_CARD = 'li.invitation-card'
    INVITATION_CARD_ACCEPT_BTN = 'button[aria-label^="Accept"]'
    
    # Invitation Card Details
    NAME_SELECTOR = '.invitation-card__title'
    PROFILE_LINK_SELECTOR = 'a.invitation-card__link'
    HEADLINE_SELECTOR_1 = '.invitation-card__subtitle'
    MUTUAL_CONNECTIONS_SELECTOR = 'span.member-insights__count'

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.playwright: Playwright = None
        self.browser: Browser = None
        self.page: Page = None

    def start_browser(self, headless=True):
        logging.info("Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.page = self.browser.new_page()

    def close_browser(self):
        logging.info("Closing browser...")
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def _human_delay(self, min_seconds=1, max_seconds=3):
        time.sleep(random.uniform(min_seconds, max_seconds))

    def login(self):
        if not self.page:
            raise Exception("Browser not started. Call start_browser() first.")
        
        logging.info("Attempting to log in...")
        self.page.goto(Selectors.LOGIN_URL)
        self._human_delay()
        
        self.page.fill(Selectors.EMAIL_INPUT, self.email)
        self._human_delay()
        self.page.fill(Selectors.PASSWORD_INPUT, self.password)
        self._human_delay()
        self.page.click(Selectors.LOGIN_BUTTON)
        
        try:
            self.page.wait_for_selector(Selectors.FEED_SEARCH_INPUT, timeout=60000)
            logging.info("Login successful.")
            return True
        except TimeoutError:
            logging.error("Login failed. Could be due to incorrect credentials, 2FA, or a CAPTCHA.")
            return False

    def get_pending_requests(self):
        if not self.page:
            raise Exception("Browser not started. Call start_browser() first.")

        logging.info("Navigating to invitation manager...")
        self.page.goto(Selectors.MY_NETWORK_URL, timeout=60000)
        try:
            self.page.wait_for_selector(Selectors.INVITATION_LIST, timeout=30000)
        except TimeoutError:
            logging.warning("No invitation list found. You may have no pending requests.")
            return []

        # Scroll to load all invitations
        self._scroll_to_bottom()

        profiles = []
        invitations = self.page.query_selector_all(Selectors.INVITATION_CARD)
        logging.info(f"Found {len(invitations)} pending invitations.")

        for inv in invitations:
            try:
                name = inv.query_selector(Selectors.NAME_SELECTOR).inner_text().strip()
                profile_link_el = inv.query_selector(Selectors.PROFILE_LINK_SELECTOR)
                profile_url = f"https://www.linkedin.com{profile_link_el.get_attribute('href')}"
                
                headline_el = inv.query_selector(Selectors.HEADLINE_SELECTOR_1)
                headline = headline_el.inner_text().strip() if headline_el else ""

                mutual_el = inv.query_selector(Selectors.MUTUAL_CONNECTIONS_SELECTOR)
                mutual_connections = mutual_el.inner_text().strip() if mutual_el else "0"

                profiles.append({
                    "name": name,
                    "profile_url": profile_url,
                    "headline": headline,
                    "mutual_connections": mutual_connections
                })
            except Exception as e:
                logging.warning(f"Could not parse an invitation card. Error: {e}")

        return profiles

    def accept_filtered_requests(self, filtered_profile_urls):
        if not self.page or not filtered_profile_urls:
            return 0

        logging.info(f"Attempting to accept {len(filtered_profile_urls)} invitations.")
        self.page.goto(Selectors.MY_NETWORK_URL, timeout=60000)
        self._scroll_to_bottom()

        accepted_count = 0
        invitations = self.page.query_selector_all(Selectors.INVITATION_CARD)

        for inv in invitations:
            profile_link_el = inv.query_selector(Selectors.PROFILE_LINK_SELECTOR)
            if not profile_link_el:
                continue

            profile_url = f"https://www.linkedin.com{profile_link_el.get_attribute('href')}"
            if profile_url in filtered_profile_urls:
                try:
                    accept_button = inv.query_selector(Selectors.INVITATION_CARD_ACCEPT_BTN)
                    if accept_button:
                        accept_button.click()
                        logging.info(f"Accepted invitation for: {profile_url}")
                        accepted_count += 1
                        self._human_delay(0.5, 1.5)
                except Exception as e:
                    logging.error(f"Failed to accept invitation for {profile_url}. Error: {e}")

        logging.info(f"Successfully accepted {accepted_count} invitations.")
        return accepted_count

    def _scroll_to_bottom(self):
        logging.info("Scrolling to load all content...")
        last_height = self.page.evaluate("document.body.scrollHeight")
        while True:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self._human_delay(2, 4)
            new_height = self.page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        logging.info("Finished scrolling.")

    def __enter__(self):
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_browser()