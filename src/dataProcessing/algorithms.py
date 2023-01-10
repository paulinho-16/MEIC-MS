import heapq
import random as r
from ..sumo.gen_routes import gen_routes
from ..sumo.gen_od  import generate_od2
import random 

def hill_climbing(routes, od_values: dict, evaluate_function):
    curr_error = float('inf')   # The current error value
    gravar = 0

    # TODO: mudar forma de alterar o vetor

    for dest_origin in od_values.keys():
        # Test different values for the od_values
        for num_cars in range(5, 15, 5):
            prev_od_value = od_values[dest_origin]      # Save the previous value
            od_values[dest_origin] = num_cars           # Update the current one
            # Update the routes 
            gen_routes(od_values, routes)
            
            new_error = evaluate_function()
            # The current state is better than the previous, one. Update the curr_error. 
            if new_error < curr_error: 
                print(f'New best error: {new_error} ; Previous error: {curr_error}')
                curr_error = new_error
            else:
                # Recover the previous od.
                od_values[dest_origin] = prev_od_value
                print(f'Worse value: {new_error} ; Best error: {curr_error}')

        gravar = (gravar + 1)%6
        if gravar == 5:
            generate_od2(od_values)

        return od_values, curr_error

def mutation(individual):
    num_mutated_keys = len(individual.keys()) // 10 # TODO: change value according to the size of keys
    mutated_keys = r.sample(individual.keys(), num_mutated_keys)
    for key in mutated_keys:
        individual[key] = individual[key] + 20 if r.uniform(0, 1.0) > 0.5 else individual[key] - 20
    
    return individual

def crossover(parent1: dict, parent2: dict):
    if len(parent1.keys()) != len(parent2.keys()):
        print(f'LENS DIFERENTES: {len(parent1.keys())}, {len(parent2.keys())}')
    
    separator = len(parent1.keys()) // 2
    first_half = parent1[:separator]
    second_half = parent2[separator:]
    child = first_half + second_half

    if (separator != len(child)):
        print(f'LENS DIFERENTES: {separator} e {len(child)}')

    return child


def gen_random_sample(initial_ods: dict) -> dict:
    """
    Create a new random sample of ods. 

    Parameters 
    ----------
    initial_ods: dict -> the key is the "origin_destination_timestamp" of the od and the value is the number of cars 

    Return
    ------
    Random position of the initial_ods summed by a random number between [1, numcars//2]
    """
    sample_size = random.randint(1, len(initial_ods.keys()))
    sample = random.sample(initial_ods.keys(), sample_size)
    for od, num_cars in sample: 
        to_add = random.randint(1, num_cars//2) # The nubmer of cars to be added. 
        initial_ods[od] += to_add

    return initial_ods 
    
def gen_initial_population(population_size: int, initial_ods: dict) -> list:
    """
    Generates a new random population of ods. 

    Parameters
    ----------
    population_size: int -> the size of the population 
    initial_ods: dict -> the key is the "origin_destination_timestamp" of the od and the value is the number of cars. This is the initial sample. 

    Return
    ------
    A list of dictionaries like initial_ods representing the population. 
    """
    population = []
    for _ in range(population_size):
        population.append(gen_random_sample(initial_ods))
    return population 

def genetic_algorithm(routes, initial_ods: dict, evaluate_function, num_iterations):
    population = gen_initial_population(10, initial_ods)

    heapq.heapify(population)
    length = len(population)

    for index in range(num_iterations):
        parent1 = heapq.nlargest(1, population)[0]  # best values
        parent2 = heapq.nsmallest(length - 1, population)[r.randint(0, length - 2)]  # random values
        child = crossover(parent1, parent2)

        if r.uniform(0, 1.0) > 0.80:  # mutation with a chance of 20%
            print(f'Before mutation: {child}')
            child = mutation(child)
            print(f'After mutation: {child}')
            print('-------------------')

        heapq.heapreplace(population, child)  # remove the worst values and add the new child

    final_layout = heapq.nlargest(1, population)[0]  # best values

    print(f'FINAL_SCORE {str(final_layout.get_score())}')
    print(f'PRODUCTS OUT: {len(final_layout.products_out)}')

    return final_layout