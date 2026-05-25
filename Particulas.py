import random

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
# PARTICLE CLASS
# ----------------------------------------

class Particle:

    def __init__(self):

        # Random initial position
        self.position = random.uniform(-10, 10)

        # Random initial velocity
        self.velocity = random.uniform(-1, 1)

        # Personal best position
        self.best_position = self.position

        # Personal best value
        self.best_value = objective_function(self.position)


# ----------------------------------------
# PARAMETERS
# ----------------------------------------

NUM_PARTICLES = 20
MAX_ITERATIONS = 50

W = 0.5      # inertia
C1 = 1.5     # cognitive coefficient
C2 = 1.5     # social coefficient


# ----------------------------------------
# CREATE PARTICLES
# ----------------------------------------

particles = [Particle() for _ in range(NUM_PARTICLES)]


# ----------------------------------------
# GLOBAL BEST
# ----------------------------------------

global_best_position = particles[0].position
global_best_value = objective_function(global_best_position)


# ----------------------------------------
# MAIN LOOP
# ----------------------------------------

for iteration in range(MAX_ITERATIONS):

    for particle in particles:

        # Evaluate current position
        current_value = objective_function(particle.position)

        # Update personal best
        if current_value < particle.best_value:
            particle.best_value = current_value
            particle.best_position = particle.position

        # Update global best
        if current_value < global_best_value:
            global_best_value = current_value
            global_best_position = particle.position

    # Update velocity and position
    for particle in particles:

        r1 = random.random()
        r2 = random.random()

        cognitive = C1 * r1 * (
            particle.best_position - particle.position
        )

        social = C2 * r2 * (
            global_best_position - particle.position
        )

        particle.velocity = (
            W * particle.velocity
            + cognitive
            + social
        )

        particle.position += particle.velocity

    # Print iteration results
    print(f"Iteration {iteration + 1}")
    print(f"Best Position: {global_best_position:.6f}")
    print(f"Best Value: {global_best_value:.6f}")
    print("-" * 40)


# ----------------------------------------
# FINAL RESULT
# ----------------------------------------

print("\nFINAL RESULT")
print("=" * 40)
print(f"Optimal x found: {global_best_position:.6f}")
print(f"Minimum function value: {global_best_value:.6f}")