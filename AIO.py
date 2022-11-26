import json
import geopy.distance
import requests
import random
from serpapi import GoogleSearch

# https://serpapi.com/dashboard
serp_api_key = "bbab243ae2358bc1ff04b9ac94507c20291c93e3c3ac493a270afbd06d452a82"
#serp_api_key = "2842e2c4c2dc135ba20e2fe720913a0d2e26e53d43fb69c3c1731851e5a7260e"
# https://home.openweathermap.org/api_keys
weather_api_key = "123c4ec2b8095708db67dc099bb0f8d4"

def events(o_lat, o_long, o_date, radius, city, country):
    #searching for events
    params = {
    "engine": "google_events",
    "q": "Events in {city}",
    "location": {city, country},
    "hl": "en",
    "api_key": serp_api_key
    }
    #print(params)
    search = GoogleSearch(params)
    #print(search)
    results = search.get_dict()

    #print(results)
    #print(json.dumps(results, indent=3))
    try:
        events_results = results["events_results"]
        #print(json.dumps(events_results, indent=3))
    except:
        print("No Events")
        return 0

    if not events_results:
        return 0   #terminate and return 0 if no events

    for i in events_results:
        #print(i["date"]["start_date"])
        #print((json.dumps(i["date"]["start_date"])))
        address = json.dumps(i["address"])
        date = (json.dumps(i["date"]["start_date"]))
        disallowed_chars ='"'
        for char in disallowed_chars:
            date = date.replace(char,"")
        #print(date.lower())
        if (date.lower()).__eq__(o_date.lower()):
            second_params = {
            "engine": "google_maps",
            "q": address,
            "type": "search",
            "hl": "en",
            "api_key": serp_api_key
            }
            search = GoogleSearch(second_params)
            results = search.get_dict()
            #print(json.dumps(results, indent=3))

            try:
                local_results = results["place_results"]["people_also_search_for"][0]["local_results"]
            except:
                continue


            #print(local_results[0]["gps_coordinates"]["latitude"])
            latitute = local_results[0]["gps_coordinates"]["latitude"]
            longitude = local_results[0]["gps_coordinates"]["longitude"]

            #print(latitute , longitude)
            coords_1 = (latitute, longitude) #destination
            coords_2 = (o_lat,o_long) #origin
            distance = geopy.distance.geodesic(coords_1, coords_2).km
            print(" <<Dis>> " + str(distance))
            if distance <= radius:
                return 1
    return 0

def weather(city_name):
    # checks the weather condtions in the city
    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # complete url address
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name + "&units=metric"

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] == "404":
        return 0
    else:
        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        #current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        #current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        #current_humidity = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]
        #print(z)
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_id = z[0]["id"]

        #According to https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
        #202, 211, 212, 221 is not acceptable thunder storms
        #501 - 531 rain conditions / 6XX snow/ 741 fog / 781 tornado

        if 500 <= weather_id <= 501:
            return 0.2
        elif weather_id == 520:
            return 0.4
        elif weather_id == 521:
            return 0.5
        elif weather_id == 600 or 612 <= weather_id <= 620:
            return 0.6
        elif weather_id == 601 or weather_id == 611 or weather_id == 621 or weather_id == 741:
            return 0.7
        elif 502 <= weather_id <= 504:
            return 0.8
        elif weather_id == 511 or weather_id <= 531:
            return 0.9
        elif weather_id == 522 or weather_id <= 602 or weather_id <= 762 or weather_id <= 781:
            return 1
        else:
            return 0

    return 0

def busyParking():
    return round(random.random(), 1)

def keywordSearch(o_lat, o_long, radius, keyword):
    #searching for hotels within radius
    coord = "@"+str(o_lat)+","+str(o_long)+",15.1z"
    params = {
        "engine": "google_maps",
        "q": keyword,
        "ll": coord,
        "type": "search",
        "api_key": serp_api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    if not results:
        return 0
    #print(json.dumps(results, indent=3))

    try:
        for i in range(len(results)):
            #print(results["local_results"][i]["gps_coordinates"], "\n")
            latitute = results["local_results"][i]["gps_coordinates"]["latitude"]
            longitude = results["local_results"][i]["gps_coordinates"]["longitude"]

            #print(latitute , longitude)
            coords_1 = (latitute, longitude)  # destination
            coords_2 = (o_lat, o_long)  # origin
            distance = geopy.distance.geodesic(coords_1, coords_2).km

            #print("Name: "+results["local_results"][i]["title"]+"\n",coords_1, coords_2, "\nDistance", distance)
            if distance <= radius:
                return 1
    except:
        print("no results")
    return 0

