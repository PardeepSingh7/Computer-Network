# import the library
import googlemaps
import pprint
import xlsxwriter
import time

API_KEY = 'AIzaSyCLezeMDD6qkolkdkUfLxo-MODxao2_riU'

gmaps = googlemaps.Client(key=API_KEY)

places_result = gmaps.places_nearby(
    location='53.312182699999994,-6.26093991548349', radius=4000, open_now=False, type='restaurant')

time.sleep(3)

place_result = gmaps.places_nearby(page_token=places_result['next_page_token'])

stored_results = []

for place in places_result['results']:

    my_place_id = place['place_id']

    my_fields = ['name', 'formatted_phone_number', 'website']

    places_details = gmaps.place(place_id=my_place_id, fields=my_fields)

    pprint.pprint(places_details['result'])

    stored_results.append(places_details['result'])

# -------------- DUMPING VALUES IN EXCEL -----------------------
row_headers = stored_results[0].keys()

# create a new workbook and a new worksheet.
workbook = xlsxwriter.Workbook(
    'C:\\Users\\parde\\Desktop\\computer network\\weather_data\\Weather_map_Data.csv')
worksheet = workbook.add_worksheet()

# populate the header row
col = 0
for header in row_headers:
    worksheet.write(0, col, header)
    col += 1

row = 1
col = 0
# populate the other rows

# get each result from the list.
for result in stored_results:

    # get the values from each result.
    result_values = result.values()

    # loop through each value in the values component.
    for value in result_values:
        worksheet.write(row, col, value)
        col += 1

    # make sure to go to the next row & reset the column.
    row += 1
    col = 0

# close the workbook
workbook.close()
