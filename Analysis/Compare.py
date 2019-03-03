from SAT import *
import matplotlib.pyplot as plt
from scipy import stats
def main():
    path_array= [
         "results/1000sudokus_most_often.txt",
         "results/1000sudokus_jeroslow_wang_2_sided.txt",
         "results/1000sudokus_freeman.txt"
                 ]
    data_list=[]
    for path in path_array:
        res=[]
        for line in open(path):
            t=line.split()[1]
            res.append(float(t))
        arr=np.array(res)
        print(np.mean(res))
        arr=(arr-np.mean(arr))
        data_list.append(arr)
        plt.plot(arr)
    print(np.corrcoef(data_list[0],data_list[1]))
    print(np.corrcoef(data_list[0], data_list[2]))
    print(np.corrcoef(data_list[1], data_list[2]))
    # plt.show()
if __name__ == '__main__':
    main()

