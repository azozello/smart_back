from __future__ import print_function

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import pickle
import os.path
import json

from ..util.cache import Cache

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_PATH = '/Users/denyspanov/Devel/smart_back/app/resources/tokens/token.pickle'
CREDENTIALS_PATH = '/Users/denyspanov/Devel/smart_back/app/resources/credentials.json'


def get_email_by_id(email_id):
    cached_message = Cache().get(f"{email_id}_long")
    if cached_message is not None:
        return cached_message
    else:
        credentials = set_up_credentials()
        service = build('gmail', 'v1', credentials=credentials)
        msg = service.users().messages().get(userId="me", id=email_id, format="full", metadataHeaders=None).execute()
        raw_data = str(msg['payload']['parts'][1]['body']['data'])
        decoded = base64.urlsafe_b64decode(raw_data.encode('ASCII'))
        Cache().add(f"{email_id}_long", decoded)
        return decoded


def get_emails_list():
    credentials = set_up_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    inbox = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = inbox.get('messages', [])
    return get_messages(service, messages)


def set_up_credentials():
    empty_credentials = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            empty_credentials = pickle.load(token)

    if not empty_credentials or not empty_credentials.valid:
        if empty_credentials and empty_credentials.expired and empty_credentials.refresh_token:
            empty_credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            empty_credentials = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(empty_credentials, token)

    return empty_credentials


def get_messages(service, messages):
    cache = Cache()
    message_count = 0
    parsed = []
    for message in messages:
        if message_count >= 10:
            break
        else:
            message_count += append_message(service, cache, message, parsed)
    return parsed


def append_message(service, cache, message, parsed):
    cached_message = cache.get(f"{message['id']}_short")
    if cached_message is not None:
        parsed.append(json.loads(cached_message))
        return 1
    else:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        result_object = {'id': msg['id'], 'message': msg['snippet']}
        fill_message_object(msg, result_object)
        parsed.append(result_object)
        cache.add(f"{message['id']}_short", json.dumps(result_object))
        return 1


def fill_message_object(msg, message_object):
    parsed_header_count = 0
    for header in msg['payload']['headers']:
        if header['name'] == 'Delivered-To':
            message_object['recipient'] = header['value']
            parsed_header_count += 1
        if header['name'] == 'From':
            from_array = str(header['value']).split('<')
            message_object['senderName'] = from_array[0][:-1]
            message_object['senderEmail'] = from_array[1][:-1]
            parsed_header_count += 1
        if header['name'] == 'Date':
            message_object['timestamp'] = header['value']
            parsed_header_count += 1
        if header['name'] == 'Subject':
            message_object['subject'] = header['value']
            parsed_header_count += 1
        if parsed_header_count >= 4:
            break
    return message_object


if __name__ == '__main__':
    get_emails_list()
