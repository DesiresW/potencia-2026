"""Grafica antes/despues del filtro: dos ejemplos, cada uno con su acercamiento.

Exporta antes_despues_filtro.png y .pdf al ancho de columna del informe (ver estilo.py).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filtro import FC, FIGURAS, filtrar, leer
from estilo import ANCHO_COL, aplicar

aplicar()
CRUDO, FILTRADO = "#b5b5b5", "#1f4e9c"

# (archivo, canal, titulo del panel, etiqueta del eje, escala)
EJEMPLOS = [
    ("1320", 2, r"1.3.2: media onda, $C_2$, captura en $R_{D1}$", r"$v_{RD1}$ [mV]", 1e3),
    ("2310", 1, r"2.3.1: tab central, $C_2$, sobre $R_L$", r"$v_o$ [V]", 1.0),
]

fig, ax = plt.subplots(len(EJEMPLOS), 2, figsize=(ANCHO_COL, 3.1),
                       gridspec_kw={"width_ratios": [2, 1]})
for i, (cod, ch, titulo, unidad, k_esc) in enumerate(EJEMPLOS):
    t, c1, c2 = leer(cod)
    x = (c2 if ch == 2 else c1)
    y = filtrar(x, t)
    ms, x, y = t * 1e3, x * k_esc, y * k_esc

    a = ax[i, 0]
    a.plot(ms, x, color=CRUDO, lw=0.6, label="Antes")
    a.plot(ms, y, color=FILTRADO, lw=1.2, label="Después")
    a.set_title(titulo, loc="left")
    a.set_ylabel(unidad)
    a.grid(alpha=0.3, lw=0.4)
    if i == 0:
        a.set_ylim(22, None)                   # franja libre abajo para la leyenda
        a.legend(loc="lower left", ncol=2)

    # acercamiento alrededor del punto mas ruidoso
    k = abs(x - y).argmax()
    w = int(len(t) * 0.08)
    sl = slice(max(k - w, 0), min(k + w, len(t)))
    z = ax[i, 1]
    z.plot(ms[sl], x[sl], color=CRUDO, lw=0.6)
    z.plot(ms[sl], y[sl], color=FILTRADO, lw=1.4)
    z.set_title("Acercamiento", loc="left")
    z.grid(alpha=0.3, lw=0.4)

for a in ax[-1]:
    a.set_xlabel("Tiempo [ms]")
fig.align_ylabels(ax[:, 0])
fig.tight_layout(pad=0.3, h_pad=0.5, w_pad=0.5)
for ext, dpi in (("png", 300), ("pdf", None)):
    fig.savefig(FIGURAS / f"antes_despues_filtro.{ext}", dpi=dpi)
print(f"fc = {FC:.0f} Hz")
