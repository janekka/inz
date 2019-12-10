from .google_maps import get_distance, get_arrivals
import time
from calendar import timegm

def time_to_epoch(date, time_dep, places):
    time_string = str(date) + 'T' + str(time_dep)
    time_stripped = time.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    epoch_time_dep = timegm(time_stripped)
    args = [places[0],]
    for el in places[1].split():
        args.append(el)
    args.append(places[2])
    arr_times = get_arrivals(args)

    for i in range(len(arr_times)):
        arr_times[i] = epoch_time_dep + arr_times[i]

    arr_times_str = ''
    for el in arr_times[:-1]:
        arr_times_str = arr_times_str + str(el) + ' '

    return (epoch_time_dep, arr_times_str, arr_times_str[-1])

#time_to_epoch('30/11/2019', '10:00', ('Wroclaw', ['Lodz',], 'Poznań'))
        