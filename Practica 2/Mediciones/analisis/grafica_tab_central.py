"""Graficas del rectificador con tab central (capturas filtradas y sincronizadas).

Codificacion de color segun la topologia:
  - tono = rama: azul = rama superior (v_s1, D1, R_D3), naranja = rama inferior (v_s2, D2, R_D4)
  - claridad = carga, de claro a oscuro: R_L -> C_1 (33 uF) -> C_2 (220 uF)
  - salida v_o por carga: amarillo (R_L), magenta (C_1), violeta (C_2); se oscurecen con C
  - trazo como codificacion secundaria: rama superior continua, inferior discontinua

Corriente de cada rama [mA], calculada a partir de la salida medida (R_L = 220 ohm):
  i_D = v_o / R_L + C dv_o/dt  (>= 0, solo donde |v_s| > v_o), asignada a la rama superior cuando v_s1 > 0
  y a la inferior cuando v_s2 = -v_s1 > 0. Las capturas directas en R_D3/R_D4 no se
  usan: registraron el voltaje inverso del diodo (~30 V), no la caida en 1 ohm.

  tab_central.png/.pdf          arriba: semidevanados + salidas; abajo: corriente por rama
  tab_central_dummies.png/.pdf  solo la corriente por rama (lo que medirian R_D3 y R_D4)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from filtro import sincronizada
from estilo import ANCHO_COL, aplicar, cerrar
from paleta import AZUL, NARANJA, SALIDA

aplicar()
RL = 220.0
CARGAS = [r"$R_L$", r"$C_1$", r"$C_2$"]
SALIDAS = [("2110", 0.0), ("2210", 33e-6), ("2310", 220e-6)]
SUP = dict(lw=1.4, ls="-")
INF = dict(lw=1.4, ls=(0, (3.2, 1.6)))


def corrientes_rama(cod, C):
    """t [ms], i_D3 [mA], i_D4 [mA] a partir de v_o."""
    t, vs, vo = sincronizada(cod)
    i_d = np.clip(vo / RL + C * np.gradient(vo, t * 1e-3), 0, None) * 1e3
    conduce = np.abs(vs) > vo          # el diodo solo conduce si el semidevanado supera a v_o
    i_d = np.where(conduce, i_d, 0.0)
    return t, np.where(vs > 0, i_d, 0.0), np.where(vs < 0, i_d, 0.0)


def dibujar_corrientes(ax):
    datos = [corrientes_rama(cod, C) for cod, C in SALIDAS]
    for n, (t, i3, i4) in enumerate(datos):     # orden: D3, D4 por carga -> leyenda en rejilla
        ax.plot(t, i3, color=AZUL[n], label=rf"$i_{{D3}}$: {CARGAS[n]}", **SUP)
        ax.plot(t, i4, color=NARANJA[n], label=rf"$i_{{D4}}$: {CARGAS[n]}", **INF)
    ax.set_ylabel("$i_D$ [mA]")
    # 3 columnas (una por carga); fila superior rama superior, fila inferior rama inferior
    ax.legend(loc="upper center", ncol=3, columnspacing=0.9, handlelength=2.4)
    return max(max(i3.max(), i4.max()) for _, i3, i4 in datos)


# ---- 1) Todo: dos paneles con el mismo eje de tiempo ------------------------
fig, (arr, aba) = plt.subplots(2, 1, figsize=(ANCHO_COL, 3.9), sharex=True)
t, vs, _ = sincronizada("2110")
arr.plot(t, vs, color=AZUL[1], lw=0.8, ls=(0, (1.5, 1.5)), label=r"$v_{s1}$")
arr.plot(t, -vs, color=NARANJA[1], lw=0.8, ls=(0, (1.5, 1.5)), label=r"$v_{s2}$")
for n, (cod, _) in enumerate(SALIDAS):
    t, _, vo = sincronizada(cod)
    arr.plot(t, vo, color=SALIDA[n], lw=1.6, label=rf"$v_o$: {CARGAS[n]}")
arr.axhline(0, color="black", lw=0.4)
arr.set_ylim(-17, 33)                          # franja libre arriba para la leyenda
arr.set_ylabel("$v$ [V]")
arr.legend(loc="upper center", ncol=3, columnspacing=0.9, handlelength=2.2)
arr.grid(alpha=0.3, lw=0.4)
pico = dibujar_corrientes(aba)
aba.set_ylim(-15, pico * 1.6)
cerrar(fig, aba, "", "tab_central")

# ---- 2) Solo la corriente por rama ---------------------------------------------
fig, ax = plt.subplots(figsize=(ANCHO_COL, 2.5))
pico = dibujar_corrientes(ax)
ax.set_ylim(-15, pico * 1.3)
cerrar(fig, ax, "", "tab_central_dummies")
for (cod, C), (_, i3, i4) in zip(SALIDAS, [corrientes_rama(c, C) for c, C in SALIDAS]):
    print(f"{cod}: pico rama sup. {i3.max():.0f} mA, rama inf. {i4.max():.0f} mA")
