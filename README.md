# pyeam

Python automation tool for posting meter readouts to EAM-Netz portal.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file in the project root:
```env
user=your_username
pwd=your_password
```

## Usage

```bash
python main.py <readout_kwh>
```

**Example:**
```bash
python main.py 449
```

## How it works

The tool performs the following steps:

1. **Authentication** - Logs in and retrieves session key
2. **Get metadata** - Fetches selected_read value
3. **Get last readout** - Retrieves the last submitted meter reading
4. **Post readout** - Submits the new meter reading
5. **Verification** - Confirms the readout was posted correctly

## Project Structure

- `main.py` - Main script and CLI interface
- `eam_api.py` - API functions for EAM portal interaction
  - `get_session_key()` - Authentication
  - `get_selected_read()` - Fetch meter metadata
  - `get_last_readout()` - Retrieve last reading
  - `post_readout()` - Submit new reading
- `.env` - Environment variables (credentials)
- `requirements.txt` - Python dependencies
