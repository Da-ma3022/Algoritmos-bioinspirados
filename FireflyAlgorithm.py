import random
import math

# ----------------------------------------
# OBJECTIVE FUNCTION
# ----------------------------------------
# Function to minimize:
# f(x) = x^2
# Best solution is x = 0
# ----------------------------------------

def objective_function(x):
    return x ** 2


# ----------------------------------------
# FIREFLY CLASS
# ----------------------------------------

class Firefly:

    def __init__(self, lower_bound, upper_bound):

        # Random initial position
        self.position = random.uniform(lower_bound, upper_bound)

        # Brightness based on solution quality
        self.brightness = 1 / (
            1 + objective_function(self.position)
        )


# ----------------------------------------
# PARAMETERS
# ----------------------------------------

NUM_FIREFLIES = 15
MAX_ITERATIONS = 50

ALPHA = 0.2
BETA_0 = 1.0
GAMMA = 1.0

LOWER_BOUND = -10
UPPER_BOUND = 10


# ----------------------------------------
# DISTANCE FUNCTION
# ----------------------------------------

def distance(f1, f2):
    return abs(f1.position - f2.position)


# ----------------------------------------
# MOVE FIREFLY FUNCTION
# ----------------------------------------

def move_firefly(firefly_i, firefly_j):

    # Distance between fireflies
    r = distance(firefly_i, firefly_j)

    # Attractiveness
    beta = BETA_0 * math.exp(-GAMMA * r ** 2)

    # Random movement
    random_step = ALPHA * (
        random.random() - 0.5
    )

    # Move toward brighter firefly
    firefly_i.position += (
        beta * (
            firefly_j.position
            - firefly_i.position
        )
        + random_step
    )

    # Keep inside boundaries
    firefly_i.position = max(
        LOWER_BOUND,
        min(UPPER_BOUND, firefly_i.position)
    )

    # Update brightness
    firefly_i.brightness = 1 / (
        1 + objective_function(
            firefly_i.position
        )
    )


# ----------------------------------------
# CREATE INITIAL POPULATION
# ----------------------------------------

fireflies = [
    Firefly(
        LOWER_BOUND,
        UPPER_BOUND
    )
    for _ in range(NUM_FIREFLIES)
]


# ----------------------------------------
# MAIN LOOP
# ----------------------------------------

for iteration in range(MAX_ITERATIONS):

    for i in range(NUM_FIREFLIES):

        for j in range(NUM_FIREFLIES):

            # Move weaker fireflies
            # toward brighter ones
            if (
                fireflies[j].brightness
                >
                fireflies[i].brightness
            ):

                move_firefly(
                    fireflies[i],
                    fireflies[j]
                )

    # Find best firefly
    best_firefly = min(
        fireflies,
        key=lambda f:
        objective_function(f.position)
    )

    # Print iteration results
    print(f"Iteration {iteration + 1}")

    print(
        f"Best Position: "
        f"{best_firefly.position:.6f}"
    )

    print(
        f"Function Value: "
        f"{objective_function(best_firefly.position):.6f}"
    )

    print("-" * 40)


# ----------------------------------------
# FINAL RESULT
# ----------------------------------------

best_firefly = min(
    fireflies,
    key=lambda f:
    objective_function(f.position)
)

print("\nFINAL RESULT")
print("=" * 40)

print(
    f"Optimal x found: "
    f"{best_firefly.position:.6f}"
)

print(
    f"Minimum function value: "
    f"{objective_function(best_firefly.position):.6f}"
)