from SAT import *
import matplotlib.pyplot as plt
from scipy import stats
def main():
    path_sudoku = "sudokus/top91.sdk.txt"
    path_res    = "results/top91_most_often.txt"
    entropys=[]
    times=[]
    for line in open(path_sudoku):
        H = getEntropy(line)
        entropys.append(H)
    for line in open(path_res):
        t=line.split()[2]
        times.append(float(t))
    # print(entropys)
    # print(times)
    print(np.corrcoef(entropys,times))
    idx = np.argsort(times)
    times=np.sort(times)
    res=[]
    for i in idx:
        res.append(int(entropys[i]))
    print(res)
    print(times)

    plt.bar(res,times)
    plt.show()
if __name__ == '__main__':
    main()

