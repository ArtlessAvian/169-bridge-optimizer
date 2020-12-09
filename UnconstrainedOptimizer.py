import math
from Bridge import Bridge
from Problem import Problem

class ConjugateGradientDescent:
    def __init__(self, grad_func, vec):
        self.gradient = grad_func(vec)
        self.direction = NormalizeVector(self.gradient)

    def step(self, func, grad_func, vec):
        newGradient = grad_func(vec)
        beta = max(0, DotProduct(newGradient, SubtractVectors(newGradient, self.gradient)) / DotProduct(self.gradient, self.gradient))
        
        newDirection = [-newGradient[i] + beta * self.direction[i] for i in range(len(self.direction))]
        newVec = line_search(func, grad_func, vec, newDirection)

        self.gradient = newGradient
        self.direction = newDirection
        return newVec

def calculate_gradient(vec, func, small_step = 1e-8):
    gradient = []
    old = func(vec)
    for i in range(len(vec)):
        vec[i] += small_step
        new = func(vec)
        vec[i] -= small_step * 2
        old = func(vec)
        vec[i] += small_step
        
        partial = (new - old) / small_step / 2
        gradient.append(partial)    
    return gradient

def line_search(func, grad_func, vec, direction):
    objective = lambda a : func([vec[i] + a * direction[i] for i in range(len(vec))])
    a, b = bracket_minimum(objective)
    alpha = golden_section_search(objective, a, b)
    return [vec[i] + alpha * direction[i] for i in range(len(vec))]
    # really garbage line search
    # tendency to explode for large gradients
    # return [vec[i] + direction[i] / 150 for i in range(len(vec))]

def bracket_minimum(func, x = 0, s = 1e-2, k = 2.0):
    a, ya = x, func(x)
    b, yb = a + s, func(a + s)
    if yb > ya:
        a, b = b, a
        ya, yb = yb, ya
        s = -s
    while True: 
        c, yc = b + s, func(b + s)
        if yc > yb:
            return (a, c) if a < c else (c, a)
        a, ya, b, yb = b, yb, c, yc
        s *= k

def golden_section_search(func, a, b, n = 5000):
    golden = (1 + 5 ** 0.5) / 2
    phi = golden - 1
    d = phi * b + (1 - phi) * a
    yd = func(d)
    for i in range(n):
        c = phi * a + (1 - phi) * b
        yc = func(c)
        if yc < yd:
            b, d, yd = d, c, yc
        else:
            a, b = b, c
    return c
    




# Generic Vector Operations
def VectorMagnitude(vec1):
    magnitude = 0
    for i in range(len(vec1)):
        magnitude += vec1[i] * vec1[i]
    return math.sqrt(magnitude)

def NormalizeVector(vec1):
    magnitude = VectorMagnitude(vec1)
    for i in range(len(vec1)):
        vec1[i] /= magnitude * -1
    return vec1

def SubtractVectors(vec1, vec2):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] - vec2[i])
    return result

def AddVectors(vec1, vec2):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] + vec2[i])
    return result

def DotProduct(vec1, vec2):
    #assume vec1 and vec2 have equal lengths
    dot = 0
    for i in range(len(vec1)):
        dot += vec1[i] * vec2[i]
    return dot

if __name__ == "__main__":
    print("### EASY TESTS ###")

    easy_function = lambda vec : vec[0] ** 2 + vec[1] ** 2 + vec[0] * vec[1]
    easy_gradient = lambda vec : [2 * vec[0] + vec[1], 2 * vec[1] + vec[0]]
    print("Expecting 27 and [9, 9]")
    print(easy_function([3, 3]))
    print(easy_gradient([3, 3]))

    print()
    print("Should return about (0.5, 0.5)")
    print(line_search(easy_function, easy_gradient, [-20, 21], [1, -1]))

    print()
    print("Should optimize to (0, 0)")
    small_test = ConjugateGradientDescent(easy_gradient, [-20, 21])
    point = [-20, 21]
    for i in range(5):
        print(point)
        point = small_test.step(easy_function, easy_gradient, point)

    print(point)

    print()
    print("### ACTUAL USAGE ###")

    # the actual problem
    bridge = Bridge()
    bridge.randomize()

    vec = bridge.to_vector()
    problem = Problem(bridge)

    print("Original Objective Function")
    print(bridge.objective_function())

    # example usage of optimizer
    the_function = problem.objective_function
    the_gradient = lambda veccc : calculate_gradient(veccc, problem.objective_function)

    optimizer = ConjugateGradientDescent(the_gradient, vec)
    for i in range(10):
        vec = optimizer.step(the_function, the_gradient, vec)
    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())