import random

def generate_chromosome():
    return [random.randint(0, 7) for _ in range(8)]

def calculate_fitness(chromosome):
    fitness = 0
    for i in range(8):
        safe = True
        for j in range(8):
            if i == j:
                continue
            if chromosome[i] == chromosome[j] or abs(i - j) == abs(chromosome[i] - chromosome[j]):
                safe = False
                break
        if safe:
            fitness += 1
    return fitness

def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population), random.choice(population)
    parents = random.choices(population, weights=fitnesses, k=2)
    return parents[0], parents[1]

def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(1, 6)
        child = parent1[:crossover_point] + parent2[crossover_point:]
    else:
        child = parent1 if random.random() < 0.5 else parent2
    return child

def mutate(child, mutation_rate):
    for i in range(8):
        if random.random() < mutation_rate:
            child[i] = random.randint(0, 7)
    return child

def genetic_algorithm():
    population_size = 100
    mutation_rate = 0.1
    crossover_rate = 0.7
    max_generations = 1000

    population = [generate_chromosome() for _ in range(population_size)]
    
    for generation in range(max_generations):
        fitnesses = [calculate_fitness(chrom) for chrom in population]
        max_fit = max(fitnesses)
        
        if max_fit == 8:
            best_chrom = population[fitnesses.index(max_fit)]
            print(f"Solution found in generation {generation}: {best_chrom}")
            return best_chrom, generation
        
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = select_parents(population, fitnesses)
            child = crossover(parent1, parent2, crossover_rate)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    print("No solution found within the maximum generations.")
    return None, max_generations

solution, generations = genetic_algorithm()
print(f"Best Solution: {solution}")
print(f"Generations taken: {generations}")


def print_board(solution):
    board = [['.' for _ in range(8)] for _ in range(8)]
    for col in range(8):
        row = solution[col]
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))

if solution:
    print("Chessboard Layout:")
    print_board(solution)