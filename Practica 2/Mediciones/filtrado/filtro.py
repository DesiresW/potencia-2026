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

CARPETA = Path(__file__).resolve().parent.parent   # Practica 2/Mediciones


def leer(codigo):
    """Devuelve t [s], ch1 [V], ch2 [V] del archivo XYZ0.csv."""
    d = np.loadtxt(CARPETA / f"{codigo}.csv", delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1], d[:, 2]


def filtrar(x, t):
    fs = 1.0 / np.median(np.diff(t))
    sos = butter(ORDEN, FC, btype="low", fs=fs, output="sos")
    return sosfiltfilt(sos, medfilt(x, MEDIANA))
