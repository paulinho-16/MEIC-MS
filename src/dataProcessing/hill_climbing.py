import time
import random
import warnings
import numpy as np

from ..sumo.gen_routes import gen_routes
from ..sumo.gen_od  import generate_od2
from ..sumo.utils import read_od_dict

from docplex.mp.model import Model
import scipy.optimize as optimize

def random_search(routes, od_values: dict, evaluate_function):
    curr_od_values = od_values.copy()
    curr_error = float('inf')   # The current error value
    gravar = 0

    for i in range(100):
        print('Iteration: ', i)
        cars = [0 for _ in range(len(od_values))]
        total_cars = 18500
        while total_cars > 0:
            cars[random.randint(0, len(od_values)-1)] += 1
            total_cars -= 1

        od_values.update(zip(od_values.keys(), cars))

        # Update the routes
        gen_routes(od_values, routes)

        new_error = evaluate_function()

        # The current state is better than the previous one: Update curr_error
        if new_error < curr_error:
            print(f'New best error: {new_error} ; Previous error: {curr_error}')
            curr_od_values = od_values.copy()
            curr_error = new_error
        else:
            print(f'Worse value: {new_error} ; Best error: {curr_error}')

        gravar = (gravar + 1) % 6
        if gravar == 5:
            generate_od2(od_values)

    return curr_od_values, curr_error

def hill_climbing(routes, od_values: dict, evaluate_function):
    curr_error = float('inf')   # The current error value
    gravar = 0
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

        gravar = (gravar + 1) % 6
        if gravar == 5:
            generate_od2(od_values)

    return od_values, curr_error

class TookTooLong(Warning):
    pass

class MinimizeStopper(object):
    def __init__(self, max_sec=60):
        self.max_sec = max_sec
        self.start = time.time()
    def __call__(self, xk=None):
        elapsed = time.time() - self.start
        if elapsed > self.max_sec:
            warnings.warn("Terminating optimization: time limit reached",
                          TookTooLong)
        else:
            # you might want to report other stuff here
            print("Elapsed: %.3f sec" % elapsed)

def optimize_search(routes, evaluate_function):
    initial_values = read_od_dict('./data/best_solution.od')
    ods, initial_guess = zip(*initial_values.items())
    initial_guess = list(map(int, initial_guess))

    result = optimize.minimize(evaluate_function, initial_guess, args=(ods, routes), callback=MinimizeStopper(1E-3))

    if result.success:
        print('AQUIIIII')
        fitted_params = result.x
        print(fitted_params)

        with open('./data/solution.txt', 'w+') as sol_file:
            for i, od in enumerate(ods):
                sol_file.write(f"{od} {fitted_params[i]}\n")
    else:
        raise ValueError(result.message)

    return None, None

# TODO: unused
def algorithm(routes, od_values: dict, evaluate_function):
    m = Model(name='OD Trips')

    ods, num_cars = zip(*od_values.items())
    num_cars = list(map(int, num_cars))

    cars = m.integer_var_list(len(num_cars), name='cars')

    # Constraints
    min_vehicles_constraint = m.add_constraint(sum(cars) >= 450)
    max_vehicles_constraint = m.add_constraint(sum(cars) <= 970)

    # convert method to a linear expression
    kpi = m.add_kpi(evaluate_function(ods, cars, routes), "Total cars")

    m.minimize(kpi)

    sol = m.solve()
    sol.display()

    with open("./data/solution.txt", 'w') as sol_file:
        for i, od in enumerate(ods):
            sol_file.write(f"{od} {cars[i].solution_value}\n")

# TODO: unused
def algorithm2(routes, od_values: dict, evaluate_function):
    # define range for input
    cars_min, cars_max = 0, 10
    # define the bounds on the search
    bounds = [[cars_min, cars_max] for i in range(len(od_values))]
    # perform the simulated annealing search
    ods, cars = zip(*od_values.items())
    cars = list(map(int, cars))
    result = dual_annealing(evaluate_function(ods, cars, routes), bounds)
    # summarize the result
    print('Status : %s' % result['message'])
    print('Total Evaluations: %d' % result['nfev'])
    # evaluate solution
    solution = result['cars']
    evaluation = evaluate_function(ods, solution, routes)
    print('Solution: f(%s) = %.5f' % (solution, evaluation))
