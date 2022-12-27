import numpy as np
import time
import random
import math
import timeit
import sys
start_time = time.time()
f=open("output2.txt", "a")

population_size = 200 #chromosomes
numberGenerations = 1000

#-----------FUNCTIONS---------------
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
    return sum(math.sin(i)* math.pow(math.sin((j*i**2)/math.pi),2*len(array)) for j,i in enumerate(array))

#--------------fitness function---------------------------
def fitnessDejong(arr) -> float:
    sum = 0.000000000000000000000001
    for i in range(0, len(arr)):
        sum = sum + arr[i]*arr[i]
    return 1/sum

def fitnessRastrigin(arr):
    sum = 0.00000000000000000001
    sum = sum + rastrigin(arr)
    return 1/sum

def fitnessSchwefel(arr):
    sum = 0.00000000000000000001
    sum = sum + schwefel(arr)
    return 1/sum
    

def fitnessMichalewicz(arr):
    sum = 0.00000000000000000001
    sum = sum + michalewicz(arr)
    return 1/sum


def XOR(x:float, y:float):
    if x == y :
        return 0.0
    else:
        return 1.0
    
#----------returns the solution in decimal in [a,b]---------
def decode(solution:list, a, b, ld)->int:
    res = binaryToDecimal(solution)
    res = res / (pow(2, ld)-1)
    res = res * (b-a)
    res = res + a 
    return res

#-------------transforms from bitstring to decimal----------
def binaryToDecimal(array_given)->int:
    gray = []
    gray.append(array_given[0])
    for i in range(1, len(array_given)):
        if array_given[i] == 0.0:
            gray.append(gray[i-1])
        else:
            gray.append(1.0 - gray[i-1])
    
    sum = 0
    for idx, val in enumerate(reversed(gray)):
        sum = sum + val * (2**idx)
    return sum


#-----------generate random the first generation----------

def firstGeneration(N)->list:
    generation_current = []

    for j in range(0, population_size):
        v_current = []
        for i in range(0,N):
            v_current.append(random.randint(0,1))
        generation_current.append(v_current)

    return generation_current

#-------------mutation -> it changes one bit in one place with some probability----------
def mutation(population:list, ld:int, mutationChance):
    gene = random.randint(0,ld-1)
    probability = random.random()
    if probability <= mutationChance :
        if population[gene] == 1:
            population[gene] = 0
        else:
            population[gene] = 1

    return population

#----------------------cross over--------------------------
def cross_over(parent1:list, parent2:list, ld:int):
    cuttingPoint = random.randint(0,ld-1)

    same1 = parent1[0:cuttingPoint].copy()
    same2 = parent2[0:cuttingPoint].copy()

    changeToParent2 = parent1[cuttingPoint:ld].copy()
    changeToParent1 = parent2[cuttingPoint:ld].copy()

    desc1 = same1+changeToParent1
    desc2 = same2+changeToParent2
    return(desc1, desc2)

#---------------creating a list with probability for cross over
def chromCrossOver():
    Rate = []
    for k in range(0, population_size):
        rate = random.random()
        Rate.append(rate)
    
    return Rate


def selection(start, stop, function_name, fitness_name, D, ld, N, firstGen):

