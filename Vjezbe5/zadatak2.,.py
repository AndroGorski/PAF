def iteracije(N):
    x = 5
    for i in range(N):
        x += 1/3
    for j in range(N):
        x += -1/3
    print(x)
iteracije(200)
iteracije(2000)
iteracije(20000)