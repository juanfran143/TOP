from classes import node

def read(name = "Instances\\tsiligirides_problem_1_budget_40.txt"):
    nodes = []
    f = open(name, "r")
    f1 = open(name, "r")
    a = f1.read()

    capacity, vehicles = f.readline()[:-1].split("\t")
    aux = f.readline()[:-1].split("\t")
    nodes.append(node(0, 0, float(aux[0]), float(aux[1])))
    aux = f.readline()[:-1].split("\t")
    nodes.append(node(a.count("\n"), 0, float(aux[0]), float(aux[1])))

    aux = f.readline()[:-1].split("\t")
    i = 1
    while len(aux) != 1:
        nodes.append(node(i, float(aux[2]), float(aux[0]), float(aux[1])))
        i += 1
        aux = f.readline()[:-1].split("\t")

    nodes.append(nodes[1])
    nodes.pop(1)

    return nodes, int(capacity), int(vehicles)