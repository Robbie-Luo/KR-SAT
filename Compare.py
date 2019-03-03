from SAT import *
import matplotlib.pyplot as plt
from scipy import stats
def main():
    path_array= ["results/top91_freeman.txt",
                 "results/top91_random_selection.txt",
                 "results/top91_most_often.txt"
                 ]
    for path in path_array:
        res=[]
        for line in open(path):
            t=line.split()[2]
            res.append(float(t))
        arr=np.array(res)
        plt.plot((arr-np.mean(arr))/np.std(arr))
    plt.show()
if __name__ == '__main__':
    main()

