from SAT import *

def main():
    path_sudoku="sudokus/1000 sudoku.sdk.txt"
    path_rules="sudoku-rules.txt"
    rs=[]
    jw=[]
    mo=[]
    jw2=[]
    fm=[]
    idx=0
    for line in open(path_sudoku):
        idx+=1
        # print(line)
        print(idx)
        clauses = open(path_rules).readlines()
        for i in range(0, len(line)):
            if line[i].isdigit():
                x = (i) % 9 + 1
                y = ((i + 1) - x) / 9 + 1
                clauses.append("%d" %(x+10*y) + line[i] + " 0\n")

        print('random_selection')
        solver = SATSolver(clauses, random_selection)
        solver.initialize()
        solver.solve()
        res, time, count=solver.get_results()
        str = ''.join(res)+" {:.4f} {}\n".format(time, count)
        print(str)
        rs.append(str)
        
        print('jeroslow_wang')
        solver = SATSolver(clauses, jeroslow_wang)
        solver.initialize()
        solver.solve()
        res, time, count = solver.get_results()
        str = ''.join(res) + " {:.4f} {}\n".format(time, count)
        print(str)
        jw.append(str)
        
        print("jeroslow_wang_2_sided")
        solver = SATSolver(clauses, jeroslow_wang_2_sided)
        solver.initialize()
        solver.solve()
        res, time, count = solver.get_results()
        str = ''.join(res) + " {:.4f} {}\n".format(time, count)
        print(str)
        jw2.append(str)
        
        print('most_often')
        solver = SATSolver(clauses, most_often)
        solver.initialize()
        solver.solve()
        res, time, count = solver.get_results()
        str = ''.join(res) + " {:.4f} {}\n".format(time, count)
        print(str)
        mo.append(str)


        print('freeman')
        solver = SATSolver(clauses, freeman)
        solver.initialize()
        solver.solve()
        res, time, count = solver.get_results()
        str = ''.join(res) + " {:.4f} {}\n".format(time, count)
        print(str)
        fm.append(str)
    
    f = open("results/1000sudokus_random_selection.txt", 'w')
    f.writelines(rs)
    
    f = open("results/1000sudokus_jeroslow_wang.txt", 'w')
    f.writelines(jw)
    
    f = open("results/1000sudokus_jeroslow_wang_2_sided.txt", 'w')
    f.writelines(jw2)
    
    f = open("results/1000sudokus_most_often.txt", 'w')
    f.writelines(mo)

    f = open("results/1000sudokus_freeman.txt", 'w')
    f.writelines(fm)


if __name__ == "__main__":
    main()
