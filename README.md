Installation:
1. Clone the repo
2. Create a bot user if you don't have one yet, and copy the API Token
3. export SLACK_BOT_TOKEN="your-api-token"
4. export BOT_ID="your-bot-id"
5. Change aws_access_key_id and aws_secret_access_key in jasper.py
6. Invite jasper into the channel

Prerequisites:
1. Python 2+
2. pip install <module> (slackclient, boto)

Commands:
It's easy to add your own commands! Create another loop or add a function to make it work. You can use boto module for managing AWS

The commands supported are:
1. help (shows the command supported)
2. list (lists the instances currently running in EC2)
3. create <instance_id> (create new EC2 instance)
4. shutdown <instance_id> (stops EC2 instance)
5. delete <instance_id> (terminates EC2 instance)

Author:
@taufique786
