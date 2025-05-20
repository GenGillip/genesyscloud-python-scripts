# Genesys Cloud User Export Tool

This script exports Genesys Cloud users to a CSV file, including their basic information and group memberships.

## Prerequisites

- Python 3.6 or higher
- Genesys Cloud OAuth client credentials with appropriate permissions.

## Installation

### Windows

1. Install Git for Windows from [git-scm.com](https://git-scm.com/download/win) if not already installed
2. Open Command Prompt or PowerShell
3. Clone the repository:
   ```
   git clone https://github.com/yourusername/genesyscloud-python-scripts.git
   cd project
   ```
   
   Alternatively, download and extract the ZIP file from the repository

4. Install the required dependencies:
   ```
   pip install PureCloudPlatformClientV2
   ```

### macOS

1. Open Terminal
2. Install Git if not already installed (it's usually pre-installed on macOS):
   ```
   brew install git
   ```
   If you don't have Homebrew, install it first from [brew.sh](https://brew.sh/)

3. Clone the repository:
   ```
   git clone https://github.com/yourusername/genesyscloud-python-scripts.git
   cd project
   ```
   
   Alternatively, download and extract the ZIP file from the repository

4. Install the required dependencies:
   ```
   pip3 install PureCloudPlatformClientV2
   ```

## Configuration

Create a `config.json` file in the same directory as the script with the following structure:

```json
{
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret",
    "region": "your-region-domain",
    "orgName": "your-org-name" // orgName NOT mandatory
}
```

Replace:
- `your-client-id` with your Genesys Cloud OAuth client ID
- `your-client-secret` with your Genesys Cloud OAuth client secret
- `your-region-domain` with your Genesys Cloud region domain (e.g., `mypurecloud.com`, `usw2.pure.cloud`, etc.)
- `your-org-name` with your organization name

## Usage

### Windows

1. Navigate to the script directory in Command Prompt or PowerShell:
   ```
   cd path\to\export_users_csv_v2
   ```

2. Run the script:
   ```
   python main.py
   ```

### macOS

1. Navigate to the script directory in Terminal:
   ```
   cd path/to/export_users_csv_v2
   ```

2. Run the script:
   ```
   python3 main.py
   ```

The script will:
1. Authenticate with Genesys Cloud
2. Retrieve all groups in your organization
3. Retrieve all active users
4. Export user data to a CSV file named `Users_Output_YYYY-MM-DD_HH-MM-SS.csv`

## Troubleshooting

If you encounter authentication issues:
- Verify your client credentials are correct
- Ensure your OAuth client has the required permissions
- Check that you've specified the correct region

For other issues, check the console output for error messages.