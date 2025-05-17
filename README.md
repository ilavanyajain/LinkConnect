# LinkConnect Pro

**LinkConnect Pro** is a powerful tool for professionals who receive a high volume of LinkedIn connection requests. It allows you to efficiently filter, review, and analyze connection requests based on your own criteria, saving you time and helping you build a more relevant network.

---

## Features

- **Automated Login:** Securely log in to your LinkedIn account using your credentials.
- **Fetch Pending Requests:** Retrieve all your pending LinkedIn connection requests in one click.
- **Profile Filtering:** Filter requests by headline keywords and minimum number of mutual connections.
- **Profile Data Table:** View all pending requests in a sortable, filterable table with names, profile URLs, headlines, and mutual connections.
- **Robust Headline Extraction:** Extracts professional headlines from each profile for better filtering.
- **Human-like Automation:** Uses Playwright with anti-bot measures for more reliable automation.
- **Modern UI:** Built with Streamlit for a clean, interactive, and responsive user experience.

---

## How It Works

1. **Login:** Enter your LinkedIn email and password (credentials are not stored).
2. **Fetch Requests:** Click "Fetch Pending Requests" to retrieve all your pending connection requests.
3. **Filter:** Use the filter options to narrow down requests by headline keywords and/or minimum mutual connections.
4. **Review:** Browse the filtered list, including names, profile URLs, professional headlines, and mutual connections.

---

## Tech Stack

- **Python 3.8+**: The core programming language for the backend logic and automation.
- **Streamlit**: Provides the interactive web-based user interface for the app, allowing users to input credentials, set filters, and view results in real time.
- **Playwright**: Automates browser actions to log in to LinkedIn and fetch pending connection requests, simulating human-like behavior to avoid detection.
- **Pandas**: Used for data manipulation and display, especially for filtering and presenting the connection requests in a table format.

---

## Technical Functionality

- The app launches a browser session using Playwright, navigates to LinkedIn, and logs in with the provided credentials.
- It navigates to the LinkedIn invitation manager and scrapes all pending connection requests, extracting names, profile URLs, professional headlines, and mutual connections.
- The data is loaded into a Pandas DataFrame for easy filtering and display.
- Users can filter the requests by keywords in the headline and by the minimum number of mutual connections.
- The filtered results are displayed in a table within the Streamlit UI, allowing users to review and analyze their pending requests efficiently.
- **Note:** Due to LinkedIn's anti-automation measures and recent changes, the app does not support automated acceptance of connection requests. It is designed for review and analysis only.

---

## Installation

### Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

### Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### `requirements.txt`

```
streamlit
playwright
pandas
```

---

## Usage

1. **Start the app:**

   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**  
   Go to the local URL provided by Streamlit (usually http://localhost:8501).

3. **Login and use the app:**  
   - Enter your LinkedIn credentials.
   - Fetch pending requests.
   - Filter and review.

---

## Security & Privacy

- **Credentials:** Your LinkedIn credentials are used only for the session and are not stored.
- **Automation:** The app uses Playwright to automate browser actions. It does not store or transmit your data anywhere.
- **Disclaimer:** Use this tool responsibly and in accordance with LinkedIn's terms of service. Excessive automation may result in account restrictions.

---

## File Structure

```
.
├── app.py                  # Streamlit app UI and logic
├── linkedin_bot.py         # Playwright automation for LinkedIn
├── filters.py              # Filtering logic (if separated)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Customization

- **Headline Extraction:** The app uses multiple selectors to robustly extract professional headlines from each profile.
- **Filtering Logic:** You can adjust the filtering logic in `filters.py` or directly in `app.py` to suit your needs.
- **Selectors:** If LinkedIn changes its DOM, update the selectors in `linkedin_bot.py`.

---

## Troubleshooting

- **Login Issues:** If you have 2FA enabled, complete it manually in the browser window that opens.
- **No Requests Fetched:** Ensure you have pending requests and that your credentials are correct.
- **Automation Not Working:** LinkedIn may change its UI or block automation. Update selectors or try running in headless mode off.
- **Missing Headlines:** If some headlines are missing, update the selectors in `linkedin_bot.py`.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is for personal use and educational purposes. Use at your own risk.

---

## Disclaimer

This tool is not affiliated with or endorsed by LinkedIn. Use responsibly and at your own risk. Excessive automation may violate LinkedIn's terms of service.

---

## Author

Developed by Lavanya J.  
For questions or support, open an issue or contact me. 