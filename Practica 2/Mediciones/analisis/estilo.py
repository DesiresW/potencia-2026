"""Estilo comun de las graficas de resultados, pensado para el PDF del informe.

Medidas tomadas del informe (IEEEtran, twocolumn):
  \\columnwidth = 272.69 pt = 3.77 in,  \\textwidth = 557.39 pt = 7.71 in
Las figuras se exportan al ancho exacto de la columna para incluirlas sin escalar
(\\includegraphics sin width), asi el texto queda a 7-8 pt reales, como los pies de figura.
Fuente: Arial, equivalente a la Helvetica (Nimbus Sans) del texto del informe.
El titulo va en el \\caption de LaTeX, no dentro de la figura.
"""
import matplotlib.pyplot as plt
from filtro import FIGURAS

ANCHO_COL = 272.69475 / 72.27      # in
ANCHO_PAG = 557.38951 / 72.27      # in
CICLO_MS = 1000 / 60
COLOR = {"R": "#1f4e9c", "C1": "#c0392b", "C2": "#1e8449"}
FUENTE = dict(color="#8c8c8c", lw=0.9, ls=(0, (4, 2)), alpha=0.9)
ESTILO_V = dict(lw=1.5)                         # voltajes: linea continua gruesa
ESTILO_I = dict(lw=1.2, ls=(0, (3, 1.5)))       # corrientes: discontinua bien visible


def aplicar():
    plt.rcParams.update({
        "font.family": "Arial",
        "mathtext.fontset": "custom", "mathtext.rm": "Arial",
        "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
        "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "legend.framealpha": 1, "legend.edgecolor": "0.8", "legend.handlelength": 2.4,
        "legend.borderpad": 0.3, "legend.labelspacing": 0.25, "legend.columnspacing": 0.9,
        "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    })


def cerrar(fig, ax, titulo, nombre, ciclos=2):
    ax.axhline(0, color="black", lw=0.4)
    ax.set_xlim(0, ciclos * CICLO_MS)
    ax.set_xlabel("Tiempo [ms]")
    if titulo:
        ax.set_title(titulo, loc="left")
    ax.grid(alpha=0.3, lw=0.4)
    fig.tight_layout(pad=0.3)
    for ext, dpi in (("png", 300), ("pdf", None)):
        fig.savefig(FIGURAS / f"{nombre}.{ext}", dpi=dpi)
    plt.close(fig)
