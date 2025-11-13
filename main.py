import os
import sys
from dotenv import load_dotenv
from login import get_session_key
from get_metadata import get_metadata
from post_readout import post_readout


def main(readout_kwh):
    """
    Main function to:
    1. Get session key
    2. Get metadata (vkont, sernr, selected_read)
    3. Post meter readout
    
    Args:
        readout_kwh (int or str): The meter reading in kWh
    """
    # Load environment variables
    load_dotenv()
    
    main_url = "https://eam.mein-portal.de/swp/eam/main.do"
    
    # Step 1: Get session key
    print("Step 1: Getting session key...")
    user = os.getenv("user")
    pwd = os.getenv("pwd")
    
    if not user or not pwd:
        raise ValueError("Environment variables 'user' and 'pwd' must be set in .env file")
    
    session_key = get_session_key(main_url, user, pwd)
    print(f"✓ Session Key obtained: {session_key}")
    
    # Step 2: Get metadata
    print("\nStep 2: Getting metadata...")
    metadata = get_metadata(session_key=session_key)
    print("✓ Metadata obtained:")
    print(f"  - selected_read: {metadata['selected_read']}")
    print(f"  - vkont: {metadata['vkont']}")
    print(f"  - sernr: {metadata['sernr']}")
    
    # Step 3: Post readout
    print(f"\nStep 3: Posting meter readout ({readout_kwh} kWh)...")
    success = post_readout(session_key, metadata, readout_kwh)
    
    if success:
        print(f"✓ Successfully posted readout: {readout_kwh} kWh")
        return True
    else:
        print("✗ Failed to post readout")
        return False


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
