from EA import *

# File reading for TSP
f = open('QatarDataset.tsp', 'r')
lines = f.readlines()[7:]
cities = []
for i in range(194):
    x,y = lines[i].strip().split()[1:]
    cities.append([round(float(x)), round(float(y))])
f.close()

class TSP(EvolutionaryAlgorithm):
    def __init__(self):
        EvolutionaryAlgorithm.__init__(self)
        self.totalCities = 194
        self.citiesList = [(x,y) for x,y in cities]

    def distance(self, source, dest):
        distance = math.sqrt(((source[0] - dest[0])**2) + ((source[1] - dest[1])**2))
        return distance

    def initialPopulation(self):
        population = []
        for _ in range(self.popSize):
            chromosomes = []
            # randomly chooses cities from list to make path
            for _ in range(self.totalCities):
                chromosomes = random.sample(self.citiesList, len(self.citiesList))
            # appends all paths in population
            population.append(chromosomes)
        return population

    def computeFitness(self, path):
        size, fitness = 0, 0
        # sum of Euclidean distances between each city in path
        while size < (self.totalCities-1):
            fitness += self.distance(path[size],path[size+1])
            size += 1
        return fitness

    def mutation(self, population):
        # Swap mutation
        offspring1, offspring2 = randint(0, self.popSize), randint(0, self.popSize)
        # randomly selects 4 indexes to swap offsprings
        index1 = random.randint(0, self.totalCities-1)
        index2 = random.randint(0, self.totalCities-1)
        index3 = random.randint(0, self.totalCities-1)
        index4 = random.randint(0, self.totalCities-1)
        population[offspring1][index1], population[offspring1][index2] = \
            population[offspring1][index2], population[offspring1][index1]
        population[offspring2][index3], population[offspring2][index4] = \
            population[offspring2][index4], population[offspring2][index3]
        return population

    def crossover(self, parent1, parent2):
        # Order 1 crossover
        total = len(parent1)
        offspring1 = [None for i in range(total)]
        offspring2 = [None for i in range(total)]
        start = random.randint(0, ((total-1)//2))
        end = random.randint(start, (total-1))
        for i in range(start, end):
            offspring1[i], offspring2[i] = parent1[i], parent2[i]
        o1_idx, p1_idx, o2_idx, p2_idx = end, end, end, end
        # fills remaining chromosomes starting from end of parents
        while offspring1[o1_idx] == None:
            if parent2[p2_idx] in offspring1:
                p2_idx = (p2_idx+1) % total
                continue
            if parent1[p1_idx] in offspring2:
                p1_idx = (p1_idx+1) % total
                continue
            offspring1[o1_idx] = parent2[p2_idx]
            offspring2[o2_idx] = parent1[p1_idx]
            # finds unique chromosomes in parent
            o1_idx, o2_idx = (o1_idx+1) % total, (o2_idx+1) % total
            p1_idx, p2_idx = (p1_idx+1) % total, (p2_idx+1) % total
        return offspring1, offspring2


tsp = TSP()
tsp.cycle(False)