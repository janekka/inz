from django.core.management.base import BaseCommand, CommandError
from drivers.models import Driver, Passenger, Ride, Driver_hist, Passenger_hist, Ride_hist
import numpy as np
from lpsolve55 import *
from lp_solve import *
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):

        ride_date = (datetime.datetime.now() + datetime.timedelta(days=2)).date()
#import danych z bazy
        drs = Driver.objects.filter(date=ride_date)
        ps = Passenger.objects.filter(date=ride_date)
        #print(type(drs[1]))

#wspolczynniki funkcji celu
        c = np.zeros([len(ps),len(drs)])
        for i in range(len(ps)):
            for j in range(len(drs)):
                c[i][j] = ps[i].distance*drs[j].price
        #print(c.shape)
        f = c.flatten(order='C')
        #print(f.shape)

#ograniczenia
#inicjacja wektora b - wektora prawej strony ograniczen i indeksu
        b = np.zeros(len(drs)+2*len(ps)+len(ps)*len(drs))
        b_i = 0

#inicjacja wektora cons_type okreslajacego typ ograniczen
        cons_type = np.ones(len(drs)+2*len(ps)+len(ps)*len(drs))

#inicjacja a - lista z prawa strona ograniczen
        a_temp = []

#ograniczenia na pojemnosc samochodow        
        for j in range(len(drs)):
            x = np.zeros([len(ps), len(drs)])
            for i in range(len(ps)):
                x[i][j] = 1
            a_temp.append(x.flatten(order='C'))
            b[b_i] = drs[j].car_cap
            b_i += 1

#ograniczenia przypisania pasazera do 1 kierowcy
        for i in range(len(ps)):
            x = np.zeros([len(ps), len(drs)])
            for j in range(len(drs)):
                x[i][j] = 1
            a_temp.append(x.flatten(order='C'))
            b[b_i] = 1
            b_i += 1
        
#ogrniczenia na budzet pasazerow
        for i in range(len(ps)):
            x = np.zeros([len(ps), len(drs)])
            for j in range(len(drs)):
                x[i][j] = ps[i].distance * drs[j].price
            a_temp.append(x.flatten(order='C'))
            b[b_i] = ps[i].max_cost
            b_i += 1

#ograniczenie kompatybilnosci kierowcow z pasazerami

        for i in range(len(ps)):
            for j in range(len(drs)):
                x = np.zeros([len(ps), len(drs)])
                x[i][j] = 1
                cons_type[b_i] = 3

                d_start = drs[j].start
                d_end = drs[j].end
                d_stops = drs[j].stops.split()
                d_cigs = drs[j].cigs
                d_pets = drs[j].pets
                d_dep = drs[j].time_dep
                #d_arr = drs[j].time_arr
                d_arr_stops_str = drs[j].stops_arr.split()
                d_arr_stops = []
                for el in d_arr_stops_str:
                    d_arr_stops.append(int(el))
                

                p_start = ps[i].start
                p_end = ps[i].end
                p_cigs = ps[i].cigs
                p_pets = ps[i].pets
                p_dep = ps[i].time_dep
                #p_arr = ps[i].time_arr

                if d_start == p_start and d_end == p_end:
                    if d_cigs == False or (d_cigs == True and p_cigs == False):
                        if d_pets == False or (d_pets == True and p_pets == False):
                            if p_dep <= d_dep <= p_dep+10800:
                                b[b_i] = 1
                                cons_type[b_i] = 1
                                #print('xd')

                if d_start == p_start and p_end in d_stops:
                    if d_cigs == False or (d_cigs == True and p_cigs == False):
                        if d_pets == False or (d_pets == True and p_pets == False):
                            if p_dep <= d_dep <= p_dep+10800:
                                b[b_i] = 1
                                cons_type[b_i] = 1
                                #print('xd')

                if p_start in d_stops and p_end == d_end:
                    if d_cigs == False or (d_cigs == True and p_cigs == False):
                        if d_pets == False or (d_pets == True and p_pets == False):
                            if p_dep <= d_arr_stops[d_stops.index(p_start)] <= p_dep+10800:
                                b[b_i] = 1
                                cons_type[b_i] = 1
                                #print('xd')

                if (p_start in d_stops and p_end in d_stops) and d_stops.index(p_start) < d_stops.index(p_end):
                    if d_cigs == False or (d_cigs == True and p_cigs == False):
                        if d_pets == False or (d_pets == True and p_pets == False):
                            if p_dep <= d_arr_stops[d_stops.index(p_start)] <= p_dep+10800:
                                b[b_i] = 1
                                cons_type[b_i] = 1
                                #print('xd')

                
                a_temp.append(x.flatten(order='C'))
                b_i += 1




