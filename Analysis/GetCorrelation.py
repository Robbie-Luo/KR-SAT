from SAT import *
import matplotlib.pyplot as plt
from scipy import stats
def standarize(arr):
    return (arr-np.mean(arr))/np.std(arr)
def main():
    path_sudoku = "sudokus/1000 sudokus.txt"
    path_res    = "results/1000sudokus_freeman.txt"
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

    data_x = [int(x) for x in variables]
    data_y = times
    xlabel = range(np.min(data_x), np.max(data_x))
    ylabel = []
    for x in xlabel:
        tmp = []
        for i in range(len(data_x)):
            if (data_x[i] == x):
                tmp.append(data_y[i])
        ylabel.append(sum(tmp) / len(tmp))
    print np.corrcoef(xlabel[:-6], ylabel[:-6])
    fig, ax = plt.subplots()
    ax.bar(xlabel, ylabel, color=(0.2, 0.4, 0.6, 1))
    plt.ylabel("Average Run time")
    # plt.ylabel("Recursions")
    # plt.xlabel("Entropy:sum(log(|v|))")
    plt.xlabel("Number of variables")
    title = "Correlation: {:.4f}".format(float(np.corrcoef(xlabel, ylabel)[0, 1]))
    plt.title(title)
    plt.show()


    data_x = [int(x) for x in variables]
    data_y = recursions
    xlabel=range(np.min(data_x), np.max(data_x))
    ylabel=[]
    for x in xlabel:
        tmp=[]
        for i in range(len(data_x)):
            if(data_x[i]==x):
                tmp.append(data_y[i])
        ylabel.append(sum(tmp)/len(tmp))
    fig, ax = plt.subplots()
    ax.bar(xlabel, ylabel, color=(0.2, 0.4, 0.6, 1))
    # plt.ylabel("Average Run time")
    plt.ylabel("Recursions")
    # plt.xlabel("Entropy:sum(log(|v|))")
    plt.xlabel("Number of variables")
    title="Correlation: {:.4f}".format(float(np.corrcoef(xlabel, ylabel)[0,1]))
    plt.title(title)
    plt.show()

    data_x = [int(x) for x in entropys]
    data_y = times
    xlabel = range(np.min(data_x), np.max(data_x))
    ylabel = []
    for x in xlabel:
        tmp = []
        for i in range(len(data_x)):
            if (data_x[i] == x):
                tmp.append(data_y[i])
        ylabel.append(sum(tmp) / len(tmp))
    print np.corrcoef(xlabel[:-6], ylabel[:-6])
    fig, ax = plt.subplots()
    ax.bar(xlabel[:-6], ylabel[:-6], color=(0.2, 0.4, 0.6, 1))
    plt.ylabel("Average Run time")
    # plt.ylabel("Recursions")
    plt.xlabel("Entropy:sum(log(|v|))")
    # plt.xlabel("Number of variables")
    title = "Correlation: {:.4f}".format(float(np.corrcoef(xlabel[:-6], ylabel[:-6])[0, 1]))
    plt.title(title)
    plt.show()

    data_x = [int(x) for x in entropys]
    data_y = recursions
    xlabel = range(np.min(data_x), np.max(data_x))
    ylabel = []
    for x in xlabel:
        tmp = []
        for i in range(len(data_x)):
            if (data_x[i] == x):
                tmp.append(data_y[i])
        ylabel.append(sum(tmp) / len(tmp))
    print np.corrcoef(xlabel[:-6], ylabel[:-6])
    fig, ax = plt.subplots()
    ax.bar(xlabel[:-6], ylabel[:-6], color=(0.2, 0.4, 0.6, 1))
    # plt.ylabel("Average Run time")
    plt.ylabel("Recursions")
    plt.xlabel("Entropy:sum(log(|v|))")
    # plt.xlabel("Number of variables")
    title = "Correlation: {:.4f}".format(float(np.corrcoef(xlabel[:-6], ylabel[:-6])[0, 1]))
    plt.title(title)
    plt.show()
if __name__ == '__main__':
    main()

