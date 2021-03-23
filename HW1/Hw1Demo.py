# Class to handle inputs from GUI
import random
import csv
import matplotlib.pyplot as plt
SEED=42
N=100
# genNumber = 200
random.seed(SEED)
generations=[]
best=[]
average=[]
mins=[]
fieldNames = ['Generation', 'Max', 'Average', 'Min']
# crossfile = "crossover.csv"
# mutfile = "mutations.csv"
# elitefile ="elite.csv"
# crossIssue = "part10part4.csv"
demoFile ="demo.csv"


class Simulation:
    def __init__(self, mutRate, eliteRate, crossOverVal, genLength):
        self.mutRate = mutRate/100 # user enters 50
        self.eliteRate = eliteRate
        self.crossOverVal = crossOverVal
        self.genNumber = genLength
        entirePop = []
        for i in range(N):
            entirePop.append(self.generateSeed())

        self.sortedList = self.sortPopulation(entirePop)


    def runSim(self):
        # print("Running Sim ")
        initialSortedPop = self.sortedList
        with open(demoFile, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
            writer.writerow({fieldNames[0]: fieldNames[0], fieldNames[1]: fieldNames[1], fieldNames[2]: fieldNames[2],
                             fieldNames[3]: fieldNames[3]})
            for i in range(self.genNumber):
                top50 = initialSortedPop[int(N/2 -1):len(initialSortedPop)-1]
                newGen = []
                top50Clone = top50.copy()
                # studs=[]
                if self.eliteRate != 0: # hopefully just a nested list and nothing more
                    studs= (initialSortedPop[len(initialSortedPop)-self.eliteRate:len(initialSortedPop)]) # Elite
                for j in range(len(top50Clone) - 1):
                    top50Clone[j] = self.randFlip(top50Clone[j], self.mutRate) # mutate the parents
                # for j in range(len(top50Clone)-1):
                #     newGen.append(top50Clone[j])
                for j in range(len(top50)):
                    newGen.append(top50[j])
                if self.crossOverVal == True:
                    for j in range(len(top50Clone) - 1-self.eliteRate):  # The stud will breed with all the top 50 except himself
                        child = self.crossoverMethod(initialSortedPop[len(initialSortedPop)-1], top50Clone[j])
                        # child = self.randFlip(child,self.mutRate)
                        newGen.append(child)
                        newGen.append(top50Clone[j])
                    if self.eliteRate == 0:
                        extraChild = self.crossoverMethod(initialSortedPop[len(initialSortedPop) - 2],
                                                 initialSortedPop[len(initialSortedPop) - 3])
                        newGen.append(extraChild)  # the next best candidates breed
                else:
                    for j in range(len(top50Clone)-self.eliteRate):
                        newGen.append(top50Clone[j])
                        # print("Elite Rate: ",self.eliteRate)
                        # print("Length of new generation after false CrossOver: ", len(newGen))
                if self.eliteRate != 0:
                    for chromosome in studs:
                        newGen.append(chromosome)
                # print("Length of new generation after everything: ", len(newGen))
                sortedGenList = self.sortPopulation(newGen)
                genFitnessValues = []
                for j in range(N):
                    genFitnessValues.append(self.countOnes(sortedGenList[j]))
                print(
                    "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                print("Generation ", i, ":")
                print("Fitness values: ", genFitnessValues)
                print("Best fitness Value: ", genFitnessValues[len(genFitnessValues) - 1])
                print("Worst fitness Value: ", genFitnessValues[0])
                print(
                    "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

                initialSortedPop = newGen
                max = genFitnessValues[len(genFitnessValues) - 1]
                avg = self.calcAverage(genFitnessValues)
                min = genFitnessValues[0]
                writer.writerow({fieldNames[0]: i, fieldNames[1]: max, fieldNames[2]: avg,
                                 fieldNames[3]: min})
        self.plotCases()
    def generateSeed(self):
        chromosome = []
        for i in range(N):
            if random.randint(0, 1) == 1:
                chromosome.append(1)
            else:
                chromosome.append(0)
        return chromosome

    def randFlip(self, oneStrand, mutationRate):
        mutatedCopy = []
        for i in range(N):
            if random.randint(1, 100) > mutationRate * 100:
                mutatedCopy.append(oneStrand[i])
            else:
                # print("mutated")
                if oneStrand[i] == 1:
                    mutatedCopy.append(0)
                else:
                    mutatedCopy.append(1)

        return mutatedCopy

    def crossoverMethod(self, father, mother):
        child = []
        if random.randint(0, 1) == 1:
            for i in range(N - 50):
                child.append(father[i])
                # print("father i: ", i)
            for i in range(N - 50, N):
                # print("Mother i: ",i)
                child.append(mother[i])
        else:
            for i in range(N - 50):
                child.append(mother[i])
            for i in range(N - 50, N):
                child.append(father[i])

        return child

    def sortPopulation(self, entirePop):
        for i in range(N):
            minIndex = i
            # print(i)
            for j in range(i + 1, N):
                # print("THis is j: ", j )
                if self.countOnes(entirePop[minIndex]) > self.countOnes(entirePop[j]):
                    minIndex = j
            entirePop[i], entirePop[minIndex] = entirePop[minIndex], entirePop[i]

        return entirePop

    def calcAverage(self, fitnessValues):
        sum = 0
        for i in range(len(fitnessValues)):
            sum += fitnessValues[i]
        return int(sum / len(fitnessValues))

    def generateSeed(self):
        chromosome = []
        for i in range(N):
            if random.randint(0, 1) == 1:
                chromosome.append(1)
            else:
                chromosome.append(0)
        return chromosome

    def countOnes(self,oneStrand):
        fitnessValue = 0
        for i in range(N):
            if oneStrand[i] == 1:
                fitnessValue += 1
        return fitnessValue

    def plotCases(self):
        generations.clear()
        best.clear()
        average.clear()
        mins.clear()
        plt.figure()
        with open(demoFile, newline='') as csvfile:
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

        plt.savefig('demoFile.png')
        plt.show()
