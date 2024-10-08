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



# Scopes required to access Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# data = []  


def authenticate():
    """Authenticate and create Gmail API service"""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Create the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


def extract_codes_from_body(body_data):
    """Extract specific codes from the body content"""
    tablet_pattern = r'<tr><td>平板 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    smartwatch_pattern = r'<tr><td>智慧手錶 85折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    earphone_pattern = r'<tr><td>耳機 7折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'

    tablet_match = re.search(tablet_pattern, body_data)
    smartwatch_match = re.search(smartwatch_pattern, body_data)
    earphone_match = re.search(earphone_pattern, body_data)


    if (
        tablet_match
        and smartwatch_match
        and earphone_match
    ):
        tablet_group1 = tablet_match.group(1)
        tablet_group2 = tablet_match.group(2)
        smartwatch_group1 = smartwatch_match.group(1)
        smartwatch_group2 = smartwatch_match.group(2)
        earphone_group1 = earphone_match.group(1)
        earphone_group2 = earphone_match.group(2)

        tablet_matches = re.findall(tablet_pattern, body_data)
        smartwatch_matches = re.findall(smartwatch_pattern, body_data)
        earphone_matches = re.findall(earphone_pattern, body_data)
    
        #if len(tablet_matches) >= 2:
        #    tablet_group1, tablet_group2 = tablet_matches[-1]
        #if len(smartwatch_matches) >= 2:
        #    smartwatch_group1, smartwatch_group2 = smartwatch_matches[-1]
        #if len(earphone_matches) >= 2:
        #    earphone_group1, earphone_group2 = earphone_matches[-1]
    

        return (
            tablet_group1,
            tablet_group2,
            smartwatch_group1,
            smartwatch_group2,
            earphone_group1,
            earphone_group2,
        )
    else:
        return None


def fetch_messages(service, query):
    """Fetch Gmail messages based on a query"""
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    
    data = []
    tablet_pattern = r'<tr><td>平板 9折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    smartwatch_pattern = r'<tr><td>智慧手錶 85折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    earphone_pattern = r'<tr><td>耳機 7折序號 </td><td>([A-Z0-9]+)</td><td>([A-Z0-9]+)</td></tr>'
    
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
            if subject == "Samsung星學力 三星智慧館校園門市專屬活動〔通知信〕":
                body = msg_data.get('body')
                if body:
                    if 'data' in body:
                        body_data = body['data']
                        body_data = base64.urlsafe_b64decode(body_data).decode('utf-8')

                        (
                            tablet_group1,
                            tablet_group2,
                            smartwatch_group1,
                            smartwatch_group2,
                            earphone_group1,
                            earphone_group2,
                        ) = extract_codes_from_body(body_data)

                        if (
                            tablet_group1
                            and tablet_group2
                            and smartwatch_group1
                            and smartwatch_group2
                            and earphone_group1
                            and earphone_group2
                            
                        ):
                            
                            print(f'Tablet Group 1: {tablet_group1}')
                            print(f'Tablet Group 2: {tablet_group2}')
                            print(f'Smartwatch Group 1: {smartwatch_group1}')
                            print(f'Smartwatch Group 2: {smartwatch_group2}')
                            print(f'Earphone Group 1: {earphone_group1}')
                            print(f'Earphone Group 2: {earphone_group2}')
                            
                            data.append(
                                {
                                    
                                    'Tablet Group 1': tablet_group1,
                                    'Tablet Group 2': tablet_group2,
                                    'Smartwatch Group 1': smartwatch_group1,
                                    'Smartwatch Group 2': smartwatch_group2,
                                    'Earphone Group 1': earphone_group1,
                                    'Earphone Group 2': earphone_group2,
                                    
                                }
                            )
                            
                        else:
                            print('Pattern not found in the body.')
                    elif 'text' in body:
                        body_data = body['text']
                    else:
                        body_data = ''
                else:
                    body_data = ''
    return data

def append_to_google_sheets(data, worksheet):
    # 獲取現有數據（不包含標題行）
    existing_data = worksheet.get_all_values()[1:]  # 排除標題行

    # 將新數據插入到現有數據後面
    for item in data:
        values = list(item.values())
        worksheet.insert_row(values, index=len(existing_data) + 2)  # 插入到現有數據後面

    print("Data has been inserted into Google Sheet.")


def main():
    # 讀取已儲存的時間戳記
    stored_timestamp = "1970-01-01 00:00:00"
    try:
        with open("timestamp.txt", "r") as file:
            stored_timestamp = file.read().strip()
    except FileNotFoundError:
        pass

    # 轉換成 datetime 格式
    stored_datetime = datetime.strptime(stored_timestamp, "%Y-%m-%d %H:%M:%S")

    # Fetch messages using a query (e.g., 'label:inbox subject:"Samsung星學力 三星智慧館校園門市專屬活動〔通知信〕"')
    query = f'label:inbox subject:"Samsung星學力 三星智慧館校園門市專屬活動〔通知信〕" after:{int(stored_datetime.timestamp())}'
    service = authenticate()
    data = fetch_messages(service, query)

    # 建立一個 gspread 的連接
    gc = gspread.service_account(filename='sheet_credentials.json')

    # 開啟指定的 Google Sheets
    spreadsheet = gc.open('一般神奇序號')
    worksheet = spreadsheet.get_worksheet(0)

    # 將新資料追加到 Google Sheets 中
    if data:
        append_to_google_sheets(data, worksheet)
        print("New data has been inserted into Google Sheet.")
        with open("flag.txt", "r") as f:
            content = f.read()

    # 將內容改寫為 "0"
        content = "0"

    # 將改寫後的內容寫回到 flag.txt
        with open("flag.txt", "w") as f:
            f.write(content)
    else:
        print("No new data to insert.")
        with open("flag.txt", "r") as f:
            content = f.read()

    # 將內容改寫為 "0"
        content = "0"

    # 將改寫後的內容寫回到 flag.txt
        with open("flag.txt", "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()
