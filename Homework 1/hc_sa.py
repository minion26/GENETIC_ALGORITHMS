from hashlib import new
from re import A
import numpy as np
import time
import random
import math


start_time = time.time()
f=open("output.txt", "a")

def rastrigin(array) :
    result = 10.0 * len(array)
    for i in range(0, len(array)):
        result+=array[i]*array[i] - 10.0 * math.cos(2.0 * math.pi * array[i])
    return result

def dejong(array):
    sum = 0.0
    for i in range(0, len(array)):
        sum = sum + array[i]*array[i]
    return sum

def schwefel(array):
    sum = 0.0
    for i in range(0, len(array)):
        sum = sum + (-array[i]) * math.sin(math.sqrt(abs(array[i])))
    return sum

def michalewicz(array):
    sum(math.sin(i)* math.pow(math.sin((j*i**2)/math.pi),2*len(array)) for j,i in enumerate(array))
 



def decode(solution, a, b, ld)->int:
    res = binaryToDecimal(solution)
    res = res / (pow(2, ld)-1)
    res = res * (b-a)
    res = res + a 
    return res
    #return (a + binatodeci(solution))*(b-a)/(pow(2, no_of_bits)-1)

def binaryToDecimal(array_given)->int:
    sum = 0
    for idx, val in enumerate(reversed(array_given)):
        sum = sum + val * (2**idx)
    return sum


def generate_nbhd(solution)->list:  #length is the slicing length       
        vn = []
        #get the current param representation
         
        for line, entry in enumerate(solution):
            aux = solution.copy()
            if aux[line] == 1:
                aux[line] = 0
            else:
                aux[line] = 1
            vn.append(aux)
        return vn

def generate_current(N)->list:
    v_current = []
    for i in range(0,N):
        v_current.append(random.randint(0,1))
    return v_current
    

#print(paramsForFunction(nbhd, start, stop, ld))
#print("\033[1;32m This text is Bright Green  \n")

def first_improvment(nbhd, function_name, current_solution, a, b, ld):
    for entry in nbhd:
        listOfParams = []
        for i in range(0, len(entry), ld):
            listOfParams.append(decode(entry[i:i+ld], a,b,ld))
        solution = function_name(listOfParams)

        if solution < current_solution:
            return entry

def best_improvment(nbhd, function_name, current_solution,a, b, ld):
    best = []
    bestValue = current_solution
    for entry in nbhd:
        listOfParams = []
        for i in range(0, len(entry), ld):
            listOfParams.append(decode(entry[i:i+ld], a,b,ld))
        solution = function_name(listOfParams)

        if solution < current_solution:
            bestValue = solution
            best = entry.copy()
    
    if bestValue == current_solution:
        return None
    else:
        return best
        

def hillclimbing(iteration_number, ld, a,b,function_name, improvment_type):

    best = None
    bestlist = None

    for i in range(0, iteration_number):
        print(f'iteration number {i}')

        vc = generate_current(N)

        #transf into decimals
        param_list = []
        for i in range(0,len(vc),ld):
            param_list.append(decode(vc[i:i+ld],a,b,ld))
        
        current_sol = function_name(param_list)

        nbhd = generate_nbhd(vc)

        candidate = []

        candidate = improvment_type(nbhd, function_name, current_sol, a, b, ld)

        if candidate is not None:
            if best is None:
                
                best = candidate
            else:
                
                list = []
                for i in range(0, len(candidate), ld):
                    list.append(decode(candidate[i:i+ld], a,b,ld))

                mylist = []
                for i in range(0, len(best), ld):
                    mylist.append(decode(best[i:i+ld], a,b,ld))

                candidateSolution = function_name(list)
                bestSolution = function_name(mylist)
                if candidateSolution < bestSolution:
                    best =  candidate
                    bestlist = mylist

    f.write(f'Function: {function_name} \n bestValue: {str(function_name(bestlist))} \n improvmentType: {improvment_type} \n numberOfExecutions: {iteration_number} \n time: {(time.time() - start_time)} seconds')
    f.write(f'\n')
    return function_name(bestlist)


