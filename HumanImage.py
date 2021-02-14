from EA import *
from PIL import Image
from PIL import ImageDraw
import numpy as np

image = Image.open("lisa.jpg").convert('L')
image_size = image.size
image_array = np.asarray(image, dtype=int)
# print(image_array.shape)
# print(image_array)
# image.show()

class Polygons:
    def __init__(self, polygons=None, colors=None):
        self.img = Image.new('L', image_size)
        self.shapes = 1000
        self.size = 10
        if polygons == None:
            self.polygons, self.colors = [], []
            for i in range(self.shapes):
                sides = int(randint(3,6))
                coords = []
                point = (randint(0, image_size[0]), randint(0, image_size[1]))
                for _ in range(sides):
                    coords.append((point[0]+randint(-self.size, self.size), \
                        point[1]+randint(-self.size, self.size)))
                self.colors.append(randint(0,255))
                self.polygons.append(coords)
                ImageDraw.Draw(self.img).polygon(self.polygons[i],self.colors[i])
        else:
            self.polygons, self.colors = polygons, colors
            for i in range(len(self.polygons)):
                ImageDraw.Draw(self.img).polygon(self.polygons[i],self.colors[i])
        self.img_array = np.asarray(self.img, dtype=int)


class HumanImage(EvolutionaryAlgorithm):
    def __init__(self):
        EvolutionaryAlgorithm.__init__(self)
        self.img = Image.new('L', image_size)

    def initialPopulation(self):
        print("Initializing Population")
        population = [Polygons() for _ in range(self.popSize)]
        return population

    def computeFitness(self, polygon):
        return np.sqrt(((image_array- polygon.img_array)**2).sum(axis=-1)).sum()

    def mutation(self, population):
        # changes color, swaps polygons or changes coordinates of polygon
        for i in population:
            index, selection = randint(0,i.shapes-1), randint(1,3)
            if selection == 1: # changes color
                i.colors[index] = randint(0,255)
            elif selection == 2: # swaps polygons
                swap = randint(0, i.shapes-1)
                i.polygons[index], i.polygons[swap] = i.polygons[swap], i.polygons[index]
            elif selection == 3: # changes coordinates of polygon
                sides = int(randint(3,6))
                coords = []
                point = (randint(0, image_size[0]), randint(0, image_size[1]))
                for _ in range(sides):
                    coords.append((point[0]+randint(-i.size, i.size), \
                        point[1]+randint(-i.size, i.size)))
                i.polygons[index] = coords
            # update chromosome
            i.img = Image.new('L', image_size)
            for p in range(i.shapes):
                ImageDraw.Draw(i.img).polygon(i.polygons[p],i.colors[p])
            i.img_array = np.asarray(i.img, dtype=int)
        # update fitness
        self.fitness = [self.computeFitness(indv) for indv in population]
        return population

    def crossover(self, parent1, parent2):
        # Order 1 crossover
        # print("-------CROSS OVER --------")
        total = parent1.size
        o1_polygons, o2_polygons = [None for _ in range(parent1.shapes)], [None for _ in range(parent1.shapes)]
        o1_colors, o2_colors = [None for _ in range(parent1.shapes)], [None for _ in range(parent1.shapes)]
        start = randint(0, ((total-1)//2))
        end = randint(start, (total-1))

        o1_polygons[start:end] = parent1.polygons[start:end]
        o1_colors[start:end] = parent1.colors[start:end]
        o2_polygons[start:end] = parent2.polygons[start:end]
        o2_colors[start:end] = parent2.colors[start:end]

        for i in range(parent1.shapes):
            if o1_polygons[i] == None:
                o1_polygons[i] = parent2.polygons[i]
                o1_colors[i] = parent2.colors[i]
            if o2_polygons[i] == None:
                o2_polygons[i] = parent1.polygons[i]
                o2_colors[i] = parent1.colors[i]
        offspring1 = Polygons(o1_polygons, o1_colors)
        offspring2 = Polygons(o2_polygons, o2_colors)
        return offspring1, offspring2


img = HumanImage()
img.cycle(False)
# print(img.computeFitness(i2))