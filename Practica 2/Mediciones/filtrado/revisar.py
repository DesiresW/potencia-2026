"""Grafica de revision interna: crudo vs filtrado y lo que se quito."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from filtro import filtrar, leer

casos = [("1320", 2), ("1220", 2), ("2310", 1), ("1120", 2)]
fig, ax = plt.subplots(len(casos), 2, figsize=(16, 3.2 * len(casos)))
for i, (cod, ch) in enumerate(casos):
    t, c1, c2 = leer(cod)
    x = c2 if ch == 2 else c1
    y = filtrar(x, t)
    ms = t * 1e3
    ax[i, 0].plot(ms, x, color="0.7", lw=0.8, label="crudo")
    ax[i, 0].plot(ms, y, color="C0", lw=1.3, label="filtrado")
    ax[i, 0].set_title(f"{cod} CH{ch}")
    ax[i, 0].legend(loc="upper right")
    # zoom de ~1 ciclo alrededor del maximo crudo
    k = x.argmax(); w = int(len(t) * 0.12)
    sl = slice(max(k - w, 0), min(k + w, len(t)))
    ax[i, 1].plot(ms[sl], x[sl], ".-", color="0.6", ms=3, lw=0.6)
    ax[i, 1].plot(ms[sl], y[sl], color="C0", lw=1.5)
    ax[i, 1].set_title("zoom alrededor del maximo")
plt.tight_layout()
plt.savefig(sys.argv[1] if len(sys.argv) > 1 else "revision_filtro.png", dpi=65)
