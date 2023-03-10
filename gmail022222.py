from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def get_message(service, count):
    results = service.users().messages().list(userId='me').execute()
    msg_ids = []
    msgs = []

    for msg in results['messages']:
        msg_ids.append(msg['id'])
    for index in range(count):
        message = service.users().messages().get(userId='me',
                                                 id=msg_ids[index], format='metadata').execute()
        msgs.append(message)
    return msgs

def get_parameters(message):
    msg = message
    available = []
    for i in range(len(msg['payload']['headers'])):
        available.append(msg['payload']['headers'][i]['name'])
    return available

def get_message_by_param(messages, params):
    for i in range(len(messages)):
        for j in range(len(messages[i]['payload']['headers'])):
            if messages[i]['payload']['headers'][j]['name'] in params:
                pprint(f"{messages[i]['payload']['headers'][j]['name']}: {messages[i]['payload']['headers'][j]['value']}")
        print("---------------------------------------")


def input_parameters():
    parameter = input("V??lasszon a param??terek k??z??l, majd g??pelje be a nev??t! ")
    params = [parameter]
    while parameter != '':
        parameter = input("V??lasszon a param??terek k??z??l, majd g??pelje be a nev??t! ")
        if parameter != '':
            params.append(parameter)
        else:
            break
    return params


def main():
    service = get_service()
    count = int(input("Adja meg a megjelen??tend?? levelek sz??m??t! "))
    messages = get_message(service, count)
    print("")
    print("El??rhet?? param??terek: \n")
    print('\n'.join(get_parameters(messages[0])))
    print("-------------------------------------")
    print("\nHa nem szeretne tov??bbi param??tereket megadni akkor nyomja meg az ENTERT, m??sk??l??nben folytassa a param??terek megad??s??t! ")
    params = input_parameters()
    print("")
    print("\nMegjegyz??s: Ha valamelyik lek??rt emailn??l nem tal??l a param??terhez adatot, akkor azt figyelmen k??v??l haggya.")
    get_message_by_param(messages, params=params)




main()