#komponowanie macierzy a
        a = np.vstack(tuple(a_temp))

        sint = np.ones(a.shape[1])

        lp = lpsolve('make_lp', 0, a.shape[1])
        lpsolve('set_lp_name', lp, 'mymodel')
        lpsolve('set_verbose', 'mymodel', IMPORTANT)
        lpsolve('set_obj_fn', 'mymodel', f)
        for i in range(a.shape[0]):
            lpsolve('add_constraint', 'mymodel', a[i], cons_type[i], b[i])
        lpsolve('set_binary', 'mymodel', sint)
        lpsolve('set_maxim', 'mymodel')
        lpsolve('solve', 'mymodel')

        #ret = lpsolve('set_outputfile', lp, 'log.txt')
        #lpsolve('print_objective', 'mymodel')
        #lpsolve('print_lp', 'mymodel')
        #lpsolve('print_constraints', 'mymodel')
        #lpsolve('print_solution', 'mymodel')
        
        #const = lpsolve('get_constraints', 'mymodel')
        result = lpsolve('get_variables', 'mymodel')
 


        lpsolve('delete_lp', 'mymodel')
        #print(const)
        #print(result)
        assign = np.reshape(result[0], (len(ps), len(drs)), order='C')
        print(assign)
        for i in range(len(ps)):
            for j in range(len(drs)):
                if assign[i][j] == 1:
                    driver_obj = Driver.objects.get(id=drs[j].id)
                    passenger_obj = Passenger.objects.get(id=ps[i].id)
                    ride = Ride(driver_username=drs[j].username, passenger_username=ps[i].username, date=drs[j].date, pick_up=ps[i].start, drop_off=ps[i].end, driver_ride_id=driver_obj, passenger_ride_id=passenger_obj)
                    ride.save()
                    print('passenger ' + ps[i].username + 'rides with driver ' + drs[j].username)

#porzadkowanie bazy danych
        ps_obj = Passenger.objects.filter(date__lt=datetime.date.today())
        for i in range(len(ps_obj)):
            ps_hist = Passenger_hist(username=ps_obj[i].username, start=ps_obj[i].start, end=ps_obj[i].end, distance=ps_obj[i].distance, date=ps_obj[i].date, time_dep=ps_obj[i].time_dep, time_arr=ps_obj[i].time_arr, cigs=ps_obj[i].cigs, pets=ps_obj[i].pets, max_cost=ps_obj[i].max_cost)    
            ps_hist.save()
            ps_obj[i].delete()

        drs_obj = Driver.objects.filter(date__lt=datetime.date.today())
        for j in range(len(drs_obj)):
            drs_hist = Driver_hist(username=drs_obj[j].username, start=drs_obj[j].start, end=drs_obj[j].end, stops=drs_obj[j].stops, stops_arr=drs_obj[j].stops_arr, date=drs_obj[j].date, time_dep=drs_obj[j].time_dep, time_arr=drs_obj[j].time_arr, car_model=drs_obj[j].car_model, car_cap=drs_obj[j].car_cap, cigs=drs_obj[j].cigs, pets=drs_obj[j].pets, price=drs_obj[j].price)    
            drs_hist.save()
            drs_obj[j].delete()
        
        ride_obj = Ride.objects.filter(date__lt=datetime.date.today())
        for i in range(len(ride_obj)):
            ride_hist = Ride_hist(driver_username=ride_obj[i].driver_username, passenger_username=ride_obj[i].passenger_username, date=ride_obj[i].date, pick_up=ride_obj[i].pick_up, drop_off=ride_obj[i].drop_off)    
            ride_hist.save()
            ride_obj[i].delete()