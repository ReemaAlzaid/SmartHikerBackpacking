#Programmed by Reema Alzaid 
import numpy.random as npr
from errno import ERANGE
from posixpath import split
from random import randrange
import random
from tokenize import String
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import math
global generation
generation=0
fitnessPerGeneration=[]
Chromosomes=[]
global Population
Population = []
items= []
fittnssedList=[]
class item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.priority=0

class Chromosom:
    def __init__(self, chromosom, fitness):
        self.chromosom = chromosom
        self.fitness = fitness
    
    def __str__(self):

        return 'String: ' + str(self.chromosom) + ' Fitness: ' + str(self.fitness)

    """"
    Search space containing:

    i1=item("Sleeping bag",10) 
    i2=item("Rope",3)
    i3=item("Pocket Knife",2)
    i4=item("Torch",5)
    i5=item("Water Bottle",9)
    i6=item("Glucose",8)
    i7=item("First aid supplies",6)
    i8=item("Rain jacket",3)
    i9=item("Personal Locator Beacon",2)
    """

def Create_Initial_Population(pop: int,geneLength:int):
    global items
    i1=item("Sleeping bag",10) 
    i2=item("Rope",3)
    i3=item("Pocket Knife",2)
    i4=item("Torch",5)
    i5=item("Water Bottle",9)
    i6=item("Glucose",8)
    i7=item("First aid supplies",6)
    i8=item("Rain jacket",3)
    i9=item("Personal Locator Beacon",2)
    items=[i1,i2,i3,i4,i5,i6,i7,i8,i9] #Search space stored in
    oneChromosome=""
    for b in range(geneLength): #Insert one chromosome
        oneChromosome=oneChromosome+str(randrange(0,2))
    Population.append(Chromosom(oneChromosome,-1))
    p=1
    while p < pop: #Create random population
        p=p+1
        oneeChromosome=""
        for g in range(geneLength):
            oneeChromosome=oneeChromosome+str(randrange(0,2))

        if oneeChromosome =="000000000":
            p=p-1
            continue

        if oneeChromosome in (Population): #To check if there is no duplicates in the chromosome array
            p=p-1

        else:   
            Population.append(Chromosom(oneeChromosome,-1))

def Compute_Fitness(pop):
    fittnssedList=[]
    for p in pop: #Get all individuals in population
        weight=0
        pri=0
        second=0
        for g in range(len(items)):
            second=second+1
            if p.chromosom[g:second]=="1": #Check if the gene is one
                    pri=items[g].priority+pri
                    weight=items[g].weight+weight

        if weight<=30:
            p.fitness=pri
        else:
            p.fitness=0
  
    return pop
    
def Selection(population): #Selection roulette wheel selects only one
    total = sum([c.fitness for c in population]) #get the total fitness
    selection_probs = [c.fitness/total for c in population] #take each fitness and divided by one and store it in a list
    return population[npr.choice(len(population), p=selection_probs)] #return the chromosom

def crossover(pop):
    offspring=[]
    for i in range(int(len(pop)/2)):
        parent1= Selection(pop) #return only one chromosom by roulette wheel larger
        parent2= Selection(pop)
        child1= Chromosom("",-1)
        child2= Chromosom("",-1)

        split = random.randint(0,(len(items)-1)) #random split from 0 to 8
        child1.chromosom = parent1.chromosom[0:split] +  parent2.chromosom[split:(len(items))] 
        child2.chromosom = parent2.chromosom[0:split] +  parent1.chromosom[split:(len(items))]


        offspring.append(child1)
        offspring.append(child2)

    return offspring    
        
def mutation(pop):
    zerOrone=["0","1"]
    for item in pop:
        for index, param in enumerate(item.chromosom): #loops on the item chromosom gene by gene and store it's index in index and it's gene in param
            if random.uniform(0.0, 1.0) <= 0.1: #choose a random number from 0 to 1 with a rate of 0.1
                randomChoice=random.choice(zerOrone)
                item.chromosom = item.chromosom[0:index] + randomChoice+ item.chromosom[index+1:(len(items))]

    return pop

def calc(puplation):
    max=0
    avg=0
    global fitnessPerGeneration
    max = sum([c.fitness for c in puplation])
    avg=max/len(puplation)
    avg=avg/100
    fitnessPerGeneration.append(avg) 

def Replacement():
    global Population
    NewPop=[]
    NewPop=crossover(Population)
    NewPop=mutation(NewPop)
    NewPop=Compute_Fitness(NewPop)
    calc(NewPop)
    Population=[]
    Population=NewPop

def Termination():
    global gen
    gen=1
    while gen < 1000:
        Replacement()
        gen=gen+1

def main():
    Create_Initial_Population(60,9) #Random population is 60
    print("\nWelcome to the AI Software Company")
    i=-1
    while i < 8:
        i=i+1
        name=items[i].name
        choice=input("\nPlease choose on of the following priorities (Low=5 - Medium=10 - High=15) for: "+name+" ") #Get user priority for each item 

        if choice in ["10","15","5"]: #Input validation
            items[i].priority=int(choice)
        else:
            i=i-1
            print("\nInvalid choice, please try again")

    global puplation
    puplation=[]
    global Population
    puplation=Compute_Fitness(Population)
    calc(puplation)
    Population=puplation
    Termination() 
    print("\n".join(map(str,Population)))
    best=max([c.fitness for c in Population])
    bestBag=[c.chromosom for c in Population if c.fitness == best ]
    bestitems=[]
    index=0
    for index,gene in enumerate(bestBag[0]):
        if(gene=="1"):
            bestitems.append(items[index].name)

    print("\nBest items are: ",str(bestitems)+"\n\nWith a fitness of: ",best,"and a chromosom of: ",bestBag[0])

    x = np.arange(1,gen+1)
    y = np.array(fitnessPerGeneration)
    plt.title("Performance Graph")
    plt.ylabel("Fitness AVG")
    plt.xlabel("Generations")
    plt.ylim([0, 1])
    plt.plot(x, y, color='blue')
    plt.show()

if __name__ == '__main__':
    main()