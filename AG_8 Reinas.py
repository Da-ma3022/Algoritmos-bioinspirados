import random

N = 8                 # Número de reinas (8 reinas)
POP_SIZE = 10       # Tamaño de la población (cuántas soluciones por generación)
GENERATIONS = 200    # Máximo de generaciones
MUT_RATE = 0.2    # Probabilidad de mutación (15%)
TOURNAMENT_K = 8    # Tamaño del torneo para selección
ELITISM = True       # Guardar siempre la mejor solucion  de la generaciones 
# Para crear un individuo
def create_individual(n=N):
    """
    Crea una solución aleatoria como permutación de 1..n
    Ej: [4,2,7,3,6,8,5,1]
    """
    ind = list(range(1, n + 1))
    random.shuffle(ind)
    return ind


# FITNESS: medie qué tan buena es la solución
def conflicts(ind):
    """
    Cuenta cuántos conflictos diagonales hay.
    Como es permutación, NO hay conflictos por filas/columnas,
    solo revisamos diagonales.
    """
    c = 0
    # Comparar cada par de columnas i < j
    for i in range(N):
        for j in range(i + 1, N):
            # Si están en la misma diagonal:
            if abs(ind[i] - ind[j]) == abs(i - j):
                c += 1
    return c


def fitness(ind):
    """
    Hay 28 pares posibles (8C2). Fitness máximo = 28 (cero conflictos).
    """
    max_pairs = (N * (N - 1)) // 2  # 8*7/2 = 28
    return max_pairs - conflicts(ind)


def tournament_selection(population):
    """
    Elige k individuos al azar y regresa el mejor (mayor fitness).
    """
    contestants = random.sample(population, TOURNAMENT_K)
    return max(contestants, key=fitness)



def order_crossover(parent1, parent2):
    """
    OX:
    - Copia un segmento de parent1
    - Rellena con el orden de parent2 sin repetir
    """
    size = len(parent1)
    child = [None] * size

    # Elege dos puntos de corte
    a, b = sorted(random.sample(range(size), 2))

    # Copiamos el segmento del parent1
    child[a:b+1] = parent1[a:b+1]

    # Rellena con genes de parent2 que no estén ya en el hijo
    p2_genes = [g for g in parent2 if g not in child]

    # Llena espacios None de izquierda a derecha
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_genes[idx]
            idx += 1

    return child

def mutate(ind):
    """
    Intercambia dos posiciones al azar (mutación simple y efectiva).
    """
    i, j = random.sample(range(N), 2)
    ind[i], ind[j] = ind[j], ind[i]
    return ind


def print_board(solution):
    """
    Imprime el tablero en consola con Q donde hay reinas.
    solution[col] = fila (1..8)
    """
    board = [["." for _ in range(N)] for _ in range(N)]
    for col in range(N):
        row = solution[col] - 1
        board[row][col] = "Q"
    for row in board:
        print(" ".join(row))



def genetic_algorithm():
    # Crear población inicial
    population = [create_individual() for _ in range(POP_SIZE)]

    best = max(population, key=fitness)

    for gen in range(1, GENERATIONS + 1):
        # Encontrar el mejor de la generación
        current_best = max(population, key=fitness)

        # Guardar si mejoró
        if fitness(current_best) > fitness(best):
            best = current_best

        # Si ya es solución perfecta, terminamos
        if fitness(best) == (N * (N - 1)) // 2:
            print(f"Solución perfecta encontrada en generación {gen}")
            return best

        # Crear nueva población
        new_population = []

        # Elitismo: guardar el mejor
        if ELITISM:
            new_population.append(best[:])  # copia del mejor

        # Llenar el resto de la población con hijos
        while len(new_population) < POP_SIZE:
            # Seleccionar padres
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            # Cruzar
            child = order_crossover(p1, p2)

            # Mutar con cierta probabilidad
            if random.random() < MUT_RATE:
                child = mutate(child)

            new_population.append(child)

        population = new_population

        # Mostrar progreso cada cierto número de generaciones
        if gen % 50 == 0:
            print(f"Gen {gen} | Mejor fitness: {fitness(best)} | Conflictos: {conflicts(best)}")

    print("No se encontró solución perfecta, pero aquí va la mejor encontrada:")
    return best


if __name__ == "__main__":
    sol = genetic_algorithm()
    print("\nMejor solución:", sol)
    print("Fitness:", fitness(sol), "| Conflictos:", conflicts(sol))
    print("\nTablero:")
    print_board(sol)