"""Compara los valores preliminares medidos con los teoricos y simulados del informe."""
import csv
from pathlib import Path

v = {r["codigo"]: {k: float(x) for k, x in r.items() if k not in ("codigo", "fuente")}
     for r in csv.DictReader(open(Path(__file__).with_name("valores_preliminares.csv")))}

# --- Tabla 1: carga resistiva --------------------------------------------
vo, i = v["1110"], v["1120"]
P = vo["RMS"] * i["RMS"]                 # carga resistiva: v e i en fase
S = i["Vs_rms"] * i["RMS"]               # media onda: i_s = i_carga
t1 = {
    "Media onda": dict(med=[vo["RMS"], vo["DC"], vo["PICO"], P, S, P / S],
                       teo=[6.02, 3.83, 12.03, 0.165, 0.247, 0.668],
                       sim=[5.88, 3.68, 11.94, 0.157, 0.240, 0.668]),
    "Tap central": dict(med=[v["2110"]["RMS"], v["2110"]["DC"], v["2110"]["PICO"], None, None, None],
                        teo=[8.51, 7.66, 12.03, 0.329, 0.493, 0.667],
                        sim=[8.53, 7.62, 11.91, 0.330, 0.498, 0.662]),
}
print("R_L estimada (1.1.x):", round(vo["RMS"] / i["RMS"], 1), round(vo["DC"] / i["DC"], 1),
      round(vo["PICO"] / i["PICO"], 1), "ohm")

# --- Tabla 2: filtro RC (fila segun el rizado medido) --------------------
def fila(c):
    return [v[c]["RMS"], v[c]["DC"], v[c]["PICO"], v[c]["FR_%"], None]

alto1, bajo1 = sorted(["1210", "1310"], key=lambda c: -v[c]["FR_%"])
alto2, bajo2 = sorted(["2210", "2310"], key=lambda c: -v[c]["FR_%"])
t2 = {
    f"Media onda bajo rizo ({bajo1})": dict(med=fila(bajo1), teo=[10.0, 9.9, 12.0, 9.9, 0.35], sim=[10.34, 10.3, 11.82, 9.29, 0.38]),
    f"Media onda alto rizo ({alto1})": dict(med=fila(alto1), teo=[6.9, 6.4, 12.0, 46.5, 0.52], sim=[7.77, 7.30, 11.90, 37.12, 0.45]),
    f"Tap central bajo rizo ({bajo2})": dict(med=fila(bajo2), teo=[11.0, 11.0, 12.0, 5.0, 0.40], sim=[11.1, 11.09, 11.83, 3.99, 0.29]),
    f"Tap central alto rizo ({alto2})": dict(med=fila(alto2), teo=[9.6, 9.2, 12.0, 33.1, 0.55], sim=[9.28, 9.07, 11.90, 23.22, 0.33]),
}


def imprimir(tabla, cols):
    for nombre, d in tabla.items():
        print(f"\n{nombre}")
        print("  " + " | ".join(f"{c:>9}" for c in ["Origen"] + cols))
        for origen in ("teo", "sim", "med"):
            print("  " + " | ".join([f"{origen:>9}"] + [f"{x:9.3f}" if x is not None else f"{'-':>9}" for x in d[origen]]))
        err = [abs(m - t) / t * 100 if m is not None else None for m, t in zip(d["med"], d["teo"])]
        print("  " + " | ".join([f"{'%err':>9}"] + [f"{e:8.1f}%" if e is not None else f"{'-':>9}" for e in err]))


imprimir(t1, ["Vo_rms", "Vo_DC", "Vo_pico", "P", "S", "PF"])
imprimir(t2, ["Vo_rms", "Vo_DC", "Vo_pico", "FR%", "PF"])
