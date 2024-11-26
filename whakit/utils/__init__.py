# whakit/utils/helpers.py


def extract_message_and_sender_info(body: dict):
    message = (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("messages", [{}])[0]
    )
    sender_info = (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("contacts", [{}])[0]
    )
    return message, sender_info
