# pyeam

Python automation tool for posting meter readouts to EAM-Netz portal.

## Setup

1. Install dependencies:
```bash
pip install requests python-dotenv
```

2. Create `.env` file:
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

1. Authenticates and retrieves session key
2. Fetches metadata (vkont, sernr, selected_read)
3. Posts meter readout to the portal
