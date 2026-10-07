"""Filtra todas las capturas y calcula los valores preliminares de las tablas.

- Guarda cada CSV filtrado en Mediciones/filtradas/ (los originales no se tocan).
- Promedios sobre un numero entero de periodos de la fuente (cruces por cero).
- La fuente es el canal simetrico (media ~ 0); el otro canal es la medicion.
  Asi se corrigen solas las capturas con los canales intercambiados.
"""
import csv
import numpy as np
from filtro import CARPETA, filtrar, leer

SALIDA = CARPETA / "filtradas"
SALIDA.mkdir(exist_ok=True)


def ventana_periodos(t, vs):
    """Indices entre el primer y el ultimo cruce ascendente por cero de la fuente."""
    s = np.signbit(vs)
    sube = np.where(s[:-1] & ~s[1:])[0]
    return slice(sube[0], sube[-1]) if len(sube) >= 2 else slice(None)


def analizar(codigo):
    t, c1, c2 = leer(codigo)
    f1, f2 = filtrar(c1, t), filtrar(c2, t)
    np.savetxt(SALIDA / f"{codigo}.csv", np.column_stack([t, f1, f2]), delimiter=",",
               header="Time(s),CH1V,CH2V", comments="", fmt="%.6e")
    # la fuente es la de media mas cercana a cero respecto a su rango
    if abs(f1.mean()) / np.ptp(f1) <= abs(f2.mean()) / np.ptp(f2):
        vs, x, canal_fuente = f1, f2, "CH1"
    else:
        vs, x, canal_fuente = f2, f1, "CH2"
    w = ventana_periodos(t, vs)
    vs, x = vs[w], x[w]
    dc = x.mean()
    rms = np.sqrt(np.mean(x ** 2))
    return {
        "codigo": codigo, "fuente": canal_fuente,
        "Vs_rms": np.sqrt(np.mean(vs ** 2)), "Vs_pico": vs.max(),
        "DC": dc, "RMS": rms, "PICO": x.max(), "MIN": x.min(),
        "FR_%": np.sqrt(max(rms ** 2 - dc ** 2, 0)) / dc * 100 if dc else np.nan,
        "periodos": round((t[w][-1] - t[w][0]) * 60),
    }


filas = [analizar(f.stem) for f in sorted(CARPETA.glob("*.csv"))]
claves = list(filas[0])
with open(CARPETA / "filtrado" / "valores_preliminares.csv", "w", newline="") as fh:
    wr = csv.DictWriter(fh, claves)
    wr.writeheader()
    for r in filas:
        wr.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})

print(f"{'cod':5}{'fuente':>7}{'Vs_rms':>8}{'Vs_pk':>8}{'DC':>9}{'RMS':>9}{'PICO':>9}{'MIN':>9}{'FR%':>8}{'per':>5}")
for r in filas:
    print(f"{r['codigo']:5}{r['fuente']:>7}{r['Vs_rms']:8.3f}{r['Vs_pico']:8.3f}{r['DC']:9.4f}"
          f"{r['RMS']:9.4f}{r['PICO']:9.4f}{r['MIN']:9.4f}{r['FR_%']:8.2f}{r['periodos']:5}")
