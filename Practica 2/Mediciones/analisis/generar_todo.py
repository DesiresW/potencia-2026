"""Regenera todo el analisis de las mediciones, en orden, y lo sincroniza con el informe.

Uso (desde cualquier carpeta):  python "Practica 2/Mediciones/analisis/generar_todo.py"

  1. valores_preliminares.py  filtra crudas/ -> filtradas/ y calcula V_rms, V_DC, V_pico, FR
  2. potencias.py             P, S y PF con i = v_o / R_L (R_L = 220 ohm)
  3. graficas                 figuras/*.png y *.pdf al ancho de columna del informe
  4. copia al informe         las figuras que usa LAB2_DE_POTENCIA/sub_files/Imagenes/
  5. auditar_tablas.py        verifica que las tablas IV y V del informe coincidan con las CSV
"""
import shutil
import subprocess
import sys
from pathlib import Path

from filtro import FIGURAS

AQUI = Path(__file__).resolve().parent
IMAGENES = AQUI.parents[1] / "LAB2_DE_POTENCIA" / "sub_files" / "Imagenes"

PASOS = ["valores_preliminares.py", "potencias.py", "antes_despues.py", "metodo_valores.py",
         "grafica_media_onda.py", "grafica_tab_central.py", "no_confiables.py", "recarga_tab.py"]
# figura generada -> nombre que usa el informe
AL_INFORME = {"antes_despues_filtro.pdf": "filtro_antes_despues.pdf",
              "metodo_valores.pdf": "marcadores_mediciones.pdf",
              "media_onda.pdf": "resultados_media_onda.pdf",
              "tab_central.pdf": "resultados_tab_central.pdf"}

FIGURAS.mkdir(exist_ok=True)
for paso in PASOS:
    print(f"-> {paso}")
    subprocess.run([sys.executable, paso], cwd=AQUI, check=True, capture_output=True)
for origen, destino in AL_INFORME.items():
    shutil.copy2(FIGURAS / origen, IMAGENES / destino)
    print(f"-> informe: {destino}")
print("-> auditar_tablas.py")
r = subprocess.run([sys.executable, "auditar_tablas.py"], cwd=AQUI, capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1])
