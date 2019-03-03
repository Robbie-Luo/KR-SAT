import random
import sys
import numpy as np

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
            if len(S[i][j])==1:
                H = H + 1
            # H = H + np.log(len(S[i][j]))
    return H


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
    # print assignment
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


# Branching heuristics

def heuristics_dict(heuristic):
    heuristics = {
        'JW'    : jeroslow_wang,
        'RAN'   : random_selection,
        'MO'    : most_often,
        'SPC'   : shortest_positive_clause,
        'FRE'   : freeman,
        'JW2S'  : jeroslow_wang_2_sided
    }
    try:
        return heuristics[heuristic]
    except:
        sys.exit("ERROR: '{}' Not valid heuristic.".format(heuristic) +
                 "\nValid heuristics: {}".format(heuristics.keys()))


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


def shortest_positive_clause(formula):
    min_len = sys.maxint
    best_literal = 0
    for clause in formula:
        negatives = sum(1 for literal in clause if literal < 0)
        if not negatives and len(clause) < min_len:
            best_literal = clause[0]
            min_len = len(clause)
    if not best_literal:
        return formula[0][0]
    return best_literal

def freeman(formula):
    counter = get_difference_counter(formula)
    max_p_literal = max(counter, key=counter.get)
    max_n_literal = min(counter, key=counter.get)
    if counter[max_p_literal] >= abs(counter[max_n_literal]):
        return max_p_literal
    return max_n_literal

def max_key_value(counter):
    keys = counter.keys()
    values = counter.values()
    return keys[values.index(max(values))]


def read_parameters():
    if len(sys.argv) != 3:
        sys.exit("Use:python SAT.py <option> <cnf_file>")
    heuristic = jeroslow_wang
    option = sys.argv[1]
    if "1" in option :
        heuristic = random_selection
        print("Heuristic:random_selection")
    if "2" in option:
        heuristic = jeroslow_wang
        print("Heuristic:jeroslow_wang")
    if "3" in option :
        heuristic = most_often
        print("Heuristic:most_often")
    if "4" in option:
        heuristic = jeroslow_wang_2_sided
        print("Heuristic:jeroslow_wang_2_sided")
    path=sys.argv[2]
    return heuristic, path