import copy

from classes import *
import random as rnd
from sim import simheuristic
import numpy as np
import time
import sys
import pandas as pd
class solution:

    def __init__(self, nodes, max_dist, max_vehicles = 1,alpha = 0.7):
        self.routes = []
        self.of = 0
        #self.stochastic_of = []
        #self.reliability = 0
        self.nodes = nodes
        self.savings = []
        self.alpha = alpha
        self.max_dist = max_dist
        self.max_vehicles = max_vehicles

    def reset(self):
        self.routes = []
        self.stochastic_of = []
        self.savings = []

    def dummy_solution(self):
        for i in range(len(self.nodes)-2):
            edges = [edge(self.nodes[0], self.nodes[i+1]), edge(self.nodes[i+1], self.nodes[-1])]
            self.routes.append(route(i, edges, sum([i.distance for i in edges])))
            self.routes[i].reward = self.nodes[i+1].reward
            self.nodes[i+1].route = self.routes[i]

    def create_saving_list(self):
        for i in range(len(self.nodes)-2):
            for j in range(len(self.nodes)-2):
                if i == j:
                    continue
                edge_a_b = edge(self.nodes[i+1], self.nodes[j+1])
                edge_a_end = edge(self.nodes[i + 1], self.nodes[-1])
                edge_depot_b = edge(self.nodes[0], self.nodes[j + 1])
                self.savings.append(saving(self.nodes[j + 1],
                                           self.nodes[i + 1],
                                           self.alpha * (edge_a_end.distance + edge_depot_b.distance - edge_a_b.distance) + (1 - self.alpha) * (self.nodes[i+1].reward + self.nodes[j+1].reward),
                                           edge_a_b.distance))

        self.savings.sort(key = lambda x: x.distance)

    def select_saving(self, random = 2):
        return self.savings.pop(rnd.randint(0, min([random, len(self.savings)-1])))

    def merge_routes(self, saving):
        route_a = saving.start.route
        route_b = saving.end.route
        distance = route_a.distance + route_b.distance + saving.a_to_b - route_a.edges[-1].distance - route_b.edges[0].distance
        if route_a.id != route_b.id and route_a.edges[0].end.id == saving.start.id and route_b.edges[0].end.id == saving.end.id and distance <= self.max_dist:

            route_a.edges.pop()
            route_a.edges = route_a.edges + [edge(saving.start, saving.end)] + route_b.edges[1:]
            route_a.distance = distance
            route_a.reward += route_b.reward
            for i in route_b.edges[:-1]:
                i.end.route = route_a

            self.routes.pop(self.routes.index(route_b))

    def local_search_same_route(self):
        """
        En el determinista no tiene sentido, pero en el simheurístico sí.
        :return:
        """
        for route in self.routes:
            for edge in route:
                pass

    def determinstic_algorithm(self):
        self.dummy_solution()
        self.create_saving_list()
        while len(self.savings) != 0:
            self.merge_routes(self.select_saving())

        self.routes.sort(key=lambda x: x.reward, reverse=True)
        self.of = sum([self.routes[i].reward for i in range(self.max_vehicles)])

        #print(self.of)
        #for i in self.routes:
        #    print(i.__str__())

        return self.routes, self.of


    def simheuristic_algorithm(self, simheuristico: simheuristic):
        self.dummy_solution()
        self.create_saving_list()
        while len(self.savings) != 0:
            self.merge_routes(self.select_saving())

        self.routes.sort(key=lambda x: x.reward, reverse=True)
        self.of = sum([self.routes[i].reward for i in range(self.max_vehicles)])

        simheuristico.simulation(self)
        self.routes.sort(key=lambda x: np.mean(x.stochastic_of), reverse=True)
        self.of = sum([np.mean(self.routes[i].stochastic_of) for i in range(self.max_vehicles)])

        #print(self.of)
        #for i in self.routes:
        #    print(i.__str__())

        return self.routes, self.of



    def deterministic_multi_start(self, max_time):
        start = time.time()
        best_route, best_of = self.determinstic_algorithm()
        while time.time()-start <= max_time:
            self.reset()
            new_route, new_sol = self.determinstic_algorithm()
            if best_of < new_sol:
                best_of = new_sol
                best_route = copy.deepcopy(new_route)

        self.routes = best_route
        print(best_of)
        for i in self.routes:
            print(i.__str__())

    def simheuristic_multi_start(self, max_time, simheuristic: simheuristic):
        start = time.time()
        best_route, best_of = self.simheuristic_algorithm(simheuristic)
        while time.time()-start <= max_time:
            self.reset()
            new_route, new_sol = self.simheuristic_algorithm(simheuristic)
            if best_of < new_sol:
                best_of = new_sol
                best_route = new_route.copy()

        self.routes = best_route

        print(best_of)
        for i in best_route:
            text = str(i.edges[0].start) + "-"
            for j in i.edges[:-1]:
                text += str(j.end) + "-"
            text += str(i.edges[-1].end)
        print(text)




    def Qmerge_routes(self, saving, route_b):
        route_a = saving.start.route
        #route_b = saving.end.route
        distance = route_a.distance + route_b.distance + saving.a_to_b - route_a.edges[-1].distance - route_b.edges[0].distance
        merge = False
        if route_a.id != route_b.id and route_a.edges[0].end.id == saving.start.id and route_b.edges[0].end.id == saving.end.id and distance <= self.max_dist:
            merge = True
            route_a.edges.pop()
            route_a.edges = route_a.edges + [edge(saving.start, saving.end)] + route_b.edges[1:]
            route_a.distance = distance
            route_a.reward += route_b.reward
            for i in route_b.edges[:-1]:
                i.end.route = route_a

            #self.routes.pop(self.routes.index(route_b))

        return merge

    def Qsimheuristic_algorithm(self, simheuristico: simheuristic, save = True):
        self.dummy_solution()
        self.create_saving_list()
        dummy_routes = copy.deepcopy(self.routes)
        while len(self.savings) != 0:
            selected_saving = self.select_saving(random=10)
            route_a = copy.deepcopy(selected_saving.start.route)
            merge = self.Qmerge_routes(selected_saving, dummy_routes[selected_saving.end.route.id])
            if merge:
                # Si hacemos el merge, vemos cuanto mejoramos
                node_merged = selected_saving.end.id
                simheuristico.fast_simulation(route_a, self.max_dist, sum([i.end.reward for i in route_a.edges[:-1]]))
                simheuristico.fast_simulation(self.routes[selected_saving.start.route.id],  self.max_dist, sum([i.end.reward for i in self.routes[selected_saving.start.route.id].edges[:-1]]))

                with open('data.txt', 'a') as f:
                    route = route_a
                    selected_nodes = [(edge.end.id, i+1) for i, edge in enumerate(route.edges[:-1])]
                    selected = [i[0] for i in selected_nodes]
                    text = ""
                    for k in range(len(self.nodes)-2):
                        if (k+1) in selected:
                            text += str([i[1] for i in selected_nodes if i[0] == (k+1)][0]) + ";"
                        else:
                            text += "0;"

                    for k in range(len(self.nodes)-2):
                        if (k+1) == node_merged:
                            text += str(np.mean(self.routes[selected_saving.start.route.id].stochastic_of) - np.mean(route_a.stochastic_of)) + ";"
                        else:
                            text += "0;"

                    text = text[:-1] + "\n"
                    f.write(text)

            else:
                # Si hacemos el merge, vemos cuanto mejoramos
                node_merged = selected_saving.end.id

                with open('data.txt', 'a') as f:
                    route = route_a
                    selected_nodes = [(edge.end.id, i+1) for i, edge in enumerate(route.edges[:-1])]
                    selected = [i[0] for i in selected_nodes]
                    text = ""
                    for k in range(len(self.nodes)-2):
                        if (k+1) in selected:
                            text += str([i[1] for i in selected_nodes if i[0] == (k+1)][0]) + ";"
                        else:
                            text += "0;"

                    for k in range(len(self.nodes)-2):
                        if (k+1) == node_merged:
                            text += "-10;"
                        else:
                            text += "0;"

                    text = text[:-1] + "\n"
                    f.write(text)

        #return self.routes, self.of

    def Qselect_saving(self, df, random = 2):
        #
        for i in self.savings[:random]:
            pass

        return self.savings.pop(rnd.randint(0, min([random, len(self.savings)-1])))

    def Qsimheuristic_algorithm2(self, simheuristico: simheuristic, df):
        self.dummy_solution()
        self.create_saving_list()
        while len(self.savings) != 0:
            self.Qselect_saving(df)
            self.merge_routes()

        self.routes.sort(key=lambda x: x.reward, reverse=True)
        self.of = sum([self.routes[i].reward for i in range(self.max_vehicles)])

        simheuristico.simulation(self)
        self.routes.sort(key=lambda x: np.mean(x.stochastic_of), reverse=True)
        self.of = sum([np.mean(self.routes[i].stochastic_of) for i in range(self.max_vehicles)])

        #print(self.of)
        #for i in self.routes:
        #    print(i.__str__())

        return self.routes, self.of

    def Qsimheuristic_multi_start(self, max_time_data, max_time_algo, simheuristic: simheuristic):
        start = time.time()
        self.Qsimheuristic_algorithm(simheuristic)
        while time.time() - start <= max_time_data:
            self.reset()
            self.Qsimheuristic_algorithm(simheuristic)

        df = pd.read_table("data.txt", sep=";", header=None)
        table = pd.DataFrame(columns=[i for i in range(len(self.nodes))])
        for i in range(len(self.nodes), len(self.nodes) - 2 + len(self.nodes) - 2):
            df2 = df.loc[df[i] != 0, [i for i in range(len(self.nodes))]+[i]]
            df2 = df2.groupby([i for i in range(len(self.nodes))]).mean().reset_index()
            table = table.merge(df2, how = "outer")
        table = table.reset_index(drop=True)
        table = table.fillna(0)
        table.to_csv("P.csv")
        while time.time() - start <= max_time_data:
            self.reset()


