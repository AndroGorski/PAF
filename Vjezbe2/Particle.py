import matplotlib.pyplot as plt
import numpy as np
import math as mt
class Particle:
    def __init__(self,x_0,v,heta):
        self.x_0 = x_0
        self.v = v
        self.heta = heta
        self.v_x = v*np.cos(mt.radians(self.heta))
        self.v_y = v*np.sin(mt.radians(self.heta))
        self.x = [x_0]
        self.y =[0]
    def reset(self):
        self.x_0 = 0
        self.v = 0
        self.heta = 0
    def __move(self,dt):
        g = 9.81
        self.v_y = self.v_y - g*dt
        self.y.append(self.y[-1]+self.v_y*dt)
        self.x.append(self.x[-1]+self.v_x*dt)
    def range(self,dt):
        self.v_x = self.v*np.cos(mt.radians(self.heta))
        self.v_y = self.v*np.sin(mt.radians(self.heta))
        self.x = [self.x_0]
        self.y =[0]
        D = 0
        while self.y[-1] >= 0:
            self.__move(dt)
        D = self.x[-1]
        #print("Domet je",D,"metara")
        return D
    def plot_trajectory(self,dt):
        while self.y[-1] >= 0:
            self.__move(dt)
        plt.plot(self.x,self.y)
        plt.xlabel("Prijeđena udaljenost u x smjeru")
        plt.ylabel("Prijeđena udaljenost u y smjeru")
        plt.show()
    def graf_relativne_pogreske(self,dt,t):
        D_anl = (self.v**2*np.sin(2*self.heta))/9.81
        odstupanja = []
        dt_ovi = []
        while dt <= t:
            D = self.range(dt)
            rj = (abs((D - D_anl))/D_anl)*100
            odstupanja.append(rj)
            dt_ovi.append(dt)
            dt += 0.01
        plt.plot(dt_ovi,odstupanja)
        plt.xlabel("Iznos vremenskog koraka dt")
        plt.ylabel("Odstupanje dvaju rjesenja")
        plt.show()



            



        

        