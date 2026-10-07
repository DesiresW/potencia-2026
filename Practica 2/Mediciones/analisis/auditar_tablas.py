"""Auditoria: recalcula desde las CSV cada valor 'Medido' y '% Error' de las tablas IV y V
del informe (sub_files/p1.tex) y lo compara con lo que esta escrito."""
import re
import subprocess
import sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).parent
subprocess.run([sys.executable, "valores_preliminares.py"], cwd=AQUI, capture_output=True, check=True)
subprocess.run([sys.executable, "potencias.py"], cwd=AQUI, capture_output=True, check=True)
import csv
from filtro import RESULTADOS
V = {r["codigo"]: r for r in csv.DictReader(open(RESULTADOS / "valores_preliminares.csv"))}
P = {r["codigo"]: r for r in csv.DictReader(open(RESULTADOS / "potencias.csv"))}
f = lambda d, k: float(d[k])

tex = (AQUI.parents[1] / "LAB2_DE_POTENCIA/sub_files/p1.tex").read_text(encoding="utf-8")
tex = re.sub(r"(?<!\\)%[^\n]*", "", tex)                # quita comentarios (no los \%)


def filas_tabla(etiqueta):
    i = tex.index(etiqueta)
    cuerpo = tex[i:tex.index("\\end{tabular}", i)]
    filas = [r for r in cuerpo.replace("\n", " ").split("\\\\")]
    return [[c.strip() for c in r.split("&")] for r in filas]


def numeros(fila, desde):
    out = []
    for c in fila[desde:]:
        m = re.search(r"-?\d+(\.\d+)?", c)
        out.append(float(m.group()) if m else None)
    return out


def comparar(nombre, escrito, esperado, tol):
    ok = True
    for col, (e, x) in enumerate(zip(escrito, esperado)):
        if x is None:
            continue
        bien = e is not None and abs(e - x) <= tol[col]
        ok &= bien
        if not bien:
            print(f"   !! {nombre} col {col}: escrito {e}  recalculado {x:.4g}")
    print(f"{'OK ' if ok else 'MAL'} {nombre}: escrito {escrito}")
    return ok


err = lambda m, t: abs(m - t) / t * 100
todo_ok = True

# ---------------- Tabla IV ----------------
filas = filas_tabla("tab:consolidado_tabla1")
med = [r for r in filas if len(r) > 2 and r[1].startswith("Medido")]
pct = [r for r in filas if len(r) > 2 and "Error" in r[1]]
teo4 = {"media": (6.02, 3.83, 12.03, 0.165, 0.247, 0.668), "tab": (8.51, 7.66, 12.03, 0.329, 0.493, 0.667)}
for i, (cod, clave) in enumerate((("1110", "media"), ("2110", "tab"))):
    v, p = V[cod], P[cod]
    esper = [f(v, "RMS"), f(v, "DC"), f(v, "PICO"), f(p, "P_W"), f(p, "S_VA"), f(p, "PF")]
    todo_ok &= comparar(f"IV Medido {cod}", numeros(med[i], 2), esper, [0.006, 0.006, 0.006, 6e-4, 6e-4, 6e-4])
    todo_ok &= comparar(f"IV %Error {cod}", numeros(pct[i], 2), [err(m, t) for m, t in zip(esper, teo4[clave])],
                        [0.06] * 6)

# ---------------- Tabla V ----------------
filas = filas_tabla("tab:consolidado_tabla2")
med = [r for r in filas if len(r) > 3 and r[2].startswith("Medido")]
pct = [r for r in filas if len(r) > 3 and "Error" in r[2]]
teo5 = [(10.0, 9.9, 12.0, 9.9, 0.35), (6.9, 6.4, 12.0, 46.5, 0.52),
        (11.0, 11.0, 12.0, 5.0, 0.40), (9.6, 9.2, 12.0, 33.1, 0.55)]
orden = ["1310", "1210", "2310", "2210"]               # filas: MO 220uF, MO 47uF, TC 220uF, TC 33uF
for i, cod in enumerate(orden):
    v, p = V[cod], P[cod]
    esper = [f(v, "RMS"), f(v, "DC"), f(v, "PICO"), f(v, "FR_%"), f(p, "PF")]
    todo_ok &= comparar(f"V  Medido {cod}", numeros(med[i], 3), esper, [0.006, 0.006, 0.006, 0.006, 0.006])
    todo_ok &= comparar(f"V  %Error {cod}", numeros(pct[i], 3), [err(m, t) for m, t in zip(esper, teo5[i])],
                        [0.06, 0.06, 0.06, 0.06, 1.5])
print("\nRESULTADO:", "todo coincide" if todo_ok else "hay diferencias")
