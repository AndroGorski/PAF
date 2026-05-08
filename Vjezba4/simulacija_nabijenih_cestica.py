

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D

NABOJ_ELEKTRONA = -1.602e-19  # C
NABOJ_POZITRONA = 1.602e-19   # C
MASA_ELEKTRONA = 9.109e-31    # kg


class SimulatorNabijeneČestice:
    
    def __init__(self, masa, naboj, električno_polje, magnetno_polje):
        self.masa = masa
        self.naboj = naboj
        self.električno_polje = np.array(električno_polje)
        self.magnetno_polje = np.array(magnetno_polje)
    
    def jednadžba_gibanja(self, položaj_brzina, vrijeme):
        x, y, z, vx, vy, vz = položaj_brzina
        brzina = np.array([vx, vy, vz])
        vektorski_produkt = np.cross(brzina, self.magnetno_polje)
        sila = self.naboj * (self.električno_polje + vektorski_produkt)
        akceleracija = sila / self.masa
        return [vx, vy, vz, akceleracija[0], akceleracija[1], akceleracija[2]]
    
    def simuliraj(self, početni_položaj, početna_brzina, vrijeme_simulacije, broj_koraka):
        početni_uvjet = list(početni_položaj) + list(početna_brzina)
        vremenske_točke = np.linspace(0, vrijeme_simulacije, broj_koraka)
        putanja = odeint(self.jednadžba_gibanja, početni_uvjet, vremenske_točke)
        return vremenske_točke, putanja
    
    
def nacrtaj_3d_putanju(vremenske_točke, putanja, naslov, boja='blue'):
    fig = plt.figure(figsize=(12, 5))
    
    ax1 = fig.add_subplot(121, projection='3d')
    x, y, z = putanja[:, 0], putanja[:, 1], putanja[:, 2]
    ax1.plot(x, y, z, color=boja, linewidth=1.5, label='Putanja')
    ax1.scatter(x[0], y[0], z[0], color='green', s=100, label='Početak', marker='o')
    ax1.scatter(x[-1], y[-1], z[-1], color='red', s=100, label='Kraj', marker='s')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_zlabel('z (m)')
    ax1.set_title(f'{naslov} - 3D putanja')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2 = fig.add_subplot(122)
    ax2.plot(x, y, color=boja, linewidth=1.5, label='xy-projekcija')
    ax2.scatter(x[0], y[0], color='green', s=100, marker='o')
    ax2.scatter(x[-1], y[-1], color='red', s=100, marker='s')
    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('y (m)')
    ax2.set_title(f'{naslov} - xy-projekcija')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')
    
    plt.tight_layout()
    return fig

