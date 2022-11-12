import numpy as np
import time
import random
import math
import timeit
import sys

population_size = 5 #chromosomes
numberGenerations = 1
kIndividuals = 10 
precision = 5
eps = pow(10, -5)
Dimension=5 # how many params has the function: 5, 10, 30
a = -5.12
b = 5.12
no_numbers = (b - a)*pow(10,5) #no of subintervals
ld = math.ceil(math.log2(no_numbers)) #len of the bitstring of one param
N = ld * Dimension #how many bits will have the list witch has all the params for the function, 5/10/30


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
    sum(math.sin(i)* math.pow(math.sin((j*i**2)/math.pi),2*len(array)) for j,i in enumerate(array))

#--------------fitness function---------------------------
def fitnessDejong(arr) -> float:
    sum = 0.0
    for i in range(0, len(arr)):
        sum = sum + arr[i]*arr[i]
    return 1/sum

def fitnessRastrigin(arr):
    pass

def fitnessSchwefel(arr):
    pass

def fitnessMichalewicz(arr):
    pass

#----------returns the solution in decimal in [a,b]---------
def decode(solution, a, b, ld)->int:
    res = binaryToDecimal(solution)
    res = res / (pow(2, ld)-1)
    res = res * (b-a)
    res = res + a 
    return res

#-------------transforms from bitstring to decimal----------
def binaryToDecimal(array_given)->int:
    sum = 0
    for idx, val in enumerate(reversed(array_given)):
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

#------decodes the bitstring to decimal to see if they are in [a,b]--------
# chr = []
# chr = firstGeneration(N)
# for i in range(0,N, ld):
#     print(decode((chr[i:i+ld], a,b,ld)))

#-------------mutation -> it changes one bit in one place with some probability----------
def mutation(population:list,ld:int):
    probability = random.random()
    if probability < 0.1 :
        randomGena = random.randint(0,ld-1)
        if population[randomGena] == 1:
            population[randomGena] = 0
        else:
            population[randomGena] = 1

    return population

#------------testing the mutation function------------
# chr = firstGeneration(N)
# pop = chr[1:1+ld]
# print(pop)
# print(mutation(pop, ld))

def cross_over(parent1:list, parent2:list, ld:int):
    cuttingPoint = random.randint(0,ld-1)

    same1 = parent1[0:cuttingPoint].copy()
    same2 = parent2[0:cuttingPoint].copy()

    changeToParent2 = parent1[cuttingPoint:ld].copy()
    changeToParent1 = parent2[cuttingPoint:ld].copy()

    desc1 = same1+changeToParent1
    desc2 = same2+changeToParent2
    return(desc1, desc2)

#------------testing the cross_over function------------
# chr = firstGeneration(N)
# parent1 = chr[0:ld]
# parent2 = chr[ld:2*ld]
# print(cross_over(parent1, parent2, ld))

def ga(start, stop, function_name, fitness_name, D, ld, N):

#-------first generation---------
    firstGen = firstGeneration(N)
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
        cumulative.append(cumulative[i-1]+probabilities[i])
    #---------------the selected chromosomes for the next steps------------------------------
    for i in range(0,population_size):
        randomProb.append(random.random())
        for j in range(0, population_size):
            if cumulative[j]>randomProb[i]:
                descendents.append(firstGen[i])
                break
            

    # print(descendents)
    # print(fitnessValues)
    # print(sumOfAllFitness)
    # print(probabilities)
    # print(functionValues)
    # print(sum)
    # print(cumulative)
    # print(randomProb)
    






        
ga(a,b,dejong, fitnessDejong, Dimension, ld, N)
