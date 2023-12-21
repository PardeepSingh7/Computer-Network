import googlemaps
import pprint
import time
#from GoogleMapsAPIKey import get_my_key

API_KEY = 'AIzaSyCLezeMDD6qkolkdkUfLxo-MODxao2_riU'

gmaps = googlemaps.Client(key=API_KEY)

places_result = gmaps.places_nearby(
    location=-'-33.8670522,151.1957362', radius=40000, open_now=False, type='cafe')
print(places_result)
for place in places_result['results']:

    my_place_id = place['place_id']

    my_field = ['name', 'formatted_phonenumber', 'type']

    place_details = gmaps.place(place_id=my_place_id, field=my_field)

    print(place_details)
