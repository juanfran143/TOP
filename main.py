from classes import *
from solution import *
from sim import *
import numpy as np
from read_inputs import read

# Press the green button in the gutter to run the script.


def deterministic_approach(max_time):
    nodes = []

    nodes.append(node(0, 0, 1, 1))
    nodes.append(node(1, 1, 2, 2))
    nodes.append(node(2, 2, 1, -1))
    nodes.append(node(3, 3, 0, 0))
    nodes.append(node(4, 4, 3, 3))
    nodes.append(node(5, 0, 4, 4))

    solution2 = solution(nodes, 10)
    solution2.deterministic_multi_start(max_time)
    short_simulations = simheuristic(1000, 0.5)
    solution2.routes = [solution2.routes[0]]
    short_simulations.simulation(solution2)
    solution2.of = np.mean(solution2.routes[0].stochastic_of)
    print("Deterministic in stochastic enviroment: "+ str(solution2.of))

def simheuristic_approach(max_time):
    nodes = []

    nodes.append(node(0, 0, 1, 1))
    nodes.append(node(1, 1, 2, 2))
    nodes.append(node(2, 2, 1, -1))
    nodes.append(node(3, 3, 0, 0))
    nodes.append(node(4, 4, 3, 3))
    nodes.append(node(5, 0, 4, 4))

    solution1 = solution(nodes, 10)
    short_simulations = simheuristic(1000, 0.5)
    solution1.simheuristic_multi_start(max_time, short_simulations)

def Qsimheuristic_approach(max_time):
    nodes, capacity, vehicles = read()

    solution1 = solution(nodes, capacity, max_vehicles = vehicles)
    short_simulations = simheuristic(10, 0.2)
    #solution1.Qsimheuristic_multi_start(max_time, 20, short_simulations)
    solution1.Qsimheuristic_multi_start(600, 10, short_simulations)

if __name__ == '__main__':
    Qsimheuristic_approach(10)
    print()
    print()
    #simheuristic_approach(10)

    #deterministic_approach(10)