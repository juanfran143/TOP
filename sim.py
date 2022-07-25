from solution import *
import numpy as np
import multiprocessing.dummy as mp

class simheuristic:

    def __init__(self, simulations, var):
        self.simulations = simulations
        self.var = var

    def simulation(self, solution):

        fail = 0
        for route in solution.routes:
            for _ in range(self.simulations):
                first = True
                distance = 0
                for edge in route.edges:
                    distance += self.lognormal_simuation(edge.distance)
                    if distance > solution.max_dist:
                        if first:
                            first = False
                            fail += 1
                            route.stochastic_of.append(0)
                if first:
                    route.stochastic_of.append(solution.of)

            route.reliability = fail/self.simulations

        # route.reliability = fail/self.simulations

    def thread_function(self, route, solution, num_sim):
        fail = 0
        for _ in range(num_sim):
            first = True
            distance = 0
            for edge in route.edges:
                distance += self.lognormal_simuation(edge.distance)
                if distance > solution.max_dist:
                    if first:
                        first = False
                        fail += 1
                        route.stochastic_of.append(0)
            if first:
                route.stochastic_of.append(solution.of)

        return fail

    def parallel_simulation(self, solution):
        for route in solution.routes:
            with mp.Pool() as p:
                my_sums = p.starmap(self.thread_function, [(route, solution, 25), (route, solution, 25), (route, solution, 25), (route, solution, 25)])  # sums from 1 to 300 (including 300)
                print(my_sums)
                fail = sum(my_sums)
            route.reliability = fail / self.simulations

    def fast_simulation(self, route, max_dist, of):

        fail = 0
        for _ in range(self.simulations):
            first = True
            distance = 0
            for edge in route.edges:
                distance += self.lognormal_simuation(edge.distance)
                if distance > max_dist:
                    if first:
                        first = False
                        fail += 1
                        route.stochastic_of.append(0)
            if first:
                route.stochastic_of.append(of)

        route.reliability = fail/self.simulations


    def lognormal_simuation(self, mean):
        return np.random.lognormal(np.log(mean), self.var)

