import requests
from datetime import date

main_url = "https://eam.mein-portal.de/swp/eam/main.do"

def post_readout(session_key, selected_read, readout_kwh: int):
    """
    Post meter readout to the EAM portal.
    
    Args:
        readout_kwh (int or str): The meter reading in kWh
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If session key or metadata is not found
        requests.RequestException: If the HTTP request fails
    """
    if readout_kwh < 0:
        raise ValueError("Readout must be a non-negative integer value")

    if not selected_read:
        raise ValueError("Selected read value is required")
    
    # Prepare the form data for posting readout
    today = date.today().isoformat()
    
    files = {
        'oninputprocessing': (None, 'METER$SICHERN'),
        'p': (None, 'EAM'),
        'sessionkey': (None, session_key),
        'timeout': (None, '1800000'),
        'abl_000000000010323427_001_datum': (None, today),
        'abl_000000000010323427_001_ablesungV': (None, str(readout_kwh)),
        'selected_read': (None, selected_read)
    }
    
    
    # Make the POST request
    response = requests.post(main_url, files=files)
    response.raise_for_status()

    return response.status_code == 200