"""Capturas descartadas o dudosas: crudo vs filtrado, con la fuente de referencia."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filtro import FIGURAS, filtrar, leer

plt.rcParams.update({"font.size": 7, "axes.titlesize": 7.5, "legend.fontsize": 6.5})
AZUL, GRIS, FUENTE = "#1f4e9c", "#bbbbbb", "#e0a0a0"

CASOS = [
    ("2120", "2.1.2: tab central, $R_L$, sobre $R_{D3}$", "pico ~30 V (debería ser mV)"),
    ("2130", "2.1.3: tab central, $R_L$, sobre $R_{D4}$", "pico ~30 V e idéntica a 2.1.2"),
    ("2230", "2.2.3: tab central, $R_L \\parallel C_1$, sobre $R_{D4}$", "pico ~30 V (debería ser mV)"),
    ("2320", "2.3.2: tab central, $R_L \\parallel C_2$, sobre $R_{D3}$", "pico ~30 V (debería ser mV)"),
    ("2330", "2.3.3: tab central, $R_L \\parallel C_2$, sobre $R_{D4}$", "pico ~30 V e idéntica a 2.3.2"),
    ("1220", "1.2.2: media onda, $R_L \\parallel C_1$, sobre $R_{D1}$", "promedio 69 mA vs 47 mA esperado"),
]

fig, ax = plt.subplots(3, 2, figsize=(10, 7.5), sharex=True)
for a, (cod, titulo, motivo) in zip(ax.ravel(), CASOS):
    t, c1, c2 = leer(cod)
    ms = t * 1e3
    f2 = filtrar(c2, t)
    a.plot(ms, c2, color=GRIS, lw=0.7, label="CH2 crudo")
    a.plot(ms, f2, color=AZUL, lw=1.1, label="CH2 filtrado")
    b = a.twinx()
    b.plot(ms, filtrar(c1, t), color=FUENTE, lw=0.8, ls="--", label="$v_s$ (CH1, eje der.)")
    b.set_ylim(-20, 20)
    b.tick_params(axis="y", colors="#b06060", labelsize=6)
    a.set_title(titulo, loc="left")
    a.text(0.99, 0.97, motivo, transform=a.transAxes, ha="right", va="top", fontsize=6.5,
           color="#c0392b", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.8", lw=0.4))
    a.set_ylabel("CH2 [V]")
    a.set_xlim(-40, 40)
    a.grid(alpha=0.3, lw=0.4)
    a.set_zorder(b.get_zorder() + 1)
    a.patch.set_visible(False)
h1, l1 = ax[0, 0].get_legend_handles_labels()
fig.legend(h1 + [plt.Line2D([], [], color=FUENTE, ls="--")], l1 + ["$v_s$ (CH1, eje derecho)"],
           loc="upper center", ncol=3, frameon=False)
for a in ax[-1]:
    a.set_xlabel("Tiempo [ms]")
plt.tight_layout(rect=(0, 0, 1, 0.96))
plt.savefig(FIGURAS / "no_confiables.png", dpi=110)
