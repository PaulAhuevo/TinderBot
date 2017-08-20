from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_calendar.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
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


def createEvent(girlName, date, time):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    eventTitle = 'Date mit ' + girlName
    startTime = date + "T" + time + ":00+02:00"
    endTime = startTime

    event = {
        'summary': eventTitle,
        'description': 'Will be used later for more specific information about the date.',
        'start': {
            'dateTime': startTime,
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': endTime,
            'timeZone': 'Europe/Berlin',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def isFree(date, time): # return boolean, checks -1h, -2h, +1h, +2h
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    isFree = True

    oneHourEarlier = str(int(time[0:2])-1) + time[2:]
    twoHoursEarlier = str(int(time[0:2])-2) + time[2:]
    oneHourLater = str(int(time[0:2])+1) + time[2:]
    twoHoursLater = str(int(time[0:2])+2) + time[2:]

    if not events:
        return True
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if not len(start) < 11:
            if date == start[0:10] and (time == start[11:16] or twoHoursEarlier == start[11:16] or oneHourEarlier == start[11:16] or oneHourLater == start[11:16] or twoHoursLater == start[11:16]):
                isFree = False
    return isFree









def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    event = {
        'summary': 'Date mit __xxx__',
        'description': 'Will be used later for more specific information about the date.',
        'start': {
            'dateTime': '2017-09-28T18:00:00+02:00',
            'timeZone': 'Europe/Berlin',
        },
        'end': {
            'dateTime': '2017-09-28T19:00:00+02:00',
            'timeZone': 'Europe/Berlin',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
