#!/usr/bin/env python
import time
import numpy as np
from utilities import *

trackback_times=0
class SATSolver:
    def __init__(self, cnf, heuristic):
        self.cnf = cnf
        self.heuristic = heuristic
        self.clauses = []
        self.literals = []
        self.solution = []
        self.time = 0
        self.count = 0

    def initialize(self):
        for line in self.cnf:
            if line.startswith('p'):
                continue
            clause = [int(x) for x in line[:-2].split()]
            for l in clause:
                if abs(l) not in self.literals:
                    self.literals.append(abs(l))
            self.clauses.append(clause)

    def solve(self):
        start = time.time()
        backtracking.count = 0
        self.solution = backtracking(self.clauses, [], self.heuristic)
        end = time.time()
        # print("Heuristic: "+str(self.heuristic))
        self.time = end - start

        self.count = backtracking.count

    def get_results(self):
        S = [x for x in sorted(self.solution) if x > 0]
        res = ''.join([(str(s)[-1]) for s in S])
        return res, self.time, self.count

    def show_results(self):
        print("Time: {:.4f}".format(self.time))
        print("Count: {}".format(self.count))
        if self.solution:
            S= [x for x in sorted(self.solution) if x > 0]
            print(np.array([int(str(s)[-1]) for s in S]).reshape(9, 9))
        else:
            print('UNSATISFIABLE')


def main():
    heuristic, path = read_parameters()
    f = open(path, "r")
    cnf = f.readlines()
    solver = SATSolver(cnf, heuristic)
    solver.initialize()
    solver.solve()
    solver.show_results()


if __name__ == "__main__":
    main()
