"""Filtro digital para las capturas del osciloscopio (red de 60 Hz).

1. Mediana de 5 muestras: quita los picos sueltos (spikes) sin redondear los flancos.
2. Butterworth pasa-bajos de orden 4, fc = 1 kHz, aplicado ida y vuelta
   (sosfiltfilt) para no desfasar la senal.

Con fc = 1 kHz pasan los armonicos de 60/120 Hz hasta el orden ~16, que son
los que dan la forma de la onda rectificada y de los pulsos de carga del condensador.
"""
from pathlib import Path
import numpy as np
from scipy.signal import butter, medfilt, sosfiltfilt

FC = 1000.0      # frecuencia de corte [Hz]
ORDEN = 4
MEDIANA = 5      # muestras

# ---- Rutas (Practica 2/Mediciones/...) ----------------------------------------
MEDICIONES = Path(__file__).resolve().parent.parent
CRUDAS = MEDICIONES / "crudas"          # CSV originales del osciloscopio (no se modifican)
FILTRADAS = MEDICIONES / "filtradas"    # CSV filtradas (generadas)
RESULTADOS = MEDICIONES / "resultados"  # tablas de valores calculados (generadas)
FIGURAS = MEDICIONES / "figuras"        # graficas .png / .pdf (generadas)
CARPETA = CRUDAS                        # alias usado por scripts anteriores


def leer(codigo):
    """Devuelve t [s], ch1 [V], ch2 [V] del archivo crudas/XYZ0.csv."""
    d = np.loadtxt(CRUDAS / f"{codigo}.csv", delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1], d[:, 2]


def filtrar(x, t):
    fs = 1.0 / np.median(np.diff(t))
    sos = butter(ORDEN, FC, btype="low", fs=fs, output="sos")
    return sosfiltfilt(sos, medfilt(x, MEDIANA))


def sincronizada(codigo, ciclos=2, desfase_180=False, f_red=60.0):
    """Captura filtrada con t = 0 en el primer cruce por cero ascendente de la fuente.

    La fuente es el canal simetrico (media ~ 0); el otro es la medicion, asi que las
    capturas con los canales intercambiados se corrigen solas. Con desfase_180 se
    sincroniza con el cruce descendente: la medicion queda corrida medio periodo.
    Devuelve t [ms], v_s y la medicion, recortados a `ciclos` periodos.
    """
    t, c1, c2 = leer(codigo)
    f1, f2 = filtrar(c1, t), filtrar(c2, t)
    if abs(f1.mean()) / np.ptp(f1) < abs(f2.mean()) / np.ptp(f2):
        vs, x = f1, f2
    else:
        vs, x = f2, f1
    s = np.signbit(vs)
    cruces = np.where((~s[:-1] & s[1:]) if desfase_180 else (s[:-1] & ~s[1:]))[0]
    tt = t - t[cruces[0]]
    w = (tt >= 0) & (tt <= ciclos / f_red)
    return tt[w] * 1e3, vs[w], x[w]