def usporedba_elektrona_i_pozitrona():
    print("=" * 70)
    print("USPOREDBA ELEKTRONA I POZITRONA U MAGNETNOM POLJU")
    print("=" * 70)
    
    B_vektor = (0, 0, 1e-3) 
    E_vektor = (0, 0, 0)      
    početni_položaj = (0, 0, 0)
    početna_brzina = (1e6, 2e6, 3e6)  
    vrijeme_simulacije = 2e-8  
    broj_koraka = 2000
    
    
    print("\n[ELEKTRON]")
    simulator_elektron = SimulatorNabijeneČestice(
        MASA_ELEKTRONA,
        NABOJ_ELEKTRONA,
        E_vektor,
        B_vektor
    )
    vrijeme_e, putanja_e = simulator_elektron.simuliraj(
        početni_položaj, početna_brzina, vrijeme_simulacije, broj_koraka
    )
    print(f"Početna brzina: {početna_brzina}")
    print(f"Ciklotronska frekvencija: {abs(NABOJ_ELEKTRONA) * np.linalg.norm(B_vektor) / MASA_ELEKTRONA / (2*np.pi):.2e} Hz")
    
    
    print("\n[POZITRON]")
    simulator_pozitron = SimulatorNabijeneČestice(
        MASA_ELEKTRONA,  
        NABOJ_POZITRONA,
        E_vektor,
        B_vektor
    )
    vrijeme_p, putanja_p = simulator_pozitron.simuliraj(
        početni_položaj, početna_brzina, vrijeme_simulacije, broj_koraka
    )
    print(f"Početna brzina: {početna_brzina}")
    print(f"Ciklotronska frekvencija: {abs(NABOJ_POZITRONA) * np.linalg.norm(B_vektor) / MASA_ELEKTRONA / (2*np.pi):.2e} Hz")
    
    
    fig = plt.figure(figsize=(16, 6))
    
    
    ax1 = fig.add_subplot(131, projection='3d')
    x_e, y_e, z_e = putanja_e[:, 0], putanja_e[:, 1], putanja_e[:, 2]
    x_p, y_p, z_p = putanja_p[:, 0], putanja_p[:, 1], putanja_p[:, 2]
    
    ax1.plot(x_e, y_e, z_e, 'b-', linewidth=1.5, label='Elektron', alpha=0.7)
    ax1.plot(x_p, y_p, z_p, 'r-', linewidth=1.5, label='Pozitron', alpha=0.7)
    ax1.scatter(x_e[0], y_e[0], z_e[0], color='blue', s=100, marker='o')
    ax1.scatter(x_p[0], y_p[0], z_p[0], color='red', s=100, marker='o')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_zlabel('z (m)')
    ax1.set_title('3D putanje - Elektron vs Pozitron')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    
    ax2 = fig.add_subplot(132)
    ax2.plot(x_e, y_e, 'b-', linewidth=1.5, label='Elektron', alpha=0.7)
    ax2.plot(x_p, y_p, 'r-', linewidth=1.5, label='Pozitron', alpha=0.7)
    ax2.scatter(x_e[0], y_e[0], color='blue', s=100, marker='o')
    ax2.scatter(x_p[0], y_p[0], color='red', s=100, marker='o')
    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('y (m)')
    ax2.set_title('xy-projekcija')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    
    ax3 = fig.add_subplot(133)
    ax3.plot(vrijeme_e, z_e, 'b-', linewidth=1.5, label='Elektron')
    ax3.plot(vrijeme_p, z_p, 'r-', linewidth=1.5, label='Pozitron')
    ax3.set_xlabel('Vrijeme (s)')
    ax3.set_ylabel('z (m)')
    ax3.set_title('z-koordinata tijekom vremena')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    fig.suptitle('Usporedba elektrona i pozitrona u B = (0, 0, 1 mT)', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig

def demonstracija_različitih_polja():
    print("\n" + "=" * 70)
    print("DEMONSTRACIJA ZA RAZLIČITE KOMBINACIJE E I B POLJA")
    print("=" * 70)
    
    scenariji = [
        {
            'naziv': 'Samo magnetno polje B = (0, 0, 1 mT)',
            'E_polje': (0, 0, 0),
            'B_polje': (0, 0, 1e-3),
            'boja': 'blue'
        },
        {
            'naziv': 'Električno polje E = (1e5 V/m, 0, 0) + B = (0, 0, 1 mT)',
            'E_polje': (1e5, 0, 0),
            'B_polje': (0, 0, 1e-3),
            'boja': 'green'
        },
        {
            'naziv': 'Električno polje E = (0, 0, 1e5 V/m) + B = (0, 0, 1 mT)',
            'E_polje': (0, 0, 1e5),
            'B_polje': (0, 0, 1e-3),
            'boja': 'orange'
        },
        {
            'naziv': 'Električno polje E = (1e5, 1e5, 0) V/m + B = (0, 0, 2 mT)',
            'E_polje': (1e5, 1e5, 0),
            'B_polje': (0, 0, 2e-3),
            'boja': 'purple'
        }
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), subplot_kw=dict(projection='3d'))
    axes = axes.flatten()
    početni_položaj = (0, 0, 0)
    početna_brzina = (1e6, 2e6, 3e6)
    vrijeme_simulacije = 2e-8
    broj_koraka = 2000
    
    for idx, scenarij in enumerate(scenariji):
        print(f"\n[{idx+1}] {scenarij['naziv']}")
        simulator = SimulatorNabijeneČestice(
            MASA_ELEKTRONA,
            NABOJ_ELEKTRONA,
            scenarij['E_polje'],
            scenarij['B_polje']
        )
        vrijeme, putanja = simulator.simuliraj(
            početni_položaj, početna_brzina, vrijeme_simulacije, broj_koraka
        )
        x, y, z = putanja[:, 0], putanja[:, 1], putanja[:, 2]
        ax = axes[idx]
        ax.plot(x, y, z, color=scenarij['boja'], linewidth=1.5, alpha=0.8)
        ax.scatter(x[0], y[0], z[0], color='green', s=100, marker='o', label='Početak')
        ax.scatter(x[-1], y[-1], z[-1], color='red', s=100, marker='s', label='Kraj')
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_zlabel('z (m)')
        ax.set_title(scenarij['naziv'], fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        brzina_završna = np.sqrt(putanja[-1, 3]**2 + putanja[-1, 4]**2 + putanja[-1, 5]**2)
        distanca = np.linalg.norm([x[-1], y[-1], z[-1]])
        print(f"  Završna brzina: {brzina_završna:.2e} m/s")
        print(f"  Distanca od početka: {distanca:.2e} m")
    fig.suptitle('Gibanje elektrona za različite kombinacije E i B polja', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig
