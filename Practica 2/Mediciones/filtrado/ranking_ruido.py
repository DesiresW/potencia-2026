"""Mide cuanto ruido quita el filtro en cada archivo y canal."""
import numpy as np
from filtro import CARPETA, filtrar, leer

filas = []
for f in sorted(CARPETA.glob("*.csv")):
    t, ch1, ch2 = leer(f.stem)
    fs = 1 / np.median(np.diff(t))
    for nombre, x in (("CH1", ch1), ("CH2", ch2)):
        y = filtrar(x, t)
        ruido = np.std(x - y)
        rango = np.ptp(y)
        filas.append((ruido / rango * 100, f.stem, nombre, fs, ruido, rango,
                      x.max(), y.max()))

print(f"{'ruido/rango':>11} archivo canal   fs[Hz]  ruido_rms   rango   max_crudo max_filtr")
for r in sorted(filas, reverse=True):
    print(f"{r[0]:10.2f}%  {r[1]}  {r[2]}  {r[3]:7.0f}  {r[4]:9.4f}  {r[5]:7.3f}  {r[6]:8.3f} {r[7]:8.3f}")
