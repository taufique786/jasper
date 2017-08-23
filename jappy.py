#!/usr/bin/python
import re
import time
import json
import psutil
import os
import boto.ec2
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

bot_id = os.environ.get("BOT_ID")

# Start connection
if slack_client.rtm_connect():
    print "Jasper connected and running"

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % bot_id):

                print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text']. \
                    split("<@%s>" % bot_id)[1]. \
                    strip()

                conn = boto.ec2.connect_to_region("us-west-2", aws_access_key_id='AKIAJ4NPEM7LESTMM5TQ',
                                                  aws_secret_access_key='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')

                # Create EC2 Instance
                if re.match(r'.*(create).*', message_text, re.IGNORECASE):
                    if 'ami-' not in message_text:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Please enter the <ami-image-id> and an instance type",
                            as_user=True)
                    else:
                        ami_id = message_text.split()[1]
                        conn.run_instances(ami_id, instance_type=message_text.split()[-1])

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Creating server with AMI {}".format(ami_id),
                            as_user=True)

                # Shutdown Instance
                if re.match(r'.*(shutdown).*', message_text, re.IGNORECASE):
                    if 'i-' not in message_text:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Use list to see the list of instances and then run shutdown <instance-id>",
                            as_user=True)
                    else:
                        instance = re.split('shutdown ', message_text)[-1]
                        conn.stop_instances(instance_ids=instance.split())

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Shutting down {}".format(instance),
                            as_user=True)

                # Terminate Instance
                if re.match(r'.*(delete).*', message_text, re.IGNORECASE):
                    if 'i-' not in message_text:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Use list to see the list of instances and then run shutdown <instance-id>",
                            as_user=True)
                    else:
                        instance = re.split('delete ', message_text)[-1]
                        conn.terminate_instances(instance_ids=instance.split())

                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Deleting instance {}".format(instance),
                            as_user=True)

                # List Instance IDs
                if re.match(r'.*(list).*', message_text, re.IGNORECASE):
                    reservations = conn.get_all_reservations()
                    for reservation in reservations:
                        list_instance = re.split('Instance:', ''.join(str(e) for e in reservation.instances))[-1]
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="{}".format(list_instance),
                            as_user=True)

        time.sleep(1)
