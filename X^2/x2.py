import random

Population = 30
Generations = 100
Mutation_rate = 0.1

def fitness(x):
    return x ** 2

def initial_population(size):
    population = []
    for i in range(size):
        population.append(random.randint(0, 255))
    return population

def parent_selection(population, fitness_values):
    probability = []
    fitness_total = sum(fitness_values)
    for i in range(len(fitness_values)):
        probability.append(fitness_values[i] / fitness_total)
    selected_parents = random.choices(population, weights=probability, k=2)
    return selected_parents

def dec_to_bin(num):
    i = 7
    String = ""
    while i > -1:
        if num >= 2 ** i:
            String += "1"
            num -= 2 ** i
        else:
            String += "0"
        i -= 1
    return String

def bin_to_dec(String):
    num = 0
    for i in range(len(str(String)) - 1, -1, -1):
        if int(str(String)[7 - i]) == 1:
            num += 2 ** i
    return num

def crossover(p1, p2):
    crossover_point = random.randint(0, 7)
    child1 = dec_to_bin(p1)[0:crossover_point] + dec_to_bin(p2)[crossover_point:len(dec_to_bin(p2))]
    child2 = dec_to_bin(p2)[0:crossover_point] + dec_to_bin(p1)[crossover_point:len(dec_to_bin(p1))]
    return child1, child2

def mutation(chromosome):
    ls = list(chromosome)
    if random.random() > Mutation_rate:
        mutation_point = random.randint(0, 7)
        if ls[mutation_point] == "1":
            ls[mutation_point] = "0"
        else:
            ls[mutation_point] = "1"
    temp = ""
    for i in ls:
        temp += i
    #returns binary
    return temp

def GA():
    population = initial_population(Population)
    for i in range(Generations):
        fitness_values = []
        new_population = []
        for j in population:
            fitness_values.append(fitness(j))
        while len(new_population) < Population:
            p1, p2 = parent_selection(population, fitness_values)
            child1, child2 = crossover(p1, p2)
            new_population.append(bin_to_dec(mutation(child1)))
            new_population.append(bin_to_dec(mutation(child2)))
        
        population = new_population[:Population]
    
    Answer = max(population, key=fitness)
    return Answer, fitness(Answer)

solution, fit = GA()
print("Best Solution: " + str(solution))
print("Best fitness " + str(fit))