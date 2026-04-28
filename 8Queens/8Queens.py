import random

def fitness(chessboard):
    non_attacking_pairs = 28
    for i in range(len(chessboard)):
        for j in range(i + 1, len(chessboard)):
            if abs(chessboard[i] - chessboard[j]) == abs(i - j):
                non_attacking_pairs -= 1
    return non_attacking_pairs

def create_population(size, n):
    return [random.sample(range(n), n) for _ in range(size)]

def sorted_fitness(i):
    return i[0]

def select_parents(population, fitnesses, tournament_size=3):
    combined = []
    for i in range(len(population)):
        combined.append((population[i], fitnesses[i]))

    tournament = random.sample(combined, tournament_size)
    tournament.sort(key=sorted_fitness, reverse=True)
    return tournament[0][0], tournament[1][0]

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

def mutate(board, mutation_rate=0.2):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(board)), 2)
        board[i], board[j] = board[j], board[i]

def GA(n=8, population_size=100, generations=3000, mutation_rate=0.2):
    population = create_population(population_size, n)
    solutions = []

    for generation in range(generations):
        fitnesses = []
        for i in population:
            fitnesses.append(fitness(i))

        if max(fitnesses) == 28:
            solutions.append(population[fitnesses.index(28)])

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitnesses)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population

        best_fitness = max(fitnesses)
        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

    return solutions

def rotate(solution):
    n = len(solution)
    rotated = [0] * n
    for row in range(n):
        rotated[solution[row]] = n - 1 - row
    return rotated

def reflect(solution):
    n = len(solution)
    reflected = [0] * n
    for i in range(n):
        reflected[i] = n - 1 - solution[i]
    return reflected

def get_all_transformations(solution):
    transformations = []
    current = solution
    for _ in range(4):
        transformations.append(current)
        transformations.append(reflect(current))
        current = rotate(current)
    return transformations

def get_canonical_solution(solution):
    transformations = get_all_transformations(solution)
    return min(transformations)

def generate_unique_solutions(all_solutions):
    unique_solutions = set()
    for solution in all_solutions:
        canonical = tuple(get_canonical_solution(solution))
        unique_solutions.add(canonical)
    return list(unique_solutions)

all_solutions = GA()
unique_solutions = generate_unique_solutions(all_solutions)
print(f"Number of unique solutions: {len(unique_solutions)}")
for i in unique_solutions:
    print(i)