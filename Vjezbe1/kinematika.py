import matplotlib.pyplot as plt
def jednoliko_gibanje(F,m):
    ak=F/m
    t=[1,2,3,4,5,6,7,8,9,10]
    a=[]
    v=[]
    x=[]
    for i in range(1,11):
        r=ak*i
        v.append(r)
        z=(ak*i**2)/2
        x.append(z)
        a.append(ak)
    plt.subplot(3,2,1)
    plt.title("x-t graf")
    plt.xlabel("t/s")
    plt.ylabel("x/m")
    plt.plot(t,x)

    plt.subplot(3,2,2)
    plt.title("v-t graf")
    plt.xlabel("t/s")
    plt.ylabel("v/m*s**-1")
    plt.plot(t,v)

    plt.subplot(3,2,3)
    plt.title("a-t graf")
    plt.xlabel("t/s")
    plt.ylabel("a/m*s**-2")
    plt.plot(t,a)
    plt.tight_layout()
    plt.show()
