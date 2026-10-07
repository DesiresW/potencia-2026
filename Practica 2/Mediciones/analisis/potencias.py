"""P, S y PF a partir del voltaje de salida medido, con R_L = 220 ohm.

Corriente del diodo:  i_D = v_o / R_L + C dv_o/dt   (solo cuando es positiva)
  - Media onda:   i_s = i_D                        ->  S = V_s,rms * I_D,rms
  - Tap central:  cada mitad lleva i_D la mitad del tiempo
                  I_dev,rms = I_D,rms / sqrt(2)    ->  S = 2 * V_dev,rms * I_dev,rms
P = <v_o^2> / R_L (el capacitor no consume potencia promedio). PF = P / S.
"""
import csv
import numpy as np
from filtro import RESULTADOS, filtrar, leer

RL = 220.0
CASOS = [  # codigo, circuito, C [F], teoricos (P, S, PF) o None
    ("1110", "media", 0.0, (0.165, 0.247, 0.668)),
    ("1210", "media", 47e-6, (None, None, 0.52)),
    ("1310", "media", 220e-6, (None, None, 0.35)),
    ("2110", "tab", 0.0, (0.329, 0.493, 0.667)),
    ("2210", "tab", 33e-6, (None, None, 0.55)),
    ("2310", "tab", 220e-6, (None, None, 0.40)),
]


def ciclos_enteros(vs):
    s = np.signbit(vs)
    k = np.where(s[:-1] & ~s[1:])[0]
    return slice(k[0], k[-1])


filas = []
for cod, circ, C, teo in CASOS:
    t, c1, c2 = leer(cod)
    f1, f2 = filtrar(c1, t), filtrar(c2, t)
    vs, vo = (f1, f2) if abs(f1.mean()) < abs(f2.mean()) else (f2, f1)
    i_d = np.clip(vo / RL + C * np.gradient(vo, t), 0, None)
    i_d = np.where(np.abs(vs) > vo, i_d, 0.0)       # solo conduce si |v_s| > v_o
    w = ciclos_enteros(vs)
    vs, vo, i_d = vs[w], vo[w], i_d[w]
    P = np.mean(vo ** 2) / RL
    vs_rms, id_rms = np.sqrt(np.mean(vs ** 2)), np.sqrt(np.mean(i_d ** 2))
    S = vs_rms * id_rms if circ == "media" else 2 * vs_rms * id_rms / np.sqrt(2)
    PF = P / S
    err = [abs(m - t_) / t_ * 100 if t_ else None for m, t_ in zip((P, S, PF), teo)]
    filas.append(dict(codigo=cod, C_uF=C * 1e6, P_W=P, S_VA=S, PF=PF,
                      ID_pico_A=i_d.max(), ID_rms_A=id_rms,
                      errP=err[0], errS=err[1], errPF=err[2]))
    e = lambda x: f"{x:5.1f}%" if x is not None else "   -  "
    print(f"{cod} C={C*1e6:5.0f}uF  P={P:.3f} W  S={S:.3f} VA  PF={PF:.3f}  "
          f"iD_pico={i_d.max()*1e3:6.1f} mA  | err P {e(err[0])} S {e(err[1])} PF {e(err[2])}")

with open(RESULTADOS / "potencias.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, list(filas[0]))
    wr.writeheader()
    wr.writerows(filas)
