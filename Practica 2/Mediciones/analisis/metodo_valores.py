"""Grafica 2x1 con marcadores sobre las capturas filtradas (estilo de la figura del filtro).

Arriba (1.2.1): marcadores verticales = inicio y fin de cada recarga del capacitor
                (intervalo de conduccion del diodo), con su duracion y angulo.
Abajo  (2.2.1): marcadores horizontales = V_pico, V_rms, V_DC y V_min en ciclos enteros.
Exporta metodo_valores.png y .pdf al ancho de columna del informe (ver estilo.py). Ventana de 40 ms.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from filtro import FIGURAS, filtrar, leer
from estilo import ANCHO_COL, aplicar

aplicar()
AZUL, GRIS, MARCA = "#1f4e9c", "#bbbbbb", "#555555"   # misma paleta que la figura del filtro
F_RED = 60.0
VENTANA = (-20, 20)                                     # ms
CAJA = dict(boxstyle="round,pad=0.2", fc="white", ec="0.75", lw=0.4)


def cruces_subida(vs):
    s = np.signbit(vs)
    return np.where(s[:-1] & ~s[1:])[0]


fig, (arr, aba) = plt.subplots(2, 1, figsize=(ANCHO_COL, 3.3), sharex=True)

# ---- Arriba: intervalo de conduccion (marcadores verticales) ---------------
t, c1, c2 = leer("1210")
vs, vo = filtrar(c1, t), filtrar(c2, t)
ms = t * 1e3
dist = int(0.8 / F_RED / np.median(np.diff(t)))
picos, _ = find_peaks(vo, distance=dist, prominence=1)
valles, _ = find_peaks(-vo, distance=dist, prominence=1)
arr.plot(ms, vs, color=GRIS, lw=0.6, label=r"$v_s$")
arr.plot(ms, vo, color=AZUL, lw=1.3, label=r"$v_o$")
duraciones = []
for v in valles:
    p = picos[picos > v]
    if not len(p):
        continue
    p = p[0]
    arr.axvspan(ms[v], ms[p], color=AZUL, alpha=0.08, lw=0)
    for i in (v, p):
        arr.axvline(ms[i], color=MARCA, ls="--", lw=0.5)
    duraciones.append(t[p] - t[v])
dt = np.mean(duraciones)
arr.text(0.99, 0.06, rf"conducción: $\Delta t$ = {dt*1e3:.1f} ms ($\theta \approx$ {dt*F_RED*360:.0f}°)",
         transform=arr.transAxes, ha="right", va="bottom", fontsize=6.5, bbox=CAJA)
arr.set_title(r"1.2.1: media onda, $C_1$, sobre $R_L$", loc="left")
arr.set_ylabel(r"$v$ [V]")
arr.legend(loc="lower left", ncol=2, framealpha=1, edgecolor="0.75")
arr.grid(alpha=0.3, lw=0.4)

# ---- Abajo: niveles calculados (marcadores horizontales) -------------------
t, c1, c2 = leer("2210")
f1, f2 = filtrar(c1, t), filtrar(c2, t)
vs, vo = (f2, f1) if abs(f1.mean()) > abs(f2.mean()) else (f1, f2)   # canales invertidos
k = cruces_subida(vs)
w = slice(k[0], k[-1])
x, ms = vo[w], t[w] * 1e3
rms, dc = np.sqrt(np.mean(x ** 2)), x.mean()
fr = np.sqrt(rms ** 2 - dc ** 2) / dc * 100
niveles = [(x.max(), r"$V_{pico}$", "bottom"), (x.min(), r"$V_{min}$", "top")]
aba.plot(ms, x, color=AZUL, lw=1.3)
for valor, nombre, va in niveles:
    aba.axhline(valor, color=MARCA, ls="--", lw=0.5)
    aba.text(VENTANA[1] - 0.3, valor, f"{nombre} = {valor:.2f} V", ha="right", va=va,
             fontsize=6.5, bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
# V_rms y V_DC quedan muy cerca: lineas en dos tonos y una sola etiqueta para ambas
aba.axhline(rms, color="#c0392b", ls="--", lw=0.6)
aba.axhline(dc, color="#1e8449", ls="--", lw=0.6)
aba.text(VENTANA[1] - 0.3, rms + 0.25, rf"$V_{{rms}}$ = {rms:.2f} V,  $V_{{DC}}$ = {dc:.2f} V",
         ha="right", va="bottom", fontsize=6.5,
         bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"))
aba.text(0.01, 0.95, rf"$FR = \sqrt{{V_{{rms}}^2 - V_{{DC}}^2}}\,/\,V_{{DC}} = {fr:.1f}\,\%$",
         transform=aba.transAxes, ha="left", va="top", fontsize=6.5, bbox=CAJA)
aba.set_ylim(x.min() - 1.4, x.max() + 3.0)
aba.set_title(r"2.2.1: tab central, $C_1$, sobre $R_L$", loc="left")
aba.set_xlabel("Tiempo [ms]")
aba.set_ylabel(r"$v_o$ [V]")
aba.grid(alpha=0.3, lw=0.4)

aba.set_xlim(*VENTANA)
fig.align_ylabels((arr, aba))
fig.tight_layout(pad=0.3, h_pad=0.5)
for ext, dpi in (("png", 300), ("pdf", None)):
    fig.savefig(FIGURAS / f"metodo_valores.{ext}", dpi=dpi)
print(f"dt = {dt*1e3:.2f} ms, FR 2.2.1 = {fr:.1f} %")
