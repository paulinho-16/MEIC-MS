from ..sumo.gen_routes import gen_routes
from ..sumo.gen_od  import generate_od2

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

        gravar = (gravar + 1)%6
        if gravar == 5:
            generate_od2(od_values)

    return od_values, curr_error