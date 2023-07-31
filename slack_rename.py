import os
import csv
import argparse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def get_args():
    parser = argparse.ArgumentParser(description='Command line options for this script')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list', action='store_const', const='list', help='Create a CSV list of all Slack channels')
    group.add_argument('-r', '--rename', action='store_const', const='rename', help='Rename Slack channels based on a CSV')
    return parser.parse_args()

def create_csv():
    data_to_file = open("ChannelList.csv", 'w', newline='')
    csv_writer = csv.writer(data_to_file, delimiter=',')
    return csv_writer

def append_csv():
    data_to_file = open("ChannelList.csv", 'a', newline='')
    csv_append = csv.writer(data_to_file, delimiter=',')
    return csv_append

def create_web_client(slack_token):
  return WebClient(token=slack_token)

def fetch_channel_list(client):
  try:
    response = client.conversations_list()
    return response["channels"]

  except SlackApiError as e:
    print(f"slack api error: {e.response['error']}")

def create_channel_list(slack_token):
  client = create_web_client(slack_token)
  channel_list =  fetch_channel_list(client)
  create_csv().writerow(['ChannelID', 'ChannelName', 'NewChannelName'])
  for i in range(0,len(channel_list)):
    channnel_id = channel_list[i]['id']
    channnel_name = channel_list[i]['name']
    append_csv().writerow([channnel_id, channnel_name, ''])

def rename_channnels(slack_token):
  client = create_web_client(slack_token)
  with open("ChannelList.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if not row['NewChannelName'] == "":
        try:
          response = client.conversations_rename(
            token=slack_token,
            channel=row['ChannelID'],
            name=row['NewChannelName']
          )
          if response["ok"]:
            print(f"The channel name has been renamed to {row['NewChannelName']}")
          else:
            print(f"The channel renaming has failed. Error message: {response['error']}")
        except SlackApiError as e:
          print(f"slack api error: {e.response['error']}")


def main():
  args = get_args()
  slack_token = os.environ["SLACK_API_TOKEN"]
  print(slack_token)
  if not slack_token:
    print("Slack API token is not set. Please set the token in the environment variable SLACK_API_TOKEN")
  
  if args.list == 'list':
    print('Downloading Slack channel list into ChannelList.csv')
    create_channel_list(slack_token)
  elif args.rename == 'rename':
    print('Renaming Slack channels based on ChannelList.csv')
    rename_channnels(slack_token)
  

if __name__ == "__main__":
    main()
