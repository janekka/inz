from django.core.management.base import BaseCommand, CommandError
from drivers.models import Driver, Passenger, Ride
import numpy as np
from lpsolve55 import *
from lp_solve import *

class Command(BaseCommand):
    def handle(self, *args, **options):

#import danych z bazy
        drs = Driver.objects.all()
        ps = Passenger.objects.all()
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
