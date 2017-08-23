#!/usr/bin/python
import os
import time
import re
import boto.ec2
from slackclient import SlackClient

# Jasper's ID as an environment variable. You need to add BOT_ID in your environmental variable by running 'export BOT_ID='
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
CREATE_INSTANCE = "create instance"
TERMINATE_INSTANCE = "delete instance"
SHUTDOWN_INSTANCE = "shutdown instance"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Takes command from slack and responses back if the command is valid
    """
    conn = boto.ec2.connect_to_region("us-west-2", aws_access_key_id='AKIAJ4NPEM7LESTMM5TQ',
                                      aws_secret_access_key='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')
    response = "Try using " + "\n" + CREATE_INSTANCE + "\n" + TERMINATE_INSTANCE + "\n" + SHUTDOWN_INSTANCE
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    # Creating EC2 Instance
    if command.startswith(CREATE_INSTANCE):
        conn.run_instances('ami-f87c9080', key_name='devops', instance_type='t2.small',
                           security_groups=['launch-wizard-1'])
        create_instance = "Creating new instance now"
        slack_client.api_call("chat.postMessage", channel=channel, text=create_instance, as_user=True)

    # Shutting down EC2 Instance
    elif command.startswith(SHUTDOWN_INSTANCE):
        shutdown = "Please select the instance_id"
        slack_client.api_call("chat.postMessage", channel=channel, text=shutdown, as_user=True)
        reservations = conn.get_all_reservations()
        for reservation in reservations:
            slack_client.api_call("chat.postMessage", channel=channel, text=reservation.instances, as_user=True)
        # if command.startswith(i):
        #     conn.stop_instances(instance_ids=i)
        #     stop_instance = "Stopping instance"
        #     slack_client.api_call("chat.postMessage", channel=channel, text=stop_instance, as_user=True)

    # Terminating EC2 Instance
    elif command.startswith(TERMINATE_INSTANCE):
        terminate = "Please enter the instance_id"
        slack_client.api_call("chat.postMessage", channel=channel, text=terminate, as_user=True)
        i = ''
        if command.startswith(i):
            conn.terminate_instances(instance_ids=i)
            del_instance = "Deleting instance"
            slack_client.api_call("chat.postMessage", channel=channel, text=del_instance, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Jasper connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
