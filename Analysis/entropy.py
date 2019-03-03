from SAT import *
import matplotlib.pyplot as plt
from scipy import stats
def standarize(arr):
    return (arr-np.mean(arr))/np.std(arr)
def main():
    path_sudoku = "sudokus/1000 sudokus.txt"
    path_res    = "results/1000sudokus_most_often.txt"
    entropys=[]
    variables=[]
    times=[]
    recursions=[]
    for line in open(path_sudoku):
        entropys.append(getEntropy(line))
        variables.append(VariableNum(line))
    # entropys=np.array(entropys)
    # entropys=standarize(entropys)
    # variables=np.array(variables)
    # variables=standarize(variables)
    for line in open(path_res):
        t=line.split()[1]
        r=line.split()[2]
        times.append((float(t)))
        recursions.append(int(r))
    print(times)
    print(recursions)


    print(np.corrcoef(times, times))
    print(np.corrcoef(entropys, variables))
    print(np.corrcoef(variables, times))
    print(np.corrcoef(entropys, times))

    data = recursions

    idx = np.argsort(data)
    data =np.sort(data)
    res=[]
    for i in idx:
        # res.append(int(entropys[i]))
        res.append(variables[i])
    th=1
    res = res[th:-th]
    data= data[th:-th]
    print(np.corrcoef(res, data))
    fig, ax = plt.subplots()
    rects1 = ax.bar(res, data, color=(0.2, 0.4, 0.6, 1))
    # plt.ylabel("Average Run time")
    plt.ylabel("Recurions")
    # plt.xlabel("Entropy:sum(log(|v|))")
    plt.xlabel("Number of variables")
    title="Correlation: {:.4f}".format(float(np.corrcoef(res,data)[0,1]))
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    main()

