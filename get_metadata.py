import requests
import re


def get_selected_read(session_key=None):
    """
    Get meter metadata from the EAM portal.
    
    Returns:
        dict: Dictionary containing 'selected_read', 'vkont', and 'sernr' values.
              Returns None for any value that couldn't be found.
    
    Raises:
        ValueError: If session key is not found or credentials are not set
        requests.RequestException: If the HTTP request fails
    """
    # Login URL
    main_url = "https://eam.mein-portal.de/swp/eam/main.do"
    
    
    # Make the POST request with the session key
    params = {
        'oninputprocessing': (None, 'menu$METER'),
        'p': (None, 'EAM'),
        'sessionkey': (None, session_key)
    }

    post_response = requests.post(main_url, params=params)
    post_response.raise_for_status()
    
    html = post_response.text
    
    # Extract selected_read value using regex
    # Looking for: <option value="..." selected >
    selected_read_value = None
    selected_pattern = r'<option[^>]*value=["\']([^"\']+)["\'][^>]*selected[^>]*>'
    match = re.search(selected_pattern, html, re.IGNORECASE)
    if match:
        selected_read_value = match.group(1)
    
    return selected_read_value