def simulatedAnnealing(iteration_number, temperature, ld, a,b,function_name, N):
    best = None
    candidateSolution = None
    bestSolution = None
    #temp_start = temperature

    while temperature > 0.00000001:
        print(f'iteration number {temperature}')

        vc = generate_current(N)
        
        #vn = vc.copy()
        canditate = []

        for i in range(0, iteration_number):
            vn = vc.copy()
            bitToNeg = random.randint(0, len(vc)-1)
            vn[bitToNeg] = not vn[bitToNeg]
            param = []

            parameters = []
            for i in range(0, N, ld):
                parameters.append(decode(vc[i:i+ld], a, b, ld))
            
            current_solution = function_name(parameters)

            for i in range(0, N, ld):
                param.append(decode(vn[i:i+ld], a, b, ld))

            vn_solution  = function_name(param)

            if vn_solution < current_solution:
                vc = vn
                # canditateBest = vn
            else:
                
                if random.random() < math.exp(-abs(vn_solution - current_solution) / temperature):
                    #canditateBest = vn
                    vc = vn
        
        canditate = vc
        temperature = temperature * 0.9

        if canditate is not None:
            if best is None:
                best = canditate
        else:
            list = []
            for i in range(0, len(canditate), ld):
                list.append(decode(canditate[i:i+ld], a,b,ld))

            mylist = []
            for i in range(0, len(best), ld):
                mylist.append(decode(best[i:i+ld], a,b,ld))

            candidateSolution = function_name(list)
            bestSolution = function_name(mylist)
            if candidateSolution < bestSolution:
                best = list

    return function_name(best)


# ----------------- 5 Dimension -------------------------------------
start_Rastrigin=-5.12
stop_Rastrigin=5.12
D = 5
eps = pow(10, -5)
no_numbers = (stop_Rastrigin - start_Rastrigin)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, first_improvment))
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, best_improvment))
print(simulatedAnnealing(100000, 1000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, N))

start_DeJong=-5.12
stop_DeJong=5.12
D=5
eps = pow(10, -5)
no_numbers = (stop_DeJong - start_DeJong)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, first_improvment))
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, best_improvment))
print(simulatedAnnealing(100000, 1000, ld, start_DeJong, stop_DeJong, dejong, N))


start_Michalewicz=0
stop_Michalewicz=math.pi
D=5
eps = pow(10, -5)
no_numbers = (stop_Michalewicz - start_Michalewicz)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, best_improvment))

start_Schwefel=-500
stop_Schwefel=500
D=5
eps = pow(10, -5)
no_numbers = (stop_Schwefel - start_Schwefel)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, best_improvment))

#----------10 Dimension-------------------------------------
start_Rastrigin=-5.12
stop_Rastrigin=5.12
D = 10
eps = pow(10, -5)
no_numbers = (stop_Rastrigin - start_Rastrigin)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, first_improvment))
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, best_improvment))

start_DeJong=-5.12
stop_DeJong=5.12
D=10
eps = pow(10, -5)
no_numbers = (stop_DeJong - start_DeJong)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, first_improvment))
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, best_improvment))

start_Michalewicz=0
stop_Michalewicz=math.pi
D=10
eps = pow(10, -5)
no_numbers = (stop_Michalewicz - start_Michalewicz)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, best_improvment))

start_Schwefel=-500
stop_Schwefel=500
D=10
eps = pow(10, -5)
no_numbers = (stop_Schwefel - start_Schwefel)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, best_improvment))

#-------------30 Dimension -------------------------------------------
start_Rastrigin=-5.12
stop_Rastrigin=5.12
D = 30
eps = pow(10, -5)
no_numbers = (stop_Rastrigin - start_Rastrigin)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, first_improvment))
print(hillclimbing(5000, ld, start_Rastrigin, stop_Rastrigin, rastrigin, best_improvment))

start_DeJong=-5.12
stop_DeJong=5.12
D=30
eps = pow(10, -5)
no_numbers = (stop_DeJong - start_DeJong)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, first_improvment))
print(hillclimbing(5000, ld, start_DeJong, stop_DeJong, dejong, best_improvment))

start_Michalewicz=0
stop_Michalewicz=math.pi
D=30
eps = pow(10, -5)
no_numbers = (stop_Michalewicz - start_Michalewicz)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Michalewicz, stop_Michalewicz, michalewicz, best_improvment))

start_Schwefel=-500
stop_Schwefel=500
D=30
eps = pow(10, -5)
no_numbers = (stop_Schwefel - start_Schwefel)*pow(10,5)
ld = math.trunc(math.log2(no_numbers))+1
N = ld * D 
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, first_improvment))
print(hillclimbing(5000, ld, start_Schwefel, stop_Schwefel, michalewicz, best_improvment))


