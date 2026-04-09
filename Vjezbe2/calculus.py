import numpy as np
from typing import Callable
import matplotlib.pyplot as plt
def derivacije(function: Callable[[float], float], x: float, h: float = 1e-5) -> float: 
    return (function(x + h) - function(x - h)) / (2 * h)

def derivacije_s_granicama(function: Callable[[float], float], donja: float, gornja: float, broj_točaka: int = 10, h: float = 1e-5):
    lista_tocaka = []
    korak = (gornja - donja) / (broj_točaka - 1)
    for i in range(broj_točaka):
        lista_tocaka.append(donja + i * korak)
    lista_derivacija = []
    for x in lista_tocaka:
        der = derivacije(function, x, h)
        lista_derivacija.append(der)
    print(lista_tocaka,lista_derivacija)

def graf_derivacije(function, analiticka_derivacija, polje_x, koraci, ime="f(x)"):    
    x = np.linspace(polje_x[0], polje_x[1], 200)
    analiticka = analiticka_derivacija(x)
    plt.figure(figsize=(12, 6))
    
    plt.plot(x, analiticka, 'k-', linewidth=2.5, label='Analiticka Derivacija', zorder=5)
    colors = plt.cm.tab10(np.linspace(0, 1, len(koraci)))
    for idx, h in enumerate(koraci):
        numericka = np.array([derivacije(function, xi, h) for xi in x])
        plt.plot(x, numericka, '--', linewidth=2, label=f'Numericka vrijednodt (h={h})', color=colors[idx])
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel("f'(x)", fontsize=12)
    plt.title(f'Derivacija od {ime}', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

graf_derivacije(lambda x:x**3, lambda x:2*x**2, [-5, 5], [4, 3, 2, 1], "f(x)=x**3")

def pravokutna_integracija(function: Callable[[float], float],donja: float,gornja: float, podjela: int):
    dx = (gornja - donja) / podjela
    tocke = []
    for i in range(podjela + 1):
        tocke.append(donja + i * dx)
    donja_suma = 0
    for i in range(podjela):
        donja_suma += function(tocke[i]) * dx
    gornja_suma = 0
    for i in range(1, podjela + 1):
        gornja_suma += function(tocke[i]) * dx
    print( donja_suma, gornja_suma, tocke)

def trapezna_integracija(f, a, b, n):
    x_tocke= []
    if n < 2:
        return None
    x = np.linspace(a, b, n)
    y = f(x)
    h = (b - a) / (n - 1)
    y_tocke = [function(x) for x in x_tocke]
    integral = h * (np.sum(y) - 0.5 * (y[0] + y[-1]))
    return integral
    print(integral)
trapezna_integracija(lambda x:x**3,1,8,10)
def graf_integracije(function, analiticki_integral, a, b, koraci, func_name="f(x)"): 
    broj_koraka = np.arange(2, koraci + 1)
    numericke_vrijednosti = []
    for n in broj_koraka:
        numericka = trapezna_integracija(function, a, b, n)
        if n < 2:
            return None
        elif numericka is not None:
            numericke_vrijednosti.append(numericka)
    analiticko_rjesenje = analiticki_integral(a, b)
    plt.figure(figsize=(12, 6))
    plt.plot(broj_koraka[:len(numericke_vrijednosti)], numericke_vrijednosti, 'b-o', 
            linewidth=2, markersize=6, label='Trapezna aproksimacija')
    plt.axhline(y=analiticko_rjesenje, color='red', linestyle='--', linewidth=2.5, 
               label=f'Analiticka vrijednost: {analiticko_rjesenje:.6f}', zorder=5)
    plt.xlabel('Broj koraka (n)', fontsize=12)
    plt.ylabel('Vrijednost integrala', fontsize=12)
    plt.title(f'Graf integracije {func_name}\nfrom x={a} to x={b}', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()




