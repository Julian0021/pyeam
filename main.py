import os
import sys
from dotenv import load_dotenv
from eam_api import get_session_key, get_selected_read, post_readout, get_last_readout

load_dotenv()


def main(readout_kwh):
    """
    Main function to:
    1. Get session key
    2. Get metadata (selected_read)
    3. Post meter readout
    
    Args:
        readout_kwh (int or str): The meter reading in kWh
    """
    # Load environment variables
    user = os.getenv("user")
    pwd = os.getenv("pwd")

    main_url = "https://eam.mein-portal.de/swp/eam/main.do"
    
    print("Step 1: Getting session key...")

    if not user or not pwd:
        raise ValueError("Environment variables 'user' and 'pwd' must be set in .env file")
    
    session_key = get_session_key(main_url, user, pwd)
    print(f"✓ Session Key obtained: {session_key}")
    
    print("\nStep 2: Getting selected read...")
    selected_read = get_selected_read(session_key, main_url)
    print(f"✓ Selected Read obtained: {selected_read}")
    
    print("\nStep 3: Getting last readout...")
    last_readout = get_last_readout(session_key, main_url)
    print(f"✓ Last Readout obtained: {last_readout['value']} kWh on date {last_readout['date']}")
    
    print("\nStep 4: Posting readout...")
    success = post_readout(session_key, selected_read, readout_kwh, main_url)
    if success:
        print(f"✓ Successfully posted readout: {readout_kwh} kWh")
    else:
        print("✗ Failed to post readout")

    print("\nStep 5: Verify the readout on the EAM portal to ensure it was posted correctly.")
    if get_last_readout(session_key, main_url) == str(readout_kwh):
        print("✓ Readout verification successful.")
    else:
        print("✗ Readout verification failed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <readout_kwh>")
        print("Example: python main.py 449")
        sys.exit(1)

    readout_value = int(sys.argv[1])

    try:
        success = main(readout_value)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
