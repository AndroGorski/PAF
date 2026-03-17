try:
    x1=int(input("Unesi x koordinatu za prvu točku:"))
    y1=int(input("Unesi y koordinatu za prvu točku:"))
    x2=int(input("Unesi x koordinatu za drugu točku:"))
    y2=int(input("Unesi y koordinatu za drugu točku:"))
except:
    print("Nešto si krivo unio, probaj ponovo:")
k=(y2-y1)/(x2-x1)
l=y1-k*x1
print("y =",k,"x +",l)