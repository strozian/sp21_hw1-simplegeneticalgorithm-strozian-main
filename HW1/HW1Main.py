import random
import csv
import matplotlib.pyplot as plt
SEED=42
N=100
genNumber = 200
random.seed(SEED)
rate = N
fieldNames = ['Generation', 'Max', 'Average', 'Min']
generations=[]
best=[]
average=[]
mins=[]

crossfile = "crossover.csv"
mutfile = "mutations.csv"
elitefile ="elite.csv"
crossIssue = "part10part4.csv"
highMut ="highMutationRate.csv"
lowMut ="lowMutationRate.csv"



def main():
    entirePop = []
    for i in range(N):
        entirePop.append(generateSeed())

    sortedList = sortPopulation(entirePop)

    """
    These lines of code will print the generations and their fitness scores to the consoles.
    Uncomment one at a time.Otherwise you will be inundated with comments on the console.
    """
    # loopMutations(sortedList) # Uncomment these to get the different graphs for the assignment. THis is for the only mutations
    loopElitism(sortedList) # The elitism part
    # crossoverLoop(sortedList) # The crossover part
    # crossIssuesLoop(sortedList) # One of my experiments for the word document


def countOnes(oneStrand):
    fitnessValue = 0
    for i in range(N):
        if oneStrand[i] == 1:
            fitnessValue += 1
    return fitnessValue