#-------there are D chromosomes, D = dimensions of function-------
    fitnessValues = [] #values of fitness function with every chromosomes
    functionValues = [] #values of function in these chromosomes
    sumOfAllFitness = 0 #sum of all fitness, helping with the cumulative list for selection
    probabilities = [] #the probability that we'll choose that chromosome
    cumulative = [] #for the selection roulette 
    randomProb = [] #random prob
    descendents = [] #the survivors for the next steps
    PARAMS = [] #list with the params in float form


    for i in range(0, population_size):
        param = []
        listofallparam = []
        #------------decode the bitstring for the fitness and the main function---------------
        for j in range(0,N,ld):
            listofallparam.append((decode(firstGen[i][j:j+ld],start,stop,ld)))

        #------------list of chromosomes-----------------------------------------------------
        for k in range(0,population_size,D):
            PARAMS.append(listofallparam[k:k+D])

        #------------a list with all the fitness result with all the chromosomes--------------
        fitnessValues.append(fitness_name(PARAMS[i]))

        #------------sum for all to help us with the probability------------------------------
        sumOfAllFitness = sumOfAllFitness + fitness_name(PARAMS[i])

        #------------a list with all the function result with all the chromosomes------------
        functionValues.append(function_name(PARAMS[i]))


    #---------------probability to choose the chromosome-------------------------------------
    for i in range(0,population_size):
        probabilities.append(fitness_name(PARAMS[i])/sumOfAllFitness)

    #---------------creating the cumulative--------------------------------------------------
    cumulative.append(probabilities[0])
    for i in range(1,population_size):
        cumulative.append(cumulative[i-1]+probabilities[i-1])

    #---------------the selected chromosomes for the next steps------------------------------
    for i in range(0,population_size):
        randomProb.append(random.random())
        for j in range(0, population_size-1):
            if (cumulative[j] < randomProb[i] and randomProb[i] <= cumulative[j+1]) or (randomProb[i] < cumulative[j]):
                descendents.append(firstGen[i])
                break

            
    if len(descendents) < population_size: 
        for j in range(len(descendents), population_size):
            descendents.append(firstGen[j])
            

    return descendents



def ga(start, stop, N, ld, Dimension, function_name, fitness_name, crossoverRate, mutationChance, MINIM):
    firstGen = firstGeneration(N)
    # print(len(firstGen))
    for i in range(0, numberGenerations):
        offSpring = selection(start, stop, function_name, fitness_name, Dimension, ld, N, firstGen)
        # print(offSpring,end='\n')
        for chrom in offSpring:
            for j in range(0, N, ld):
                # print(len(offSpring[i][j:j+ld]))
                param = chrom[j:j+ld]
                #mutation(offSpring[i][j:j+ld], ld)
                mutation(param, ld, mutationChance)
                # print("a mers mutatia")
            
        
        # print(len(offSpring))
        rate = chromCrossOver()
        
        for indx,chromo in enumerate(offSpring):
            if indx != len(offSpring)-1:
                
                for j in range(0, N, ld*2):
                    if rate[indx+1] < crossoverRate:
                        param1 = chromo[j:j+ld]
                        param2 = chromo[j+ld:j+2*ld]
                        cross_over(param1,param2,ld)
                        # print("a mers cross_over")
                            # print(ld)
                            # return(offSpring[i][j:j+ld])
                    else:
                        randomVal = random.random()
                        if randomVal == 1:
                            # print("a mers cross_over 2")
                            param1 = chromo[j:j+ld]
                            param2 = chromo[j+ld:j+2*ld]
                            cross_over(param1,param2,ld)
                            # cross_over(offSpring[i][j:j+ld], offSpring[i+1][j+1:j+1+ld], ld)
        # firstGen = offSpring
                            
        #--------------modifiyng the mutation chance----------------
        mutationChance = mutationChance * 0.99
        if mutationChance < 0.01 :
            mutationChance = 0.01

        #--------------modifiyng the cross over rate-----------------
        crossoverRate = crossoverRate * 1.01
        if crossoverRate > 2.0 :
            crossoverRate = 2.0    
   
    min=0
    minj = 0
    for i in range(0, population_size):
        for j in range(0, N, ld):
            # print( offSpring[i][j:j+ld])
            # print(offSpring[min][j:j+ld])
            # print("j")
            # print(decode(offSpring[i][j:j+ld], start, stop, ld))
            # print("min")
            # print(decode(offSpring[min][j:j+ld], start, stop, ld))
            actualVal = decode(offSpring[i][j:j+ld], start, stop, ld)
            minVal = decode(offSpring[min][minj:minj+ld], start, stop, ld)
            if actualVal < MINIM:
                if actualVal > minVal:
                    min = i
                    minj = j
            else:
                if actualVal < minVal:
                    min = i
                    minj = j
            print(actualVal, minVal, len(offSpring), function_name(offSpring[min][minj:minj+ld]), mutationChance, crossoverRate) 

    
    f.write(f'Function: {function_name} \n minimum value: {function_name(offSpring[min][minj:minj+ld]), minVal} \n numberOfGeneration: {numberGenerations} \n populationSize: {population_size} \n dimension: {Dimension} \n time: {(time.time() - start_time)} seconds')
    f.write(f'\n')
    f.write(f'\n')
    return minVal
    # return 0


