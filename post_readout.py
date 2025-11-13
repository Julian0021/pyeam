import requests
from datetime import date
from get_metadata import get_metadata

main_url = "https://eam.mein-portal.de/swp/eam/main.do"

def post_readout(session_key, metadata, readout_kwh: int):
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
    
    if not metadata.get('vkont') or not metadata.get('sernr') or not metadata.get('selected_read'):
        raise ValueError("Required metadata not found")
    
    # Prepare the form data for posting readout
    today = date.today().isoformat()
    
    files = {
        'oninputprocessing': (None, 'METER$SICHERN'),
        'p': (None, 'EAM'),
        'sessionkey': (None, session_key),
        'timeout': (None, '86400000 '),
        'abl_000000000010323427_001_datum': (None, today),
        'abl_000000000010323427_001_ablesungV': (None, str(readout_kwh)),
        'vkont': (None, metadata['vkont']),
        'sernr': (None, metadata['sernr']),
        'selected_read': (None, metadata['selected_read'])
    }
    
    
    # Make the POST request
    response = requests.post(main_url, files=files)
    response.raise_for_status()

    return response.status_code == 200


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python post_readout.py <readout_kwh>")
        print("Example: python post_readout.py 449")
        sys.exit(1)
    
    readout_value = sys.argv[1]
    
    try:
        success = post_readout(readout_value, get_metadata())
        if success:
            print(f"Successfully posted readout: {readout_value} kWh")
        else:
            print("Failed to post readout")
    except Exception as e:
        print(f"Error: {e}")