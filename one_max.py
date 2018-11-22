import random
import copy
import numpy as np

GENOM_LENGTH = 100
MAX_GENOM_LIST = 1000
SELECT_GENOM = 200
INDIVIDUAL_MUTATION = 0.1  # 個体に突然変異が起きる確率を表す
GENOM_MUTATION = 0.1  # 突然変異が起きた個体について、各々の遺伝子が変異する確率を表す
MAX_ITER = 50
ATGC = [0, 1, 2, 3]


class Gene:
    def __init__(self):
        self.chromosome = [random.choice(ATGC) for i in range(GENOM_LENGTH)]

    def __repr__(self):
        return "<<{}>>".format(",".join([str(i) for i in self.chromosome]))


class Ecoli:
    def __init__(self):
        self.gene = Gene()

    def evaluate(self):
        chromosome_np = np.asarray(self.gene.chromosome)
        return 1 / (np.sum((chromosome_np - 1)**2)+1e-5)#すべてが1であるほどよい

    def mutate(self, force=False):
        if force or random.random() < INDIVIDUAL_MUTATION:
            length = len(self.gene.chromosome)
            for i in range(length):
                if random.random() < GENOM_MUTATION:
                    self.gene.chromosome[i] = random.choice(ATGC)
            return True
        else:
            return False


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


pool = [Ecoli() for i in range(MAX_GENOM_LIST)]
best = pool[0]
highScore = 0


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


for epoch in range(MAX_ITER):
    print("epoch:{}".format(epoch))
    pool = selectEcols(pool)

    print("Max:{}".format(pool[0].evaluate()))
    if pool[0].evaluate() > highScore:
        highScore = pool[0].evaluate()
        best = copy.deepcopy(pool[0])
    print("Min:{}".format(pool[-1].evaluate()))
    pool = nextGeneration(pool)
    for ecol in pool:
        ecol.mutate()

    print()

print(best.gene)
