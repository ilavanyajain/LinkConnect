from playwright.sync_api import sync_playwright
import time
import random
import os

LOGIN_URL = "https://www.linkedin.com/login"
MY_NETWORK_URL = "https://www.linkedin.com/mynetwork/invitation-manager/"

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_pending_requests(self):
        def safe_inner_text(element):
            try:
                return element.inner_text().strip() if element else ""
            except:
                return ""

        profiles = []
        with sync_playwright() as p:
            print("[DEBUG] Launching Chromium browser...")
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = browser.new_context()
            page = context.new_page()
            print("[DEBUG] Navigating to LinkedIn login page...")
            page.goto(LOGIN_URL)
            print("[DEBUG] Filling in email...")
            page.fill('input[name="session_key"]', self.email)
            print("[DEBUG] Filling in password...")
            page.fill('input[name="session_password"]', self.password)
            print("[DEBUG] Clicking login button...")
            page.click('button[type="submit"]')
            print("[DEBUG] Waiting for search input (post-login)...")
            page.wait_for_selector('input[placeholder="Search"]', timeout=120000)
            print("[DEBUG] Login successful, navigating to My Network...")

            while "feed" not in page.url:
                print("Waiting for user to complete login/2FA...")
                time.sleep(2)

            page.goto(MY_NETWORK_URL, timeout=120000)
            page.wait_for_selector('li.invitation-card', timeout=120000)

            previous_height = 0
            while True:
                page.mouse.wheel(0, 10000)
                time.sleep(1)
                current_height = page.evaluate("document.body.scrollHeight")
                if current_height == previous_height:
                    break
                previous_height = current_height

            requests = page.query_selector_all('li.invitation-card')
            for req in requests:
                # Name & Profile URL
                name_elem = req.query_selector('strong > a')
                name = safe_inner_text(name_elem)
                profile_url = name_elem.get_attribute('href') if name_elem else ""
                profile_url = f"https://www.linkedin.com{profile_url}" if profile_url and profile_url.startswith('/') else profile_url

                # --- Headline robust extraction ---
                headline = ""
                headline_selectors = [
                    'div.invitation-card__subtitle',
                    'span.invitation-card__subtitle',
                    'div.invitation-card_subtitle',
                    'span.entity-result__primary-subtitle',
                ]
                for selector in headline_selectors:
                    headline_elem = req.query_selector(selector)
                    if headline_elem:
                        headline = safe_inner_text(headline_elem)
                        if headline:
                            break
                if not headline:
                    try:
                        headline = req.inner_text().replace(name, '').strip()
                    except Exception:
                        headline = ""
                # --- End headline robust extraction ---

                # Mutual Connections
                mutual_elem = req.query_selector('div.member-insights span[dir="ltr"]')
                mutual = safe_inner_text(mutual_elem)

                profiles.append({
                    "name": name,
                    "profile_url": profile_url,
                    "headline": headline,
                    "mutual_connections": mutual
                })
            browser.close()
        return profiles

    def accept_request(self, url_list):
        print(f"Starting accept_request with {len(url_list)} profile URLs (profile page method)")
        from playwright.sync_api import TimeoutError

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            page.set_default_timeout(30000)

            def human_delay():
                time.sleep(1 + random.random() * 2)

            # Login
            print("Attempting to login...")
            page.goto(LOGIN_URL)
            human_delay()
            page.fill('input[name="session_key"]', self.email)
            human_delay()
            page.fill('input[name="session_password"]', self.password)
            human_delay()
            page.click('button[type="submit"]')
            try:
                page.wait_for_selector('input[placeholder="Search"]', timeout=120000)
                while "feed" not in page.url:
                    print("Waiting for user to complete login/2FA...")
                    time.sleep(2)
            except Exception as e:
                print(f"Error during login: {str(e)}")
                browser.close()
                return 0

            print("Login successful, starting to process profiles...")

            accepted = 0
            for profile_url in url_list:
                print(f"Visiting profile: {profile_url}")
                try:
                    page.goto(profile_url, timeout=60000)
                    human_delay()
                    # Try several selectors for the Accept button
                    accept_btn = None
                    for selector in [
                        'button:has-text("Accept")',
                        'button[aria-label^="Accept"]',
                        'button[data-control-name="accept"]',
                        'button.artdeco-button--primary'
                    ]:
                        try:
                            accept_btn = page.query_selector(selector)
                            if accept_btn and accept_btn.is_visible() and 'accept' in accept_btn.inner_text().lower():
                                break
                        except Exception:
                            continue
                    if accept_btn and accept_btn.is_visible():
                        print(f"Found Accept button on {profile_url}, clicking...")
                        accept_btn.scroll_into_view_if_needed()
                        human_delay()
                        box = accept_btn.bounding_box()
                        if box:
                            page.mouse.move(
                                box['x'] + box['width']/2,
                                box['y'] + box['height']/2
                            )
                            human_delay()
                        accept_btn.click()
                        time.sleep(3)
                        accepted += 1
                        print(f"Accepted: {profile_url}")
                    else:
                        print(f"No Accept button found on {profile_url}")
                except TimeoutError:
                    print(f"Timeout visiting {profile_url}")
                except Exception as e:
                    print(f"Error processing {profile_url}: {str(e)}")
            print(f"Accepted {accepted} connection requests via profile pages.")
            browser.close()
            return accepted