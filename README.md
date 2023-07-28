## Overview
By using this, you can accomplish the following:
1. You can export a list of channels existing within the workspace to a CSV file.
1. By utilizing the CSV file exported in step 1, you can bulk rename channel names.

## Getting Started
### Setting Environment Variables
Set the User OAuth Token to the SLACK_API_TOKEN variable.<br>
Please issue the User OAuth Token from the following URL:https://api.slack.com/apps<br>
※ The required scopes are as follows:
- channels:read
- channels:write

### 1. Installing the Library
- `$ pip3 install -r requirements.txt`

### 2. Outputting Channel List
- `$ python3 slack_rename.py -l`

### 3. Renaming Channels
1. Open the CSV file and enter the new channel names in the "NewChannelName" column
1. `$ python3 slack_rename.py -r`