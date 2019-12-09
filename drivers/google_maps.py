import googlemaps

def get_distance(args):
    API_key = 'AIzaSyDAkP8-ao9ZVMdAAPXBpSsIBIFi0-JxCkk'
    gmaps = googlemaps.Client(key=API_key)

    origins = args[0]
    destinations = args[1]

    result = gmaps.distance_matrix(origins, destinations)
    #print(result["rows"][0]["elements"][0]["distance"]["value"], result["rows"][0]["elements"][0]["duration"]["value"])
    return (result["rows"][0]["elements"][0]["distance"]["value"], result["rows"][0]["elements"][0]["duration"]["value"])

def get_arrivals(args):
    API_key = 'AIzaSyDAkP8-ao9ZVMdAAPXBpSsIBIFi0-JxCkk'
    gmaps = googlemaps.Client(key=API_key)

    origins = list(args[:-1])
    destinations = list(args[1:])

    result = gmaps.distance_matrix(origins, destinations)

    travel_times = []
    for i in range(len(result['rows'])):
        travel_times.append(result['rows'][i]['elements'][i]['duration']['value'])
    
    arr_times = []
    for i in range(len(travel_times)):
        arr_times.append(sum(travel_times[:i+1]))
 
    return arr_times



