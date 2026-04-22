import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from enum import Enum
from dataclasses import dataclass
class IntegrationMethod(Enum):
@dataclass
class SimulationResult:
    dt: float
    method: IntegrationMethod
    trajectory: np.ndarray  
    time_array: np.ndarray
    final_range: float
    max_height: float
    valid: bool  
    issues: List[str] = None

class Projectile:
    def __init__(self, masa: float, koeficijent_otpora: float, povrsina: float, 
                 gustoca_zraka: float = 1.225):
        self.masa = masa
        self.koeficijent_otpora = koeficijent_otpora
        self.povrsina = povrsina
        self.gustoca_zraka = gustoca_zraka
        self.gravitacija = 9.81  
        
    def izracunaj_silu_otpora(self, brzina: np.ndarray) -> np.ndarray:
        vektor_brzine = np.linalg.norm(brzina)
        if vektor_brzine < 1e-10:  
            return np.array([0.0, 0.0])
        
        sila_otpora = 0.5 * self.gustoca_zraka * self.koeficijent_otpora * self.povrsina * vektor_brzine**2 # Skalarni oblik sile
        sila_otpora_vektor = -sila_otpora * (brzina / vektor_brzine) # Vektorski oblik sile
        return sila_otpora_vektor
    
    def izracunaj_akceleraciju(self, brzina: np.ndarray) -> np.ndarray:
        sila_otpora_vektor = self.calculate_drag_force(brzina)
        gravitaciska_sila = np.array([0.0, -self.masa * self.gravitacija])
        totalna_sila = sila_otpora_vektor + gravitaciska_sila
        akceleracija = totalna_sila / self.masa
        return akceleracija
    
    def simuliraj_euler(self, pocetna_brzina: np.ndarray, pocetan_polozaj: np.ndarray,
                      dt: float) -> Tuple[np.ndarray, np.ndarray]:
        pozicija = pocetan_polozaj.copy().astype(float)
        brzina = pocetna_brzina.copy().astype(float)
        domet = [pozicija.copy()]
        vremena = [0.0]
        trenutno_vrijeme = 0.0
        while pozicija[1] > 0: 
            akceleracija = self.calculate_acceleration(brzina)
            brzina__nova = brzina + akceleracija * dt
            pozicija = pozicija + brzina * dt
            brzina = brzina__nova
            trenutno_vrijeme_vrijeme += dt
            domet.append(pozicija.copy())
            vremena.append(trenutno_vrijeme)
        return np.array(domet), np.array(vremena)
    
    def derivacija_statusa(self, status: np.ndarray) -> np.ndarray:
        pozicija = status[0:2]
        brzina = status[2:4]
        akceleracija = self.calculate_acceleration(brzina)
        return np.array([brzina[0],brzina[1],akceleracija[0],akceleracija[1]])

    def simuliraj_rk4(self, pocetna_brzina: np.ndarray, pocetni_polozaj: np.ndarray,
                    dt: float) -> Tuple[np.ndarray, np.ndarray]:
        status = np.array([pocetni_polozaj[0],pocetni_polozaj[1],pocetna_brzina[0],pocetna_brzina[1]],dtype=float)
        domet = [status[0:2].copy()]
        vremena = [0.0]
        trenutno_vrijeme = 0.0
        while status[1] > 0:
            k1 = self.state_derivative(status)
            k2 = self.state_derivative(status + 0.5 * dt * k1)  
            k3 = self.state_derivative(status + 0.5 * dt * k2)
            k4 = self.state_derivative(status + dt * k3)
            status = status + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
            trenutno_vrijeme += dt
            domet.append(status[0:2].copy())
            vremena.append(trenutno_vrijeme)
        return np.array(domet), np.array(vremena)
    def simulacija(self,pocetna_brzina: np.ndarray,pocetan_polozaj: np.ndarray,dt: float, method: IntegrationMethod = IntegrationMethod.EULER,) -> Tuple[np.ndarray, np.ndarray]:
        if method == IntegrationMethod.EULER:
            return self.simuliraj_euler(pocetna_brzina, pocetan_polozaj, dt)
        elif method == IntegrationMethod.RK4:
            return self.simuliraj_rk4(pocetna_brzina, pocetan_polozaj, dt)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def provjera_tocnosti(self, domet: np.ndarray,vremena: np.ndarray) -> Tuple[bool, List[str]]:
        problemi = []
        if np.any(np.isnan(domet)) or np.any(np.isinf(domet)):
            problemi.append("NaN or Inf vrijednosti detektirane")
            return False, problemi
        if len(vremena) > 1:
            dt_vrijednosti = np.diff(vremena)
            if np.any(dt_vrijednosti <= 0):
                problemi.append("Nemonotonski vremenski interval")
                return False, problemi
        if len(domet) > 1:
            dx = np.diff(domet[:, 0])
            pomicanje_unatrag = np.sum(dx < -1e-6)
            if pomicanje_unatrag> 0:
                problemi.append(f"Pomicanje unatrag otkriveno u x ({pomicanje_unatrag} koraka)")
        
        if len(domet) > 3:
            visine = domet[:, 1]
            razlike_visina = np.diff(visine)
            neobicno_ponasanje = 0
            for i in range(1, len(razlike_visina)):
                if razlike_visina[i-1] < -1e-3 and razlike_visina[i] > 1e-3:
                    neobicno_ponasanje += 1
            if neobicno_ponasanje > 2:
                problemi.append(f"Draticnja oscilacija visine,({neobicno_ponasanje} preokreta)")
        validno = len(problemi) == 0
        return validno, problemi


