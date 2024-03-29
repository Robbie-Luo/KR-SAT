#!/usr/bin/env python
import random
import sys
import time
import numpy as np

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
        print("Reursions: {}".format(self.count))
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

def VariableNum(line):
    count=0
    for i in range(0, len(line)):
        if line[i].isdigit():
            count+=1
    return 81-count

def getEntropy(line):
    # line = '.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8'
    S=[]
    for i in range(9):
        row=[]
        for j in range(9):
            v = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            row.append(v)
        S.append(row)

    for i in range(0, len(line)):
        if line[i].isdigit():
            x = (i) % 9 + 1
            y = ((i + 1) - x) / 9 + 1
            num = str(line[i])
            for m in range(9):
                if num in S[m][x-1]:
                    S[m][x-1].remove(num)
                if num in S[y-1][m]:
                    S[y-1][m].remove(num)
            u=(x-(x-1)%3-1)
            v=(y-(y-1)%3-1)
            for m in range(u,u+3):
                for n in range(v,v+3):
                    if num in S[n][m]:
                     S[n][m].remove(num)
            S[y-1][x-1]=[num]
    H=0
    for i in range(9):
        for j in range(9):
            # if len(S[i][j])==1:
            #     H = H + 1
            H = H + np.log(len(S[i][j]))
    return H

def read_parameters():
    if len(sys.argv) != 3:
        sys.exit("Use:python SAT.py <option> <cnf_file>")
    heuristic = jeroslow_wang
    option = sys.argv[1]
    if "1" in option :
        heuristic = most_often
        print("Heuristic:Default")
    if "2" in option:
        heuristic = jeroslow_wang_2_sided
        print("Heuristic:jeroslow_wang_2_sided")
    if "3" in option :
        heuristic = DLIS
        print("Heuristic:DLIS")
    path=sys.argv[2]
    return heuristic, path

def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [x for x in clause if x != -unit]
            if not new_clause:
                return -1
            modified.append(new_clause)
        else:
            modified.append(clause)
    return modified


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return counter


def get_weighted_counter(formula, weight=2):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter


def get_weighted_abs_counter(formula, weight=2):
    counter = {}
    for clause in formula:
        for literal in clause:
            literal = abs(literal)
            if literal in counter:
                counter[literal] += weight ** -len(clause)
            else:
                counter[literal] = weight ** -len(clause)
    return counter


def get_difference_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                if literal > 0:
                    counter[literal] += 1
                else:
                    counter[-literal] += - 1
            else:
                if literal > 0:
                    counter[literal] = 1
                else:
                    counter[-literal] = - 1
    return counter


def pure_literal(formula):
    counter = get_counter(formula)
    assignment = []
    pures = []
    for literal, _ in counter.items():
        if -literal not in counter:
            pures.append(literal)
    for pure in pures:
        formula = bcp(formula, pure)
    assignment += pures
    return formula, assignment


def unit_propagation(formula):
    assignment = []
    unit_clauses = [c for c in formula if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        formula = bcp(formula, unit[0])
        assignment += [unit[0]]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = [c for c in formula if len(c) == 1]
    return formula, assignment


def backtracking(formula, assignment, heuristic):
    backtracking.count += 1
    formula, pure_assignment = pure_literal(formula)
    formula, unit_assignment = unit_propagation(formula)
    assignment = assignment + unit_assignment  + pure_assignment
    if formula == - 1:
        return []
    if not formula:
        return assignment

    variable = heuristic(formula)
    solution = backtracking(bcp(formula, variable), assignment + [variable], heuristic)
    if not solution:
        solution = backtracking(bcp(formula, -variable), assignment + [-variable], heuristic)

    return solution


def random_selection(formula):
    counter = get_counter(formula)
    return random.choice(list(counter.keys()))


def jeroslow_wang(formula):
    counter = get_weighted_counter(formula)
    return max(counter, key=counter.get)

def jeroslow_wang_2_sided(formula):
    counter = get_weighted_abs_counter(formula)
    return max(counter, key=counter.get)

def most_often(formula):
    counter = get_counter(formula)
    return max(counter, key=counter.get)

def DLIS(formula):
    counter = get_difference_counter(formula)
    max_p_literal = max(counter, key=counter.get)
    max_n_literal = min(counter, key=counter.get)
    if counter[max_p_literal] >= abs(counter[max_n_literal]):
        return max_p_literal
    return max_n_literal

if __name__ == "__main__":
    main()
