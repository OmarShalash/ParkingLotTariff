from AIO import *
import array

writeToFile = []

def doMagic(invoke):
    global writeToFile
    if str(invoke[0]).__eq__("events"):
        if len(invoke) != 7:
            return 404
        else:
            result = events(invoke[1], invoke[2], invoke[3], invoke[4], invoke[5], invoke[6])
            print("Events -> "+str(result))
            writeToFile.append("Events "+str(result))
            print(writeToFile)
    elif str(invoke[0]).__eq__("weather"):
        if len(invoke) != 2:
            return 404
        else:
            result = weather(invoke[1])
            writeToFile.append("Weather "+str(result))
            print(writeToFile)
    elif str(invoke[0]).__eq__("keywordSearch"):
        if len(invoke) != 5:
            return 404
        else:
            result = keywordSearch(invoke[1], invoke[2], invoke[3], invoke[4])
            writeToFile.append(invoke[4]+" "+str(result))
            print(writeToFile)

f = open("in.data", "r")
for x in f:
    chunks = x.split(',')
    chunks = list(map(lambda x: x.strip(), chunks))
    doMagic(chunks)
f.close()
f = open("out.data", "w")
f.write('\n'.join(writeToFile))
f.close()

#Testing the Busy ParkingFunc:
#print(events(51.51730045807655, -0.10509365287228956, "sep 20", 10, "London", "united kingdom"))

#Testing the Busy ParkingFunc:
#print(busyParking())

#Testing the WeatherFunc:
#print(weather("alexandria"))


#Testing the HotelFunc:
#Keyword could be ["hotel", "restaurant", "supermarket"]
#print(keywordSearch(51.51730045807655, -0.10509365287228956, 2, "supermarket"))

