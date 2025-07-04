import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, send_from_directory
from linkedin_bot import LinkedInBot
import re
import logging

# Set the browser path for Playwright
if os.environ.get("VERCEL"):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/var/task/browser"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_folder='../public', static_url_path='')

def safe_mutual_count(mc_string):
    """Safely extracts the number of mutual connections from a string."""
    numbers = re.findall(r'\d+', mc_string)
    return int(numbers[0]) if numbers else 0

def filter_profiles(profiles, headline_keywords, min_mutual):
    """Filters profiles based on headline keywords and minimum mutual connections."""
    if not isinstance(profiles, list):
        logging.error(f"Expected a list of profiles, but got {type(profiles)}")
        return []

    filtered_list = []
    for p in profiles:
        headline = p.get('headline', '').lower()
        mutual_count = safe_mutual_count(p.get('mutual_connections', '0'))
        
        keyword_match = not headline_keywords or any(kw.lower() in headline for kw in headline_keywords)
        mutual_match = mutual_count >= min_mutual
        
        if keyword_match and mutual_match:
            filtered_list.append(p)
            
    return filtered_list

@app.route('/api/linkedin', methods=['POST'])
def handle_linkedin_action():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    action = data.get('action')
    email = data.get('email', os.getenv('LINKEDIN_EMAIL'))
    password = data.get('password', os.getenv('LINKEDIN_PASSWORD'))

    if not all([action, email, password]):
        return jsonify({"error": "Missing required parameters: action, email, password"}), 400

    bot = LinkedInBot(email, password)
    
    try:
        bot.start_browser(headless=True)
        if not bot.login():
            return jsonify({"error": "Login failed. Check credentials or solve 2FA/CAPTCHA."}), 401

        if action == 'fetch':
            profiles = bot.get_pending_requests()
            return jsonify({"profiles": profiles, "count": len(profiles)})

        elif action == 'accept':
            headline_keywords = data.get('headline_keywords', [])
            min_mutual = data.get('min_mutual', 0)
            
            all_profiles = bot.get_pending_requests()
            
            filtered_profiles = filter_profiles(all_profiles, headline_keywords, min_mutual)
            
            urls_to_accept = [p['profile_url'] for p in filtered_profiles]
            
            if not urls_to_accept:
                return jsonify({"message": "No profiles matched the criteria. Nothing to accept."}), 200

            accepted_count = bot.accept_filtered_requests(urls_to_accept)
            return jsonify({
                "message": f"Accepted {accepted_count} connection requests.",
                "accepted_count": accepted_count,
                "total_matched": len(urls_to_accept)
            })

        else:
            return jsonify({"error": "Invalid action specified."}), 400

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
        
    finally:
        bot.close_browser()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/debug-list-public')
def debug_list_public():
    try:
        return str(os.listdir(os.path.join(os.getcwd(), 'public')))
    except Exception as e:
        return f"Error: {e}"

@app.route('/debug-docker-paths')
def debug_docker_paths():
    try:
        root_files = os.listdir('/app')
        public_files = os.listdir('/app/public') if os.path.exists('/app/public') else 'NO PUBLIC DIR'
        return f"WORKDIR: {os.getcwd()}<br>/app: {root_files}<br>/app/public: {public_files}"
    except Exception as e:
        return f"Error: {e}"

# This is for local development, Vercel will use its own server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True) 