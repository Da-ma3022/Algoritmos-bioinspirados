import random

# MATRIZ DE DISTANCIAS
# 5 nodos o ciudades
distancias = [
    [0, 2, 9, 10, 7],
    [2, 0, 6, 4, 3],
    [9, 6, 0, 8, 5],
    [10, 4, 8, 0, 6],
    [7, 3, 5, 6, 0]
]

num_nodos = len(distancias)
num_hormigas = 5
num_iteraciones = 20
alpha = 1       # importancia de la feromona
beta = 2        # importancia de la distancia
evaporacion = 0.5
Q = 100         # cantidad de feromona depositada

# Feromonas iniciales
feromonas = [[1.0 for _ in range(num_nodos)] for _ in range(num_nodos)]

mejor_ruta = None
mejor_distancia = float('inf')



# FUNCIONES

def calcular_distancia(ruta):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancias[ruta[i]][ruta[i + 1]]
    return total


def seleccionar_siguiente_nodo(actual, no_visitados):
    probabilidades = []
    suma = 0

    for nodo in no_visitados:
        tau = feromonas[actual][nodo] ** alpha
        eta = (1 / distancias[actual][nodo]) ** beta
        valor = tau * eta
        probabilidades.append((nodo, valor))
        suma += valor

    if suma == 0:
        return random.choice(list(no_visitados))

    r = random.uniform(0, suma)
    acumulado = 0

    for nodo, prob in probabilidades:
        acumulado += prob
        if acumulado >= r:
            return nodo

    return probabilidades[-1][0]


def construir_ruta():
    inicio = random.randint(0, num_nodos - 1)
    ruta = [inicio]
    no_visitados = set(range(num_nodos))
    no_visitados.remove(inicio)

    actual = inicio

    while no_visitados:
        siguiente = seleccionar_siguiente_nodo(actual, no_visitados)
        ruta.append(siguiente)
        no_visitados.remove(siguiente)
        actual = siguiente

    ruta.append(inicio)  # regresar al inicio
    return ruta
#for example, if the route is [0, 2, 3, 1, 4], it means the ant starts at node 0, then goes to node 2, then to node 3, then to node 1, and finally returns to node 0.

def actualizar_feromonas(todas_las_rutas):
    global feromonas

    # Evaporación
    for i in range(num_nodos):
        for j in range(num_nodos):
            feromonas[i][j] *= (1 - evaporacion)

    # Depósito de feromonas
    for ruta, distancia in todas_las_rutas:
        deposito = Q / distancia
        for i in range(len(ruta) - 1):
            a = ruta[i]
            b = ruta[i + 1]
            feromonas[a][b] += deposito
            feromonas[b][a] += deposito  # porque es bidireccional



# ALGORITMO PRINCIPAL

for iteracion in range(num_iteraciones):
    todas_las_rutas = []

    for _ in range(num_hormigas):
        ruta = construir_ruta()
        distancia_total = calcular_distancia(ruta)
        todas_las_rutas.append((ruta, distancia_total))

        if distancia_total < mejor_distancia:
            mejor_distancia = distancia_total
            mejor_ruta = ruta

    actualizar_feromonas(todas_las_rutas)

    print(f"Iteración {iteracion + 1}: Mejor distancia hasta ahora = {mejor_distancia}")

print("\n=== RESULTADO FINAL ===")
print("Mejor ruta encontrada:", mejor_ruta)
print("Distancia total:", mejor_distancia)