# --------------------------------------------------------------------
start_Rastrigin=-5.12
stop_Rastrigin=5.12 
# D = 5
eps = pow(10, -5)
no_numbers = (stop_Rastrigin - start_Rastrigin)*pow(10,5)
ld = math.ceil(math.log2(no_numbers))
# N = ld * D
for k in range(0,1):
    print(k) 
    print(ga(start_Rastrigin, stop_Rastrigin, ld*5, ld, 5, rastrigin, fitnessRastrigin, 0.1,0.7, 0))
    print(ga(start_Rastrigin, stop_Rastrigin, ld*10, ld, 10, rastrigin, fitnessRastrigin, 0.1,0.7, 0))
    print(ga(start_Rastrigin, stop_Rastrigin, ld*30, ld, 30, rastrigin, fitnessRastrigin, 0.1,0.7, 0))


start_DeJong=-5.12
stop_DeJong=5.12
# D=5
eps = pow(10, -5)
no_numbers = (stop_DeJong - start_DeJong)*pow(10,5)
ld = math.ceil(math.log2(no_numbers))
# N = ld * D 

for k in range(0,1):
    print(k)
    print(ga(start_DeJong, stop_DeJong, ld*5, ld, 5, dejong, fitnessDejong, 0.1, 0.7, 0))
    print(ga(start_DeJong, stop_DeJong, ld*10, ld, 10, dejong, fitnessDejong, 0.1,0.7, 0))
    print(ga(start_DeJong, stop_DeJong, ld*30, ld, 30, dejong, fitnessDejong, 0.1,0.7, 0))


start_Michalewicz=0
stop_Michalewicz=math.pi
# D=5
eps = pow(10, -5)
no_numbers = (stop_Michalewicz - start_Michalewicz)*pow(10,5)
ld = math.ceil(math.log2(no_numbers))
# N = ld * D 
for k in range(0,1):
    print(k)
    print(ga(start_Michalewicz, stop_Michalewicz, ld*5, ld, 5, michalewicz, fitnessMichalewicz, 0.1,0.7, -4.687))
    print(ga(start_Michalewicz, stop_Michalewicz, ld*10, ld, 10, michalewicz, fitnessMichalewicz, 0.1,0.7, -9.66))
    print(ga(start_Michalewicz, stop_Michalewicz, ld*30, ld, 30, michalewicz, fitnessMichalewicz, 0.1,0.7, -9.66))


start_Schwefel=-500
stop_Schwefel=500
# D=5
eps = pow(10, -5)
no_numbers = (stop_Schwefel - start_Schwefel)*pow(10,5)
ld = math.ceil(math.log2(no_numbers))
# N = ld * D 
for k in range(0,1):
    print(k)
    print(ga(start_Schwefel, stop_Schwefel, ld*5, ld, 5, schwefel, fitnessSchwefel, 0.1,0.7, -2094.9145))
    print(ga(start_Schwefel, stop_Schwefel, ld*10, ld, 10, schwefel, fitnessSchwefel, 0.1,0.7, -4189.829))
    print(ga(start_Schwefel, stop_Schwefel, ld*30, ld, 30, schwefel, fitnessSchwefel, 0.1,0.7, -12569.497))

