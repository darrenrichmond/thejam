import requests, json, maya, user_calendar
from app.models import Event, Venue
import keys

def getRawEvents():
    
    #Try to ge the events from the database
    events = Event.query.all()

    #If I didn't get any events, populate with hard-coded test data
    if not events:
        events = [
            {
                'venue': {
                    'name': 'The Pigpen Test',
                    'address': '106 Pershing Ave, San Antonio, TX 78209',
                    'website': 'https://www.facebook.com/thepigpensa/'
                },
                'event': {
                    'night': 'Tuesday',
                    'recurs': 'weekly',
                    'start': '7 pm',
                    'end': '9 pm',
                    'adv_signup': 'none', 
                    'notes': 'My current favorite!'
                }
            },
            {
                'venue': {
                    'name': 'Big Bobs Burgers Test',
                    'address': '447 W Hildebrand Ave Ste 107, San Antonio, Texas 78212',
                    'website': 'https://www.facebook.com/bigbobsburger/'
                },
                'event': {
                    'night': 'Wednesday',
                    'recurs': 'weekly',
                    'start': '7pm',
                    'end': '10pm',
                    'adv_signup': 'none', 
                    'notes': 'Next one to try'
                }
            }
        ]
    return events

#this is the core method to get the drive time to the event.
#required: start is the starting location
#required: end is the ending location
#optional: departure time is the time you plan to leave
def getDriveDuration(start,end,departure_time=None):
    #this is the Google Maps API. I am always going to work with JSON, never with XML
    maps_api='https://maps.googleapis.com/maps/api/distancematrix/json'
    maps_api_key = keys.google_maps_api_key
    #construct the basic payload of required information for the Google Maps API
    payload = {
        'origins': start,
        'destinations': end,
        'key': maps_api_key        
    }
    r = requests.get(maps_api, params=payload)
    r_json = r.json()
    print("Duration JSON")
    print(r_json)
    print('**************')
    first_element = r_json['rows'][0]['elements'][0]
    if 'duration' in first_element:
        duration = first_element['duration']['text']
    else:
        duration = 'N/A'
    return duration

def addDriveDuration(start_loc,event):
    event['drive'] = 'N/A'
    event_address = event['venue']['address']
    if start_loc and event_address:
        drive = getDriveDuration(start_loc,event_address)
        event['drive'] = drive
    return event

def getEvents(user):
    #get the raw events, then enrich them with calculated values
    raw_events = getRawEvents()
    enriched_events = []
    for i, e in enumerate(raw_events):
        serialized_event = e.serialize()
        print(serialized_event)
        enriched_event = addDriveDuration(user.home_address,serialized_event)
        enriched_events.append(enriched_event)
    return enriched_events