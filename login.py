import requests
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_session_key(url, user, pwd):
    """
    Login to the service and extract the session key from the HTML response.

    Args:
        url (str): The login endpoint URL

    Returns:
        str: The session key extracted from the HTML response

    Raises:
        ValueError: If credentials are not set or session key is not found
        requests.RequestException: If the HTTP request fails
    """

    # Prepare the multipart form data
    params = {
        "oninputprocessing": (None, "LOGIN$LOGIN"),
        "p": (None, "EAM"),
        "timeout": (None, "86400000"),
        "user": (None, user),
        "passwd": (None, pwd),
    }

    # Make the POST request with multipart/form-data
    response = requests.post(url, params=params)
    response.raise_for_status()

    # Extract session key from HTML using regex
    # Looking for: <input type='text' id="sessionkey" name='input' style='display:none' value='...' />
    pattern = r'<input[^>]*id=["\']sessionkey["\'][^>]*value=["\']([A-F0-9]+)["\']'
    match = re.search(pattern, response.text, re.IGNORECASE)

    if not match:
        raise ValueError("Session key not found in response")

    session_key = match.group(1)
    return session_key


if __name__ == "__main__":
    # Example usage
    login_url = "https://eam.mein-portal.de/swp/eam/main.do"

    try:
        session_key = get_session_key(login_url)
        print(f"Session key: {session_key}")
    except Exception as e:
        print(f"Error: {e}")