def loopMutations(sortedList):
    with open(mutfile, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writerow({fieldNames[0]:fieldNames[0],fieldNames[1]:fieldNames[1],fieldNames[2]:fieldNames[2],fieldNames[3]:fieldNames[3]})
        initialSortedPop = sortedList
        for i in range(genNumber):
            top50 = initialSortedPop[int(N/2 -1):len(initialSortedPop)-1]
            newGen = []
            top50Clone = top50.copy()
            for j in range(len(top50Clone) - 1):
                top50Clone[j] = randFlip(top50Clone[j], 1 / rate)
            for j in range(len(top50Clone)):
                newGen.append(top50Clone[j])
            for j in range(len(top50)):
                newGen.append(top50[j])
            sortedGenList = sortPopulation(newGen)
            genFitnessValues = []
            for j in range(N):
                genFitnessValues.append(countOnes(sortedGenList[j]))
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("Generation ", i, ":")
            print("Fitness values: ", genFitnessValues)
            print("Best fitness Value: ", genFitnessValues[len(genFitnessValues) - 1])
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            initialSortedPop = newGen
            max = genFitnessValues[len(genFitnessValues) - 1]
            avg = calcAverage(genFitnessValues)
            min = genFitnessValues[0]
            writer.writerow({fieldNames[0]: i, fieldNames[1]: max, fieldNames[2]: avg,
                             fieldNames[3]: min})

def loopElitism(sortedList):
    with open(elitefile, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writerow({fieldNames[0]:fieldNames[0],fieldNames[1]:fieldNames[1],fieldNames[2]:fieldNames[2],fieldNames[3]:fieldNames[3]})
        initialSortedPop = sortedList
        for i in range(genNumber):
            top50 = initialSortedPop[int(N/2 -1):len(initialSortedPop)-1]
            newGen = []
            top50Clone = top50.copy()
            stud = initialSortedPop[len(initialSortedPop)-1]
            for j in range(len(top50Clone) - 1):
                top50Clone[j] = randFlip(top50Clone[j], 1 / rate) # mutate
            for j in range(len(top50Clone)-1):
                newGen.append(top50Clone[j])
            for j in range(len(top50)):
                newGen.append(top50[j])
            newGen.append(stud)
            print("Length of new generation: ", len(newGen))
            sortedGenList = sortPopulation(newGen)
            genFitnessValues = []
            for j in range(N):
                genFitnessValues.append(countOnes(sortedGenList[j]))

            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("Generation ", i, ":")
            print("Previous Elite Fitness Score",countOnes(stud))
            print("New Fitness values: ", genFitnessValues)
            print("New Elite Value: ", genFitnessValues[len(genFitnessValues) - 1])
            # print("Length of new generation: ", len(top50))
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            initialSortedPop = newGen
            max = genFitnessValues[len(genFitnessValues) - 1]
            avg = calcAverage(genFitnessValues)
            min = genFitnessValues[0]

            writer.writerow({fieldNames[0]: i, fieldNames[1]: max, fieldNames[2]: avg,
                             fieldNames[3]: min})





def crossoverLoop(sortedList):
    with open(crossfile, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writerow({fieldNames[0]:fieldNames[0],fieldNames[1]:fieldNames[1],fieldNames[2]:fieldNames[2],fieldNames[3]:fieldNames[3]})
        initialSortedPop = sortedList
        for i in range(genNumber):
            # print(N/2 -1)
            top50 = initialSortedPop[int(N/2 -1):len(initialSortedPop)-1]
            stud = initialSortedPop[len(initialSortedPop) - 1]
            newGen = []
            for j in range(len(top50)-1): # The stud will breed with all the top 50 except himself
                child = crossoverMethod(stud, top50[j])
                child = randFlip(child, 1/rate)
                newGen.append(child)
                newGen.append(top50[j])
            extraChild = crossoverMethod(initialSortedPop[len(initialSortedPop) - 2],initialSortedPop[len(initialSortedPop) - 3])
            newGen.append(extraChild) # the next best candidates breed
            newGen.append(stud)
            sortedGenList = sortPopulation(newGen)
            genFitnessValues = []
            for j in range(N):
                genFitnessValues.append(countOnes(sortedGenList[j]))
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("Generation ", i, ":")
            print("Breeder Fitness Score", countOnes(stud))
            print("New Fitness Values: ", genFitnessValues)
            print("New Breeder Value: ", genFitnessValues[len(genFitnessValues) - 1])
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            initialSortedPop = newGen
            max =  genFitnessValues[len(genFitnessValues) - 1]
            avg = calcAverage(genFitnessValues)
            min =  genFitnessValues[0]

            writer.writerow({fieldNames[0]: i, fieldNames[1]: max, fieldNames[2]: avg,
                             fieldNames[3]: min})



def generateSeed():
    chromosome = []
    for i in range(N):
        if random.randint(0,1) == 1:
            chromosome.append(1)
        else:
            chromosome.append(0)
    return chromosome

def randFlip(oneStrand, mutationRate):
    mutatedCopy =[]
    for i in range(N):
        if random.randint(1,100) > mutationRate*100:
            mutatedCopy.append(oneStrand[i])
        else:
            # print("mutated")
            if oneStrand[i] == 1:
                mutatedCopy.append(0)
            else:
                mutatedCopy.append(1)

    return mutatedCopy

def crossoverMethod(father, mother):
    child = []
    if random.randint(0,1) == 1:
        for i in range(N-50):
            child.append(father[i])
            # print("father i: ", i)
        for i in range(N-50, N):
            # print("Mother i: ",i)
            child.append(mother[i])
    else:
        for i in range(N - 50):
            child.append(mother[i])
        for i in range(N-50,N):
            child.append(father[i])

    return child

def sortPopulation(entirePop):
    for i in range(N):
        minIndex = i
        # print(i)
        for j in range(i+1, N):
            # print("THis is j: ", j )
            if countOnes(entirePop[minIndex]) > countOnes(entirePop[j]):
                minIndex =j
        entirePop[i], entirePop[minIndex] = entirePop[minIndex], entirePop[i]

    return entirePop

def calcAverage(fitnessValues):
    sum =0
    for i in range(len(fitnessValues)):
        sum += fitnessValues[i]
    return int(sum/len(fitnessValues))





def plotCases():
    with open(crossfile, newline='') as csvfile:
        # Using the csv reader automatically places all values
        # in columns within a row in a dictionary with a
        # key based on the header (top line of the file)
        reader = csv.DictReader(csvfile)
        for row in reader:
            generations.append(row["Generation"])
            best.append(int(row["Max"]))
            average.append(int(row["Average"]))
            mins.append(int(row["Min"]))

    plt.plot(generations, best, label="best")
    plt.plot(generations, average, label="average")
    plt.plot(generations, mins, label="min")

    plt.legend()
    plt.xlabel('generations')
    plt.ylabel('fitness')

    plt.savefig('crossfile.png')
    plt.show()

    with open(mutfile, newline='') as csvfile:
        generations.clear()
        best.clear()
        average.clear()
        mins.clear()
        # Using the csv reader automatically places all values
        # in columns within a row in a dictionary with a
        # key based on the header (top line of the file)
        reader = csv.DictReader(csvfile)
        for row in reader:
            generations.append(row["Generation"])
            best.append(int(row["Max"]))
            average.append(int(row["Average"]))
            mins.append(int(row["Min"]))

    plt.plot(generations, best, label="best")
    plt.plot(generations, average, label="average")
    plt.plot(generations, mins, label="min")

    plt.legend()
    plt.xlabel('generations')
    plt.ylabel('fitness')

    plt.savefig('mutfile.png')
    plt.show()

    with open(crossIssue, newline='') as csvfile:
        generations.clear()
        best.clear()
        average.clear()
        mins.clear()
        # Using the csv reader automatically places all values
        # in columns within a row in a dictionary with a
        # key based on the header (top line of the file)
        reader = csv.DictReader(csvfile)
        for row in reader:
            generations.append(row["Generation"])
            best.append(int(row["Max"]))
            average.append(int(row["Average"]))
            mins.append(int(row["Min"]))

    plt.plot(generations, best, label="best")
    plt.plot(generations, average, label="average")
    plt.plot(generations, mins, label="min")

    plt.legend()
    plt.xlabel('generations')
    plt.ylabel('fitness')

    plt.savefig('crossIssue.png')
    plt.show()

    with open(elitefile, newline='') as csvfile:
        generations.clear()
        best.clear()
        average.clear()
        mins.clear()
        # Using the csv reader automatically places all values
        # in columns within a row in a dictionary with a
        # key based on the header (top line of the file)
        reader = csv.DictReader(csvfile)
        for row in reader:
            generations.append(row["Generation"])
            best.append(int(row["Max"]))
            average.append(int(row["Average"]))
            mins.append(int(row["Min"]))

    plt.plot(generations, best, label="best")
    plt.plot(generations, average, label="average")
    plt.plot(generations, mins, label="min")

    plt.legend()
    plt.xlabel('generations')
    plt.ylabel('fitness')

    plt.savefig('elitefile.png')
    plt.show()

def crossIssuesLoop(sortedList):
    with open(crossIssue, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writerow({fieldNames[0]:fieldNames[0],fieldNames[1]:fieldNames[1],fieldNames[2]:fieldNames[2],fieldNames[3]:fieldNames[3]})
        initialSortedPop = sortedList
        for i in range(genNumber):
            # print(N/2 -1)
            top50 = initialSortedPop[int(N/2 -1):len(initialSortedPop)-1]
            stud = initialSortedPop[len(initialSortedPop) - 1]
            newGen = []
            for j in range(len(top50)-1): # The stud will breed with all the top 50 except himself
                child = crossoverMethod(stud, top50[j])
                newGen.append(child)
                newGen.append(top50[j])
            extraChild = crossoverMethod(initialSortedPop[len(initialSortedPop) - 2],initialSortedPop[len(initialSortedPop) - 3])
            newGen.append(extraChild) # the next best candidates breed
            newGen.append(stud)
            sortedGenList = sortPopulation(newGen)
            genFitnessValues = []
            for j in range(N):
                genFitnessValues.append(countOnes(sortedGenList[j]))
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("Generation ", i, ":")
            print("Crossover Elite Fitness Score", countOnes(stud))
            print("New Fitness Values: ", genFitnessValues)
            print("New Best Crossover Value: ", genFitnessValues[len(genFitnessValues) - 1])
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

            initialSortedPop = newGen
            max =  genFitnessValues[len(genFitnessValues) - 1]
            avg = calcAverage(genFitnessValues)
            min =  genFitnessValues[0]

            writer.writerow({fieldNames[0]: i, fieldNames[1]: max, fieldNames[2]: avg,
                             fieldNames[3]: min})













































main()
plotCases()