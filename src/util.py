def member_to_attachment(member):
    if "photo" in member:
        photo_url = member["photo"].get("photo_link")
    else:
        photo_url = (
            "https://secure.meetupstatic.com/s/img/2982428616572973604/noPhoto_80.gif"
        )
    return {
        "text": f"*{member['name']}* has asked to join *{member['group']['name']}*",
        "attachments": [
            {
                "text": "Approve or deny this user request",
                "fallback": "Unable to submit request",
                "callback_id": "approve_member",
                "attachment_type": "default",
                "author_icon": "https://secure.meetupstatic.com/s/img/786824251364989575000/logo/swarm/m_swarm_630x630.png",
                "author_name": member["profile_url"],
                "author_link": member["profile_url"],
                "thumb_url": photo_url,
                "actions": [
                    {
                        "name": "approve_member",
                        "text": "Approve",
                        "style": "primary",
                        "type": "button",
                        "value": "approve",
                    },
                    {
                        "name": "deny_member",
                        "text": "Deny",
                        "type": "button",
                        "value": "deny",
                        "confirm": {
                            "title": "Deny this member request?",
                            "ok_text": "Yes",
                            "dismiss_text": "No",
                        },
                    },
                ],
            }
        ],
    }