def usporedba_metoda(projectile: Projectile, pocetna_brzna: float, 
                   kut_u_stupnjevima: float, dt: float = 0.01) -> Tuple[SimulationResult, SimulationResult]:
    kut_u_radijanima = np.radians(kut_u_stupnjevima)
    pocetne_brzine = pocetna_brzna * np.array([np.cos(kut_u_radijanima), np.sin(kut_u_radijanima)])
    pocetan_polozaj = np.array([0.0, 0.0])
    print(f"Pokretanje simulacije koristeci Eulerovu metodu (dt={dt}s)...")
    domet_euler, vrime_euler = projectile.simulate(pocetne_brzine, pocetan_polozaj, dt, 
                                                  method=IntegrationMethod.EULER)
    valid_euler, problemi_euler = projectile.check_physical_validity(domet_euler, vrime_euler) 
    rezultati_euler = SimulationResult(
        dt=dt,
        method=IntegrationMethod.EULER,
        domet=domet_euler,
        vremena=vrime_euler,
        finalni_domet=domet_euler[-1, 0],
        vrhunac=np.max(domet_euler[:, 1]),
        valid=valid_euler,
        problemi1=problemi_euler
    )
    print(f"Pokretanje simulacije sa RK4 metodom (dt={dt}s)...")
    domet_rk4, vrime_rk4 = projectile.simulate(pocetne_brzine,pocetan_polozaj, dt, 
                                             method=IntegrationMethod.RK4)
    valid_rk4, problemi_rk4 = projectile.check_physical_validity(domet_rk4, vrime_rk4)
    rezultati_rk4 = SimulationResult(
        dt=dt,
        method=IntegrationMethod.RK4,
        domet=domet_rk4,
        vremena=vrime_rk4,
        finalni_domet=domet_rk4[-1, 0],
        vrhunac=np.max(domet_rk4[:, 1]),
        valid=valid_rk4,
        problemi2=problemi_rk4
    ) 
    return rezultati_euler, rezultati_rk4

def plot_method_comparison(result_euler: SimulationResult, result_rk4: SimulationResult,
                          title: str = "Euler vs RK4 Comparison"):
    """Plot comparison of trajectories from both methods"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    ax = axes[0, 0]
    ax.plot(result_euler.domet[:, 0], result_euler.domet[:, 1], 
           'b-', linewidth=2.5, label="Eulerova metoda", marker='o', markersize=3, 
           markevery=max(1, len(result_euler.domet)//20))
    ax.plot(result_rk4.domet[:, 0], result_rk4.domet[:, 1], 
           'r--', linewidth=2.5, label="RK4 metoda", marker='s', markersize=3,
           markevery=max(1, len(result_rk4.domet)//20))
    ax.set_xlabel("Domet (m)", fontsize=11)
    ax.set_ylabel("Visina (m)", fontsize=11)
    ax.set_title("Usporedba hitaca", fontsize=12)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)
