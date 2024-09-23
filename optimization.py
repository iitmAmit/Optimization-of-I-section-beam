import numpy as np
from scipy.optimize import minimize

# Polynomial expressions (functions) as provided
def evaluate_polynomial(expression, variables):
    # Safely evaluate the polynomial expression
    return eval(expression, {"__builtins__": None}, dict(zip(["t1", "t2", "t3", "w1", "w2", "a"], variables)))

# Polynomial expressions
mass_expr = "37.00526 + 0.00000*1 + -0.00000*t2 + -0.00000*a + -0.00000*w2 + 0.00000*t3 + 0.00000*w1 + -0.00000*t1 + -0.00000*t2**2 + 0.00000*t2*a + -0.00000*t2*w2 + 0.00000*t2*t3 + 0.00000*t2*w1 + 0.00000*t2*t1 + -0.00000*a**2 + -0.00001*a*w2 + 0.00000*a*t3 + 0.00000*a*w1 + 0.00000*a*t1 + -0.00005*w2**2 + 0.01680*w2*t3 + -0.00000*w2*w1 + 0.00000*w2*t1 + -0.00000*t3**2 + -0.00000*t3*w1 + 0.00000*t3*t1 + 0.00000*w1**2 + 0.01680*w1*t1 + 0.00000*t1**2"
stress_expr = "43.16871 + 0.00000*1 + -0.00000*t2 + -0.00000*a + 0.00000*w2 + -0.00014*t3 + -0.00000*w1 + -0.00004*t1 + 0.00000*t2**2 + -0.00000*t2*a + 0.00011*t2*w2 + -0.00438*t2*t3 + -0.00008*t2*w1 + -0.00114*t2*t1 + -0.00000*a**2 + 0.00025*a*w2 + -0.00984*a*t3 + -0.00018*a*w1 + -0.00256*a*t1 + 0.00124*w2**2 + -0.00450*w2*t3 + -0.00062*w2*w1 + -0.00191*w2*t1 + 0.01087*t3**2 + -0.00008*t3*w1 + 0.00311*t3*t1 + 0.00036*w1**2 + 0.00014*w1*t1 + 0.00282*t1**2"
displacement_expr = "0.28877 + 0.00000*1 + -0.00000*t2 + -0.00000*a + -0.00000*w2 + -0.00000*t3 + -0.00000*w1 + -0.00000*t1 + 0.00000*t2**2 + -0.00000*t2*a + -0.00000*t2*w2 + -0.00001*t2*t3 + -0.00000*t2*w1 + -0.00002*t2*t1 + 0.00000*a**2 + -0.00000*a*w2 + -0.00003*a*t3 + -0.00001*a*w1 + -0.00004*a*t1 + -0.00000*w2**2 + 0.00000*w2*t3 + 0.00000*w2*w1 + 0.00000*w2*t1 + 0.00001*t3**2 + 0.00000*t3*w1 + 0.00001*t3*t1 + 0.00000*w1**2 + 0.00000*w1*t1 + 0.00001*t1**2"

# Constraints and bounds
def constraint_stress(variables):
    return 140 - evaluate_polynomial(stress_expr, variables)

def constraint_displacement(variables):
    return 1 - evaluate_polynomial(displacement_expr, variables)

# Define bounds for the design variables
bounds = [
    (40, 60),  # t1
    (32, 48),  # t2
    (48, 72),  # t3
    (120, 180),# w1
    (160, 240),# w2
    (71, 108)  # a
]

# Objective function to minimize (mass function)
def objective_function(variables):
    return evaluate_polynomial(mass_expr, variables)

# Initial guess (mid-point of bounds)
initial_guess = [
    (40 + 60) / 2,
    (32 + 48) / 2,
    (48 + 72) / 2,
    (120 + 180) / 2,
    (160 + 240) / 2,
    (71 + 108) / 2
]

# Constraints
constraints = [
    {'type': 'ineq', 'fun': constraint_stress},
    {'type': 'ineq', 'fun': constraint_displacement}
]

# Perform the optimization
result = minimize(objective_function, initial_guess, bounds=bounds, constraints=constraints, method='SLSQP')

# Print the results
if result.success:
    optimized_design = result.x
    optimized_mass = evaluate_polynomial(mass_expr, optimized_design)
    optimized_stress = evaluate_polynomial(stress_expr, optimized_design)
    optimized_displacement = evaluate_polynomial(displacement_expr, optimized_design)
    
    print("Optimization successful!")
    print(f"Optimized Design Variables: {optimized_design}")
    print(f"Minimized Mass: {optimized_mass}")
    print(f"Stress at Optimized Design: {optimized_stress}")
    print(f"Displacement at Optimized Design: {optimized_displacement}")
else:
    print("Optimization failed!")
    print(result.message)
