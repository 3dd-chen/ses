import os
import base64
import re
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import gspread
from datetime import datetime


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    """Authenticate and create Gmail API service"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def extract_codes_from_body(body_data):
    """Extract specific codes from the body content"""
    phone_pattern = r'<tr><td>手機 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    screen_pattern = r'<tr><td>螢幕 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    tablet_pattern = r'<tr><td>平板 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    smartwatch_pattern = r'<tr><td>智慧手錶/智慧手環 最低7折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    earphone_pattern = r'<tr><td>耳機 最低7折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    storage_pattern = r'<tr><td>儲存產品 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'

    phone_match = re.search(phone_pattern, body_data)
    screen_match = re.search(screen_pattern, body_data)
    tablet_match = re.search(tablet_pattern, body_data)
    smartwatch_match = re.search(smartwatch_pattern, body_data)
    earphone_match = re.search(earphone_pattern, body_data)
    storage_match = re.search(storage_pattern, body_data)

    if (
        phone_match
        and screen_match
        and tablet_match
        and smartwatch_match
        and earphone_match
        and storage_match
    ):
        phone_group1 = phone_match.group(1)
        phone_group2 = phone_match.group(2)
        screen_group1 = screen_match.group(1)
        screen_group2 = screen_match.group(2)
        tablet_group1 = tablet_match.group(1)
        tablet_group2 = tablet_match.group(2)
        smartwatch_group1 = smartwatch_match.group(1)
        smartwatch_group2 = smartwatch_match.group(2)
        earphone_group1 = earphone_match.group(1)
        earphone_group2 = earphone_match.group(2)
        storage_group1 = storage_match.group(1)
        storage_group2 = storage_match.group(2)

        tablet_matches = re.findall(tablet_pattern, body_data)
        smartwatch_matches = re.findall(smartwatch_pattern, body_data)
        earphone_matches = re.findall(earphone_pattern, body_data)

        if len(tablet_matches) >= 2:
            tablet_group1, tablet_group2 = tablet_matches[-1]
        if len(smartwatch_matches) >= 2:
            smartwatch_group1, smartwatch_group2 = smartwatch_matches[-1]
        if len(earphone_matches) >= 2:
            earphone_group1, earphone_group2 = earphone_matches[-1]

        return (
            phone_group1,
            phone_group2,
            screen_group1,
            screen_group2,
            tablet_group1,
            tablet_group2,
            smartwatch_group1,
            smartwatch_group2,
            earphone_group1,
            earphone_group2,
            storage_group1,
            storage_group2,
        )
    else:
        return None

def fetch_messages(service, query):
    """Fetch Gmail messages based on a query"""
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    data = []

    if not messages:
        print('No messages found.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            msg_data = msg['payload']
            headers = msg_data['headers']
            for header in headers:
                name = header['name']
                if name.lower() == 'from':
                    sender = header['value']
                if name.lower() == 'subject':
                    subject = header['value']
            if subject == "【開信領取】Samsung | 2025 年星學力教育優惠 (校園門市)":
                body = msg_data.get('body')
                if body:
                    if 'data' in body:
                        body_data = body['data']
                        body_data = base64.urlsafe_b64decode(body_data).decode('utf-8')
                        parsed_data = extract_codes_from_body(body_data)
                        if not parsed_data:
                            continue

                        (
                            phone_group1,
                            phone_group2,
                            screen_group1,
                            screen_group2,
                            tablet_group1,
                            tablet_group2,
                            smartwatch_group1,
                            smartwatch_group2,
                            earphone_group1,
                            earphone_group2,
                            storage_group1,
                            storage_group2,
                        ) = parsed_data

                        print(f'Phone Group 1: {phone_group1}')
                        print(f'Phone Group 2: {phone_group2}')
                        print(f'Screen Group 1: {screen_group1}')
                        print(f'Screen Group 2: {screen_group2}')
                        print(f'Tablet Group 1: {tablet_group1}')
                        print(f'Tablet Group 2: {tablet_group2}')
                        print(f'Smartwatch Group 1: {smartwatch_group1}')
                        print(f'Smartwatch Group 2: {smartwatch_group2}')
                        print(f'Earphone Group 1: {earphone_group1}')
                        print(f'Earphone Group 2: {earphone_group2}')
                        print(f'Storage Group 1: {storage_group1}')
                        print(f'Storage Group 2: {storage_group2}')

                        data.append(
                            {
                                'Phone Group 1': phone_group1,
                                'Phone Group 2': phone_group2,
                                'Screen Group 1': screen_group1,
                                'Screen Group 2': screen_group2,
                                'Tablet Group 1': tablet_group1,
                                'Tablet Group 2': tablet_group2,
                                'Smartwatch Group 1': smartwatch_group1,
                                'Smartwatch Group 2': smartwatch_group2,
                                'Earphone Group 1': earphone_group1,
                                'Earphone Group 2': earphone_group2,
                                'Storage Group 1': storage_group1,
                                'Storage Group 2': storage_group2,
                            }
                        )
                    elif 'text' in body:
                        body_data = body['text']
                    else:
                        body_data = ''
                else:
                    body_data = ''
    return data

def append_to_google_sheets(data, worksheet):
    existing_data = worksheet.get_all_values()[1:]
    for item in data:
        values = list(item.values())
        worksheet.insert_row(values, index=len(existing_data) + 2)
    print("Data has been inserted into Google Sheet.")

def main():
    stored_timestamp = "1970-01-01 00:00:00"
    try:
        with open("timestamp.txt", "r") as file:
            stored_timestamp = file.read().strip()
    except FileNotFoundError:
        pass
    stored_datetime = datetime.strptime(stored_timestamp, "%Y-%m-%d %H:%M:%S")

    query = f'label:inbox subject:"【開信領取】Samsung | 2025 年星學力教育優惠 (校園門市)" after:{int(stored_datetime.timestamp())}'
    service = authenticate()
    data = fetch_messages(service, query)

    gc = gspread.service_account(filename='sheet_credentials.json')
    spreadsheet = gc.open('神奇序號2025')
    worksheet = spreadsheet.get_worksheet(0)

    if data:
        append_to_google_sheets(data, worksheet)
        print("New data has been inserted into Google Sheet.")
        with open("flag.txt", "r") as f:
            content = f.read()
        content = "0"
        with open("flag.txt", "w") as f:
            f.write(content)
    else:
        print("No new data to insert.")
        with open("flag.txt", "r") as f:
            content = f.read()
        content = "0"
        with open("flag.txt", "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()
