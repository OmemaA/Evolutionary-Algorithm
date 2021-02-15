from EA import *


# File reading for KP
file = open("Knapsack\\low-dimensional\\f2_l-d_kp_20_878", "r")
no_items, capacity = map(int, file.readline().split())
items = []
index = 0
for line in file:
    items.append((int(line.split()[0]), int(line.split()[1]), index))
    index += 1
file.close()

class KP(EvolutionaryAlgorithm):
    def __init__(self):
        EvolutionaryAlgorithm.__init__(self)
        self.no_items = no_items
        self.items = items
        self.capacity = capacity

    def computeFitness(self, path):
        value, weight, index = 0, 0, 0
        # calculate the total weight and total value of chromosomes
        for exists in path:
            if exists == 1:
                value += self.items[index][0]
                weight += self.items[index][1]
            index += 1
        # if weight exceeds the capacity limit. Discard the chromosome
        if weight > self.capacity:
            return 0
        return value

    def initialPopulation(self):
        population = []
        for _ in range(self.popSize):
            indiv = []
            for _ in range(self.no_items):
                indiv.append(random.randint(0, 1))
            population.append(indiv)
        return population

    def crossover(self, parent1, parent2):
        # one point crossover
        # select a random range
        rand_range = random.randrange(0, len(parent1))
        # perform crossover on the range
        offspring1 = parent1[0:rand_range]
        offspring1.extend(parent2[rand_range:self.no_items])
        offspring2 = parent2[0:rand_range]
        offspring2.extend(parent1[rand_range:self.no_items])
        return offspring1, offspring2

    def mutation(self, population):
        # choose random gene and chromosome to perform mutation
        chromosome = random.randint(0, len(population) - 1)
        gene = random.randint(0, len(population[0]) - 1)
        # if bit is 1 swap it to 0 and vice versa
        if population[chromosome][gene] == 0:
            population[chromosome][gene] = 1
        else:
            population[chromosome][gene] = 0
        return population


kp = KP()
kp.cycle(True)