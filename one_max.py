import random
import copy
import numpy as np

GENOM_LENGTH = 100
MAX_GENOM_LIST = 10000
SELECT_GENOM = 2000
INDIVIDUAL_MUTATION = 0.1  # 個体に突然変異が起きる確率を表す
GENOM_MUTATION = 0.1  # 突然変異が起きた個体について、各々の遺伝子が変異する確率を表す
MAX_ITER = 50
ATGC = [i for i in range(100)]


class Gene:
    def __init__(self):
        self.chromosome = [random.choice(ATGC) for i in range(GENOM_LENGTH)]


    def __repr__(self):
        return "<<{}>>".format(",".join([str(i) for i in self.chromosome]))

    def mutate(self):
        for i in range(len(self.chromosome)):
            if random.random() < GENOM_MUTATION:
                self.chromosome[i] = random.choice(ATGC)


class Ecoli:
    def __init__(self):
        self.gene = Gene()

    def evaluate(self):
        chromosome_np = np.asarray(self.gene.chromosome)
        return 1 / (np.sum((chromosome_np - np.arange(100))**2)+1e-5)#連番

    def mutate(self, force=False):
        if force or random.random() < INDIVIDUAL_MUTATION:
            self.gene.mutate()


def crossOver(Ecoli1, Ecoli2, i=None, j=None):
    if i == None and j == None:
        _i = random.randint(0, GENOM_LENGTH)
        _j = random.randint(0, GENOM_LENGTH)
        i = min(_i, _j)
        j = max(_i, _j)
    elif i == 0 or j == 0:
        raise e

    tmp = Ecoli2.gene.chromosome[i:j]
    Ecoli2.gene.chromosome[i:j] = Ecoli1.gene.chromosome[i:j]
    Ecoli1.gene.chromosome[i:j] = tmp

    return Ecoli1, Ecoli2



def nextGeneration(pool):
    newPool = []
    while len(newPool) <= MAX_GENOM_LIST - 2:
        parent1 = random.choice(pool)
        parent2 = random.choice(pool)
        c1, c2 = crossOver(parent1, parent2)
        newPool.append(copy.deepcopy(c1))
        newPool.append(copy.deepcopy(c2))
    return newPool


def selectEcols(pool):
    pool = sorted(pool, key=lambda x: -x.evaluate())
    return pool[:SELECT_GENOM:]

pool = [Ecoli() for i in range(MAX_GENOM_LIST)]
best = pool[0]
highScore = 0


for epoch in range(MAX_ITER):
    print("epoch:{}".format(epoch))
    pool = selectEcols(pool)
    Max=pool[0].evaluate()
    print("Max:{}".format(Max))
    if pool[0].evaluate() > highScore:
        highScore = Max
        best = copy.deepcopy(pool[0])
    Min=pool[-1].evaluate()
    print("Min:{}".format(Min))
    if Max-Min<1e-10:
        for i in range(int(len(pool)*0.8)):
            pool[i].mutate(force=True)
    pool = nextGeneration(pool)
    for ecol in pool:
        ecol.mutate()

    if Max>10000:
        break

    print()

print(best.gene)
