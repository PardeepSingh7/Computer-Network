import requests
city = input('input the city name')
print(city)
print('Displaying Weather report for: ' + city)
# output:
# Displaying Weather report for: bhopal
city = input('input the city name')
print(city)
url = 'https://wttr.in/{}'.format(city)
res = requests.get(url)
print(res.text)
