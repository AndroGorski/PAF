import matplotlib.pyplot as plt
import numpy as np
def pravac(x1,y1,x2,y2):
    k=(y2-y1)/(x2-x1)
    l=y1-k*x1
    x=[1,2,3,4,5,6,7,8,9,10]
    y=[]
    for i in range(1,11):
        r=k*i+l
        y.append(r)
    plt.plot(x,y)
    plt.savefig("zad4.pdf",format="pdf")
    plt.show()
pravac(1,1,4,4)