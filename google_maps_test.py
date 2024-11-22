import requests

API_KEY = 'AIzaSyDQuIKyW6EAbnqSId02ATMte8ItuAnpguo'

'''
url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"
response = requests.get(url)
data = response.json()
sample code from https://blog.apify.com/google-maps-api-python/ of sayam tripathi
thanks king 
'''


# use google maps api to get coordinates of an address string
def get_coords(api_key, address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            return lat, lng

        else:

            print(f"Error: {data['error_message']}")
            return 0, 0
    else:
        print("Failed to make the request.")
        return 0, 0


def get_distance(begin, goal, api_key):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": begin,
        "destinations": goal,
        "key": api_key
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:

        data = response.json()

        if data["status"] == "OK":
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            return distance, duration
        else:
            print("Request failed.")
            return None, None
    else:
        print("Failed to make the request.")
        return None, None


start = "3601 Ridge Road, Durham, NC"
end = "302 South Bend Dr, Durham, NC"

distance, duration = get_distance(start, end, API_KEY)

if distance and duration:
    print(f"Driving Distance: {distance}")

    print(f"Driving Duration: {duration}")

address = '302 South Bend Drive, Durham, NC'

lati, longi = get_coords(API_KEY, address)

print(f"Latitude: {lati}")
print(f"Longitude: {longi}")
