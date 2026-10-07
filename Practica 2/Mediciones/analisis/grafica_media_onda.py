"""Graficas del rectificador de media onda (capturas filtradas y sincronizadas).

  media_onda.png/.pdf          fuente + salidas; eje derecho = misma curva en mA (i = v_o / R_L)
  media_onda_dummies.png/.pdf  solo la corriente en R_D1 en las tres configuraciones
Criterio del informe: la corriente se calcula como i = v_o / R_L con R_L = 220 ohm, a partir
de la misma captura de v_o (no se usan las capturas directas de la dummy).
Ancho = columna del informe (3.77 in); ver estilo.py.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filtro import sincronizada
from estilo import ANCHO_COL, COLOR, ESTILO_V, FUENTE, aplicar, cerrar

aplicar()
RL = 220.0
# (salida, etiqueta, clave de color)
CONFIG = [("1110", r"$R_L$", "R"), ("1210", r"$C_1$", "C1"), ("1310", r"$C_2$", "C2")]
ETIQ_I = r"$i_{RD1} = v_o/R_L$ [mA]"

# ---- 1) Todo: voltajes + corrientes ---------------------------------------
fig, ax = plt.subplots(figsize=(ANCHO_COL, 2.7))
t, vs, _ = sincronizada("1110")
ax.plot(t, vs, label=r"$v_s$", **FUENTE)
for sal, etiqueta, c in CONFIG:
    t, _, vo = sincronizada(sal)
    ax.plot(t, vo, color=COLOR[c], label=rf"$v_o$: {etiqueta}", **ESTILO_V)
ax.set_ylim(-17, 17)
ax.set_ylabel("$v$ [V]")
# i = v_o / R_L tiene la misma forma que v_o: el eje derecho solo traduce la curva a mA
der = ax.secondary_yaxis("right", functions=(lambda v: v / RL * 1e3, lambda i: i * RL / 1e3))
der.set_ylabel(ETIQ_I)
ax.legend(loc="lower left")
cerrar(fig, ax, "", "media_onda")

# ---- 2) Solo la corriente ----------------------------------------------------
fig, ax = plt.subplots(figsize=(ANCHO_COL, 2.5))
for sal, etiqueta, c in CONFIG:
    t, _, vo = sincronizada(sal)
    ax.plot(t, vo / RL * 1e3, color=COLOR[c], label=etiqueta, **ESTILO_V)
ax.set_ylabel(ETIQ_I)
ax.legend(loc="upper right")
cerrar(fig, ax, "", "media_onda_dummies")
for sal, etiqueta, _ in CONFIG:
    _, _, vo = sincronizada(sal)
    print(f"{sal}: pico {vo.max() / RL * 1e3:.1f} mA, promedio {vo.mean() / RL * 1e3:.1f} mA")
