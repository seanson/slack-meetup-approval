import os
import sys
import logging
import time

import schedule
import requests
import meetup.api

from dotenv import load_dotenv
from pprint import pprint

from util import member_to_attachment

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("slack-meetup-approval")
load_dotenv()

REQUIRED_ENV = ["MEETUP_API_KEY", "WEBHOOK_URL", "MEETUP_URL"]

for item in REQUIRED_ENV:
    if item not in os.environ:
        log.error(f"Missing {item} in environment variables.")
        sys.exit(1)

pending_members = {}
sent_members = set()


def fetch_pending_members():
    client = meetup.api.Client()
    log.info("Querying Meetup API")
    members = client.GetProfiles(
        {
            "group_urlname": os.environ["MEETUP_URL"],
            "status": "pending",
            "fields": "bio,comment",
        }
    )
    log.info(f"Found {len(members.results)} pending members.")
    for member in members.results:
        pending_members.setdefault(member["member_id"], member)


def send_pending_to_slack():
    log.info(f"Current pending members: {list(pending_members.keys())}")
    for member in pending_members.values():
        if member["member_id"] in sent_members:
            continue
        message = member_to_attachment(member)
        log.info(f"Sending Slack alert for {member['member_id']}")
        requests.post(os.environ["WEBHOOK_URL"], json=message)
        sent_members.add(member["member_id"])


# fetch_pending_members()
# send_pending_to_slack()

schedule.every(10).seconds.do(fetch_pending_members)
schedule.every(30).seconds.do(send_pending_to_slack)


while True:
    schedule.run_pending()
    time.sleep(1)
