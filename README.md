# LinkConnect (Render Edition)

**LinkConnect** is a tool to automate and filter LinkedIn connection requests using Playwright and Flask. This version is designed for deployment on [Render](https://render.com/).

---

## Features

- **Web-Based UI:** A clean and modern user interface built with standard HTML, CSS, and JavaScript.
- **Serverless Backend:** Powered by Flask, designed to run as a serverless function for scalability and cost-efficiency.
- **Efficient Automation:** Uses a refactored Playwright-based bot for faster and more reliable LinkedIn interactions.
- **Direct Connection Acceptance:** Accepts requests directly from the network page, avoiding slow and risky profile visits.
- **Dynamic Filtering:** Filter pending requests in real-time by headline keywords and the number of mutual connections.
- **Secure:** Credentials are handled for each session and are not stored. For production, environment variables are recommended.
- **Deployable on Render (persistent, no serverless limits):**

---

## Architecture

LinkConnect now uses a modern web architecture:

- **Frontend:** A static single-page application located in the `/public` directory. It is built with HTML, CSS, and vanilla JavaScript.
- **Backend:** A Flask API located in the `/api` directory. It's designed to be deployed as a single serverless function (`index.py`) that controls the `LinkedInBot`.
- **Bot:** The core automation logic is encapsulated in `linkedin_bot.py`, which is now more robust and efficient.

This architecture is optimized for deployment on **Render**.

---

## Local Development

### Prerequisites

- Python 3.8+
- [Playwright](https://playwright.dev/python/docs/intro)

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Then, install the necessary Playwright browser:

```bash
playwright install chromium
```

### 2. Set Up Environment Variables (Optional)

For convenience, you can create a `.env` file in the root of the project to store your LinkedIn credentials. This prevents you from having to type them into the UI every time.

```
LINKEDIN_EMAIL="your-email@example.com"
LINKEDIN_PASSWORD="your-password"
```

The application will automatically use these if the fields in the UI are left blank.

### 3. Run the Flask App

Start the local Flask development server:

```bash
flask run --port 5001
```

Or, more directly:

```bash
python3 api/index.py
```

*Note: Running `api/index.py` directly is often easier for local testing.*

### 4. Run a Local Server for the Frontend

Since the frontend and backend run on different ports locally, you need a simple HTTP server for the frontend.

Open a **new terminal window**, navigate to the `public` directory, and run:

```bash
cd public
python3 -m http.server 5000
```

### 5. Access the Application

Open your browser and go to **http://localhost:5000**. The frontend will make API calls to the Flask server running on port 5001.

---

## Deploying to Render

1. **Push your code to GitHub.**
2. **Create a new Web Service on Render:**
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Start Command: `python api/index.py`
   - (Optional) Set environment variables for secrets.
3. **Set the service to listen on port 10000 or `$PORT` (Render sets this automatically).**

---

## File Structure

```
.
├── api/
│   └── index.py            # Flask backend (Serverless Function)
├── public/
│   ├── index.html          # Frontend HTML
│   ├── style.css           # Frontend CSS
│   └── main.js             # Frontend JavaScript
├── linkedin_bot.py         # Core Playwright automation logic
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
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

---

## Notes
- Remove all Vercel-specific files/configs before deploying to Render.
- Playwright will download the browser on first build (see build command above).
- For persistent storage, use Render's disk or environment variables as needed.
