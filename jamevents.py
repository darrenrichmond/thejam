import requests, json, maya
import keys

def getRawEvents():
    events = [
        {
            'venue': {
                'name': 'The Pigpen',
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
                'name': 'Big Bobs Burgers',
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
    duration = r_json['rows'][0]['elements'][0]['duration']['text']
    return duration

def addDriveDuration(start_loc,event):
    if start_loc is None:
            event['venue']['drive'] = 'N/A'
    else:
        event_address = event['venue']['address']
        drive = getDriveDuration(start_loc,event_address)
        event['venue']['drive'] = drive
    return event

def enrichEvents(user,events):
    #iterate over all the events, and add drive durations to each
    for i, e in enumerate(events):
        events[i] = addDriveDuration(user.home_address,e)
    return events


def getEvents(user):
    #get the raw events, then enrich them with calculated values
    return enrichEvents(user, getRawEvents())