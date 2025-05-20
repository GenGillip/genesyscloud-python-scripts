# genesyscloud-python-scripts
Common python scripts that I have built


config.js
Each python app uses the config.js in the same directory to be able to authenticate with the Genesys Cloud Org.  The SDK uses Client Credentials configuration, if you need help creating the oAuth, that can be found here --> https://developer.genesys.cloud/authorization/platform-auth/guides/oauth/module-1-client-credentials.
You also need to know the URL Region your org is in, example is mypurecloud.com or usw2.pure.cloud.  The full list can be found here --> https://developer.genesys.cloud/platform/api/


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
    "orgName": "your-org-name"
}
```

Replace:
- `your-client-id` with your Genesys Cloud OAuth client ID
- `your-client-secret` with your Genesys Cloud OAuth client secret
- `your-region-domain` with your Genesys Cloud region domain (e.g., `mypurecloud.com`, `usw2.pure.cloud`, etc.)
- `your-org-name` with your organization name ** NOT Required **

## Usage

### Windows

1. Navigate to the script directory in Command Prompt or PowerShell:
   ```
   cd path\to\project
   ```

2. Run the script:
   ```
   python main.py
   ```

### macOS

1. Navigate to the script directory in Terminal:
   ```
   cd path/to/project
   ```

2. Run the script:
   ```
   python3 main.py
   ```

## Troubleshooting

If you encounter authentication issues:
- Verify your client credentials are correct
- Ensure your OAuth client has the required permissions
- Check that you've specified the correct region

For other issues, check the console output for error messages.