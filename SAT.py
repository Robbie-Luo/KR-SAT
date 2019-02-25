from utilities import *

class SATSolver:
    def __init__(self, cnf):
        self.cnf = cnf
        self.satisfy = "normal"
        self.clauses = []
        self.solution = []

    def initialize(self):
        for rec in self.cnf:
            rec = rec.strip()
            if (rec[0].isdigit()) or (rec[0].startswith("-")):
                clause=list(map(int,rec.split()[:-1]))
                self.clauses.append(clause)

    def solve(self):
        self.solution = solve_dfs(self.clauses)

    def show_results(self):
        print (self.solution)


def main():
    f = open("cnf-test.txt", "r")
    cnf = f.readlines()
    solver = SATSolver(cnf)
    solver.initialize()
    solver.solve()
    solver.show_results()

if __name__ == "__main__":
    main()
