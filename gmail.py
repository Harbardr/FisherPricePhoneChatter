from __future__ import print_function
import httplib2
import os

import sys
import pyttsx
import time
import base64

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
HOME = "/home/pi/"
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
# https://developers.google.com/gmail/api/auth/scopes
# SCOPES = 'https://mail.google.com/'
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = '/home/pi/client_secret.json'
APPLICATION_NAME = 'FisherPriceChatter'

PRINT_CATEGORY = False
GMAIL_UNREAD = 0

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    #home_dir = os.path.expanduser('~')
    home_dir = os.path.expanduser(HOME)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.
    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
           page_token = response['nextPageToken']
           response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
           messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.
    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id, snippetMessage=True):
    """Get a Message with given ID.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.
    Returns:
        A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        #print('Message snippet: %s' % message['snippet'])
        #print('Message snippet: %s' % message['payload']['headers'])
        #print(unicode('Message snippet: %s' % message['snippet'],'utf-8'))

        if snippetMessage:
            return message['snippet']
        else:
            return message
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def DeleteMessage(service, user_id, msg_id):
    """Delete a Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
    """
    try:
        service.users().messages().delete(userId=user_id, id=msg_id).execute()
        print('Message with id: %s deleted successfully.' % msg_id)
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def TrashMessage(service, user_id, msg_id):
    """Delete a Message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message to delete.
    """
    try:
        service.users().messages().trash(userId=user_id, id=msg_id).execute()
        print('Message with id: %s deleted successfully.' % msg_id)
    except errors.HttpError, error:
        print('An error occurred: %s' % error)


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


if __name__ == '__main__':
    main()