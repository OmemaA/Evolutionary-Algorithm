import math, random
from random import randint
from copy import deepcopy
import matplotlib.pyplot as plt


# Base class
class EvolutionaryAlgorithm:
    def __init__(self):
        self.popSize = 30
        self.offsprings = 10
        self.generations = 100
        self.mutationRate = 0.5
        self.iterations = 10
        self.fitness = None
        self.generations_score = [[] for _ in range(self.generations)]

    # Dummy functions defined in child classes acc to each problem
    def initialPopulation(self):
        return [[] for _ in range(self.popSize)]

    def computeFitness(self, path):
        return 0

    def mutation(self, chromosomes):
        return chromosomes

    def crossover(self, parent1, parent2):
        return parent1, parent2
    
    # EA Cycle
    def cycle(self, maximise):
        generations = 0
        chromosomes = self.initialPopulation() 
        while generations < self.generations:
            if generations % 500 == 0:
                print("Saving image")
                for x in chromosomes:
                    fit = min([self.computeFitness(i) for i in chromosomes])
                    if self.computeFitness(x) == fit:
                        x.img.save('FBLogo'+str(generations)+'.png', 'PNG')
                        print("Fitness:", fit)
                        break

            # compute fitness of each individual in population
            self.fitness = [self.computeFitness(indv) for indv in chromosomes]
            print('Generation', generations+1)
            for _ in range(self.offsprings//2):
                # print("Parent Selection")
                # parent selection
                parents = self.BT(chromosomes, maximise, 2)
                parent1, parent2 = parents[0], parents[1]
                # cross over
                offspring1, offspring2  = self.crossover(parent1, parent2)
                # add new offsprings to population
                chromosomes.append(offspring1)
                chromosomes.append(offspring2)
                # compute fitness of new offsprings
                self.fitness.append(self.computeFitness(offspring1))
                self.fitness.append(self.computeFitness(offspring2))
                # mutation
                if random.random() < 0.5:
                    chromosomes = self.mutation(chromosomes)
            # survivor selection
            # print("Survivor Selection")
            chromosomes = self.truncation(chromosomes, maximise, self.popSize)
            # if maximise:
            #     BFS = max(self.fitness)
            # else:
            #     BFS = min(self.fitness)
            # AFS = sum(self.fitness)/len(self.fitness)
            # self.generations_score[generations].append((BFS, AFS))
            print(min(self.fitness))
            generations +=1
        # self.plot_graph()


    def plot_graph(self):
        BFS = [i[0][0] for i in self.generations_score]
        AFS = [i[0][1] for i in self.generations_score]
        generations = [i+1 for i in range(self.generations)]
        plt.plot(generations, BFS, label="Best-so-far Fitness")
        plt.plot(generations, AFS, label="Average Fitness")
        plt.title("BT and Truncation")
        plt.xlabel('No. of generations')
        plt.ylabel('Fitness value')
        plt.legend(loc="upper left")
        plt.show()
        

    # Selection procedures
    def FPS(self, chromosomes, maximise, size):
        # total fitness
        total = sum([val for val in self.fitness])
        # calculates ranges for chromosomes
        proportion = [val/total for val in self.fitness]
        # calculates cumulative probabilities
        prev_prob = 0
        probabilities = []
        for i in range(len(proportion)):
            prev_prob = prev_prob+proportion[i]
            probabilities.append(prev_prob)
        selected = []
        for _ in range(size):
            # selects two random numbers and chooses parents based on given range
            rand_no = random.random()
            for i in range(len(chromosomes)):
                if rand_no <= probabilities[i]:
                    selected.append(chromosomes[i])
                    break
        return selected

    def RBS(self, chromosomes, maximise, size):
        # assigns a rank to each chromosome acc to its fitness value
        ranks = list(range(len(self.fitness)))
        ranks.sort(key=lambda x: self.fitness[x])
        ranked_list = [0] * len(ranks)
        for i, x in enumerate(ranks):
            ranked_list[x] = i
        # total ranks
        total = sum([val for val in ranks])
        # calculates ranges for chromosomes
        proportion = [val/total for val in ranks]
        # calculates cumulative probabilities
        prev_prob = 0
        probabilities = []
        for i in range(len(proportion)):
            prev_prob = prev_prob+proportion[i]
            probabilities.append(prev_prob)
        selected = []
        for _ in range(size):
            # selects two random numbers and chooses chromosomes based on given range
            rand_no = random.random()
            for i in range(len(chromosomes)):
                if rand_no <= probabilities[i]:
                    selected.append(chromosomes[i])
                    break
        return selected
        

    def BT(self, chromosomes, maximise, size):
        selected = []
        if maximise:
            for _ in range(size):
                # randomly select two individuals
                rand = random.sample(range(0,len(chromosomes)), 2)
                # choose one with higher fitness value
                if self.fitness[rand[0]] > self.fitness[rand[1]]:
                    selected.append(chromosomes[rand[0]])
                selected.append(chromosomes[rand[1]])
        else:
            for _ in range(size):
                # randomly select two individuals
                rand = random.sample(range(0,len(chromosomes)), 2)
                # choose one with lower fitness value
                if self.fitness[rand[0]] < self.fitness[rand[1]]:
                    selected.append(chromosomes[rand[0]])
                selected.append(chromosomes[rand[1]])
        return selected
        

    def truncation(self, chromosomes, maximise, size):
        indexes = [(self.fitness[i], i) for i in range(len(self.fitness))]
        indexes.sort(key = lambda x: x[0], reverse=maximise)
        indexes = indexes[:size]
        top_N = [chromosomes[i[1]] for i in indexes]
        return top_N

    def random(self, chromosomes, size):
        return random.sample(chromosomes, size)

