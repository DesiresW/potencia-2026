"""Rampas ordinales (claro -> oscuro) a partir de los tonos de la paleta de referencia.

Se mantiene el tono (hue) de cada color base en OKLCH y se escalona la claridad L.
Uso:  python paleta.py   -> imprime las rampas en hex
"""
import numpy as np


def _hex_a_lin(h):
    c = np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _lin_a_hex(c):
    c = np.clip(c, 0, 1)
    s = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)
    return "#" + "".join(f"{round(v * 255):02x}" for v in s)


M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
               [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
               [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])


def a_oklch(h):
    lab = M2 @ np.cbrt(M1 @ _hex_a_lin(h))
    return lab[0], np.hypot(lab[1], lab[2]), np.arctan2(lab[2], lab[1])


def de_oklch(L, C, H):
    lab = np.array([L, C * np.cos(H), C * np.sin(H)])
    lms = (np.linalg.inv(M2) @ lab) ** 3
    return _lin_a_hex(np.linalg.inv(M1) @ lms)


def rampa(base, claridades, croma=None):
    _, C, H = a_oklch(base)
    return [de_oklch(L, croma if croma else C, H) for L in claridades]


L_CARGA = (0.74, 0.58, 0.42)          # R_L, C_1, C_2  (claro -> oscuro)
AZUL = rampa("#2a78d6", L_CARGA, 0.14)    # rama superior (D1 / R_D3)
NARANJA = rampa("#eb6834", L_CARGA, 0.15)  # rama inferior (D2 / R_D4)
GRIS = [de_oklch(L, 0.0, 0.0) for L in (0.70, 0.52, 0.30)]   # rampa neutra (reserva)
# salida v_o por carga (R_L, C_1, C_2): tonos de la paleta de referencia que no chocan
# con azul/naranja (validado all-pairs: CVD 11.0, normal 16.7) y que oscurecen con C
SALIDA = ["#eda100", "#e87ba4", "#4a3aa7"]                  # amarillo, magenta, violeta

if __name__ == "__main__":
    for nombre, r in (("azul", AZUL), ("naranja", NARANJA), ("gris", GRIS)):
        print(nombre, ",".join(r))
