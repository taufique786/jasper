<h3>Installation:</h3>
<ol>
<li> Clone the repo </li>
<li> Create a bot user if you don't have one yet, and copy the API Token </li>
<li> export SLACK_BOT_TOKEN="your-api-token" </li>
<li> export BOT_ID="your-bot-id" </li>
<li> Run bot_id.py to get the BOT_ID </li>
<li> Change aws_access_key_id and aws_secret_access_key in jasper.py </li>
<li> Invite jasper into the channel </li>
</ol>

<h3>Prerequisites:</h3>
<ol>
<li> Python 2+ </li>
<li> pip install <module> (slackclient, boto) </li>
</ol>

<h3>Commands:</h3>
It's easy to add your own commands! Create another loop or add a function to make it work. You can use boto module for managing AWS

<h3>The commands supported are:</h3>
<ol>
<li> help (shows the command supported) </li>
<li> list (lists the instances currently running in EC2) </li>
<li> create <instance_id> (create new EC2 instance) </li>
<li> shutdown <instance_id> (stops EC2 instance) </li>
<li> delete <instance_id> (terminates EC2 instance) </li>
</ol>

<h3>Author:</h3>
@taufique786

