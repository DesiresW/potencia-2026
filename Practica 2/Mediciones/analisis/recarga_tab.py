"""Prueba: en las capturas 2.x.2 / 2.x.3, CH2 - CH1 recupera v_o mientras el diodo esta bloqueado."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from filtro import FIGURAS, filtrar, leer

REF = {"2120": "2110", "2130": "2110", "2230": "2210", "2320": "2310", "2330": "2310"}
fig, ax = plt.subplots(len(REF), 1, figsize=(8, 9), sharex=True)
for a, (cod, ref) in zip(ax, REF.items()):
    t, c1, c2 = leer(cod)
    vs, ch2 = filtrar(c1, t), filtrar(c2, t)
    bloq = ch2 > 2                                  # diodo bloqueado (CH2 lejos de -V_D)
    d = np.where(bloq, ch2 - vs, np.nan)
    tr, r1, r2 = leer(ref)
    f1, f2 = filtrar(r1, tr), filtrar(r2, tr)
    vo = f1 if abs(f1.mean()) > abs(f2.mean()) else f2
    ms = t * 1e3
    a.plot(ms, ch2, color="#bbbbbb", lw=0.7, label="CH2")
    a.plot(ms, d, color="#1f4e9c", lw=1.1, label="CH2 - $v_s$ (diodo bloqueado)")
    a.axhline(np.mean(vo), color="#27ae60", ls="--", lw=0.8, label=f"$V_{{DC}}$ de {ref} = {np.mean(vo):.2f} V")
    a.set_title(f"{cod}: CH2 - v_s promedio = {np.nanmean(d):.2f} V, pico CH2 = {ch2.max():.1f} V", loc="left", fontsize=8)
    a.legend(fontsize=6, loc="upper right")
    a.set_xlim(-40, 40)
    a.grid(alpha=0.3)
    print(cod, "mean(CH2-vs) bloqueado =", round(np.nanmean(d), 2), "| VDC ref", ref, "=", round(np.mean(vo), 2),
          "| ripple d:", round(np.nanmin(d), 2), round(np.nanmax(d), 2))
ax[-1].set_xlabel("Tiempo [ms]")
plt.tight_layout()
plt.savefig(FIGURAS / "recarga_tab.png", dpi=100)
