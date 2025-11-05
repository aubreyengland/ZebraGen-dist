
# ZebraGen

## Overview

**ZebraGen** is a command-line utility for exporting third-party SIP device credentials from Zoom Phone and formatting them for use with the Zebra Extension Manager. It automates the retrieval of “Other” device provisioning data (SIP credentials) via the Zoom API, applies H-E-B–specific site and department naming conventions, and outputs a ready-to-import CSV file.

## Features

- Authenticates with the Zoom API using Server-to-Server OAuth credentials
- Retrieves all “Other” device types (e.g., Zebra devices) from Zoom Phone
- Extracts SIP credentials and other relevant provisioning data
- Applies custom site and department naming conventions
- Outputs a CSV file in the format required by Zebra Extension Manager (45 columns)
- Supports filtering by Zoom site name
- Handles department and site name lookups via local JSON files

## Requirements

- Python 3.7+
- Zoom account with API access and Server-to-Server OAuth app credentials
- `dept_info.json` and `site_info.json` files for department/site lookups
- (Optional) `.env` file for storing Zoom API credentials

## Usage

```bash
python zebra_gen.py --site "<Zoom Site Name>" [--site-list <site_list.xlsx>] [--output <output.csv>]
```

- `--site` (required): The Zoom site name to filter devices (e.g., `"Main Site"`)
- `--output`: Output CSV file name (default: `sip_credentials.csv`)

### Example

```bash
python zebra_gen.py --site "CORP 195"
```

## Dependencies

- `requests`
- `pandas`
- `python-dotenv`
- `zebra_gen_client` (included custom Zoom API client)

You can install dependencies via:

```bash
pip install -r requirements.txt
```

## Output Format

The output is a CSV file with **45 columns**, matching the Zebra Extension Manager import format. Columns include:

- `site_name`, `site_info`, `site_multi`, `dep_name`, `dep_info`, `dep_auto`, `dep_hidden`, `dep_reserved`, `dep_threshold`, `dep_role`, `dep_role_desc`, `dep_code`, `number`, `ext_name`, `ext_info`, `second_pbx_params`, `reserved_uid`, `pbx_name`, `profile_type`, `sip_remhost`, `sip_sipid`, `sip_userid`, `sip_mac`, `sip_userpass`, `site_config`, `dep_config`, `ext_config`, `sip_pbx_logo`, `sip_device_type`, `sip_transport`, `sip_remport`, `sip_remhost2`, `sip_remhost3`, `sip_localport`, `sip_realm`, `sip_vmnum`, `sip_parknum`, `sip_confnum`, `sip_http_remhost`, `sip_srtp`, `sip_outboundproxy`, `sip_linenumber`, `sip_lineaddress`, `sip_conferenceid`, `sip_conferenceuri`

## Example Output Command

```bash
python zebra_gen.py --site "CORP 195" --output "zebra_195.csv"
```

## Notes

- IMPORTANT: Only devices of type "other" (i.e., Zebra devices) whose display names end with `-W` are included in the output.
- Make sure to set the following environment variables (either in your shell or in a `.env` file in the project directory):
    - `ZOOM_S2S_ACCOUNT_ID`
    - `ZOOM_S2S_CLIENT_ID`
    - `ZOOM_S2S_CLIENT_SECRET`
- Ensure `dept_info.json` and `site_info.json` are present in the working directory for department and site lookups.
- The script logs progress and errors to the console.
- For more details, review or modify the `zebra_gen.py` source code.