import random
import math

def fitness(city1, city2):
    return math.sqrt(((city1[0] - city2[0]) ** 2) + ((city1[1] - city2[1]) ** 2))

def cities():
    cities = []
    with open("D:\\AI\\Assignments\\TSP51\\TSP51.txt", "r") as file:
        while file.readline():
            line = file.readlines()
        for i in range(len(line)):
            j = line[i].split()
            cities.append((int(j[1]), int(j[2])))
    return cities

def total_distance(path, cities):
    distance = 0
    for i in range(len(path)):
        city1 = cities[path[i]]
        city2 = cities[path[(i + 1) % len(path)]]
        distance += fitness(city1, city2)
    return distance

def create_population(cities, population_size):
    population = []
    for _ in range(population_size):
        path = list(range(len(cities)))
        random.shuffle(path)
        population.append(path)
    return population

def parent_selection(population, cities, tournament_size=10):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda p: total_distance(p, cities))
    return tournament[0], tournament[1]

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    i = end
    for j in parent2:
        if j not in child:
            child[i % size] = j
            i += 1
    return child

def mutation(path, mutation_rate=0.05):
    x = random.randint(0, len(path) - 1)
    if random.random() < mutation_rate:
        i = random.randint(0, len(path) - 1)
        path[x], path[i] = path[i], path[x]

def GA(cities, population_size=50, generations=3000, mutation_rate=0.05):
    population = create_population(cities, population_size)
    best_distance = float('inf')
    best_path = None

    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = parent_selection(population, cities)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutation(child1, mutation_rate)
            mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = sorted(new_population, key=lambda p: total_distance(p, cities))
        best_in_gen = population[0]
        best_in_gen_distance = total_distance(best_in_gen, cities)

        if best_in_gen_distance < best_distance:
            best_distance = best_in_gen_distance
            best_path = best_in_gen

        print(f"Generation {generation + 1}: Best Distance = {best_distance:.2f}")

    return best_path, best_distance

cities = cities()
best_path, best_distance = GA(cities, population_size=50, generations=3000, mutation_rate=0.05)
print(f"\nBest Distance: {best_distance:.2f}")
print(f"Best Path: {best_path}")