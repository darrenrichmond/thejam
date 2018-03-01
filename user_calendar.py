from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

import datetime
import jamevents

#this seems to be messing up my running of flask, so getting rid of argument parsing
#TODO: would be cool to add it back somewhere, but probably not here
#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'thejam calendar client 1'

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
                                   'thejam_calendar.json')

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

def getCalendar(credentials):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service

def getEvents(credentials, time, max):
    service = getCalendar(credentials)
    print('Getting the upcoming ' + str(max) + ' events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=time, maxResults=max, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events

#TODO: genericice to take the details needed to add any calendar event
def addEvent(credentials):
    event = {
        'summary': 'Pigpen Test',
        'description': 'Test inserting an event',
        'start': {
            'dateTime': '2018-02-21T09:00:00-07:00',
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': '2018-02-21T17:00:00-07:00',
            'timeZone': 'America/Chicago',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT=5'
        ],
    }

    service = getCalendar(credentials)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created:' + event.get('htmlLink'))


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    max = 7
    events = getEvents(credentials, now, max)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    #addEvent(credentials)

if __name__ == '__main__':
    main()