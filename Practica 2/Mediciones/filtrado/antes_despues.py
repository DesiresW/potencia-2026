"""Grafica antes/despues del filtro: dos ejemplos, cada uno con su acercamiento.

Exporta antes_despues_filtro.png y .pdf con figsize = (5, 3) in y 150 DPI.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filtro import FC, filtrar, leer

plt.rcParams.update({"font.size": 6, "axes.titlesize": 6.5, "legend.fontsize": 5.5,
                     "lines.linewidth": 0.8})

# (archivo, canal, descripcion, unidad)
EJEMPLOS = [
    ("1320", 2, r"1.3.2: media onda, $R_L \parallel C_2$, sobre $R_{D1}$", r"$v$ [V] ($=i$ [A])"),
    ("2310", 1, r"2.3.1: tab central, $R_L \parallel C_2$, sobre $R_L$", r"$v_o$ [V]"),
]

fig, ax = plt.subplots(len(EJEMPLOS), 2, figsize=(5, 3),
                       gridspec_kw={"width_ratios": [2, 1]})
for i, (cod, ch, titulo, unidad) in enumerate(EJEMPLOS):
    t, c1, c2 = leer(cod)
    x = c2 if ch == 2 else c1
    y = filtrar(x, t)
    ms = t * 1e3

    a = ax[i, 0]
    a.plot(ms, x, color="#bbbbbb", lw=0.6, label="Antes")
    a.plot(ms, y, color="#1f4e9c", label="Después")
    a.set_title(titulo, loc="left")
    a.set_ylabel(unidad)
    a.grid(alpha=0.3, lw=0.4)
    if i == 0:
        a.legend(loc="lower left", frameon=False)

    # acercamiento alrededor del punto mas ruidoso
    k = abs(x - y).argmax()
    w = int(len(t) * 0.08)
    sl = slice(max(k - w, 0), min(k + w, len(t)))
    z = ax[i, 1]
    z.plot(ms[sl], x[sl], color="#bbbbbb", lw=0.6)
    z.plot(ms[sl], y[sl], color="#1f4e9c", lw=1.0)
    z.set_title("Acercamiento", loc="left")
    z.grid(alpha=0.3, lw=0.4)

for a in ax[-1]:
    a.set_xlabel("Tiempo [ms]")
fig.align_ylabels(ax[:, 0])
plt.tight_layout(pad=0.4, h_pad=0.6, w_pad=0.6)
for ext in ("png", "pdf"):
    plt.savefig(f"antes_despues_filtro.{ext}", dpi=150)
print(f"fc = {FC:.0f} Hz")
