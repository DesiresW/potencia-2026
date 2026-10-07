# Electrónica de Potencia 2026 — Universidad Nacional de Colombia

Material de laboratorio: informes, simulaciones y mediciones.

```
.
├── Practica 1/                       Caracterización de diodos
│   ├── Datos.txt                     base de datos del informe 1
│   ├── Datos_backup_...txt           respaldo anterior a la base maestra
│   └── SIM1N4004.asc                 simulación LTspice del 1N4004
└── Practica 2/                       Rectificadores de potencia con diodos
    ├── LAB2_DE_POTENCIA/             proyecto LaTeX del informe 2 (main.tex)
    │   └── sub_files/
    │       ├── circuitos/            esquemáticos CircuiTikZ (generalizados, bloques, adaptados)
    │       ├── metodologia_circuitos.tex   protocolo experimental: figuras y tablas de mediciones
    │       └── Imagenes/             figuras del informe (las de mediciones se copian desde Mediciones/figuras)
    ├── LAB2_DE_POTENCIA_actualizado.zip   el proyecto listo para subir a Overleaf
    ├── Simulaciones_Lab2/            simulaciones LTspice definitivas (con y sin filtro RC)
    ├── Mediciones/
    │   ├── crudas/                   capturas originales del osciloscopio (no se modifican)
    │   ├── filtradas/                capturas filtradas            (generado)
    │   ├── resultados/               valores calculados en CSV     (generado)
    │   ├── figuras/                  gráficas .png y .pdf          (generado)
    │   └── analisis/                 scripts de Python
    └── montaje físico.jfif           foto original del montaje
```

## Práctica 2

### Informe
Compila con `latexmk -pdf main.tex` dentro de `LAB2_DE_POTENCIA/` (requiere `IEEEtran`, `circuitikz`, `subfig`, `booktabs`, `multirow`, `titlesec`, `enumitem`). Para Overleaf se sube `LAB2_DE_POTENCIA_actualizado.zip`.

### Nomenclatura de las mediciones
El archivo `crudas/XYZ0.csv` corresponde a la medición **X.Y.Z** (el `0` final se ignora). Columnas: `Time(s), CH1V, CH2V`.

- **X**: circuito — 1 media onda (SW1, SW2), 2 onda completa con tab central (SW3–SW5), 3 puente rectificador (SW6–SW9).
- **Y**: carga — 1 resistiva ($R_L$), 2 $R_L \parallel C_1$ (selector a la izquierda), 3 $R_L \parallel C_2$ (selector a la derecha).
- **Z**: punto medido — 1 sobre $R_L$; 2 en adelante sobre cada R dummy de 1 Ω.

Estados de los switches: C cerrado, A abierto, I izquierda, D derecha. Capacitores: media onda $C_1 = 47\,\mu$F, tab central y puente $C_1 = 33\,\mu$F; $C_2 = 220\,\mu$F en los tres.

> **Corrección (2026-10-06):** `2210.csv` y `2310.csv` se guardaron con los nombres intercambiados en el laboratorio y ya están corregidos aquí. Evidencia: el nivel DC de cada uno coincidía con el de las capturas de la otra configuración (2230 frente a 2320/2330) y el rizado no correspondía a su capacitor. Las copias originales fuera del repo (`D:\`) siguen con los nombres viejos.

### Análisis (`Mediciones/analisis/`)
Todo se regenera con un solo comando:

```
pip install -r "Practica 2/Mediciones/analisis/requirements.txt"
python "Practica 2/Mediciones/analisis/generar_todo.py"
```

Filtra las capturas, calcula los valores, rehace las gráficas, las copia al informe y verifica que las tablas IV y V coincidan con las CSV.

| Script | Qué hace |
|---|---|
| `filtro.py` | lectura, rutas y filtro digital: mediana de 5 muestras + Butterworth pasa-bajos orden 4, $f_c = 1$ kHz, ida y vuelta (sin desfase) |
| `valores_preliminares.py` | $V_{rms}$, $V_{DC}$, $V_{pico}$ y FR sobre un número entero de ciclos |
| `potencias.py` | P, S y PF con $R_L = 220\,\Omega$ e $i_D = v_o/R_L + C\,dv_o/dt$ |
| `auditar_tablas.py` | compara cada valor medido de las tablas del informe con lo recalculado |
| `estilo.py`, `paleta.py` | estilo común de las figuras (ancho de columna del informe, Arial 7–8 pt) y paleta validada |
| `antes_despues.py`, `metodo_valores.py` | figuras de metodología (filtro y marcadores) |
| `grafica_media_onda.py`, `grafica_tab_central.py` | figuras de resultados |
| `no_confiables.py`, `recarga_tab.py`, `ranking_ruido.py` | revisión de capturas (no van al informe) |

**Criterio de corriente:** la corriente se calcula a partir de $v_o$ con $R_L = 220\,\Omega$. Las capturas directas sobre las R dummy del tab central registraron el voltaje inverso del diodo (~30 V), no la caída en 1 Ω, y no se usan para calcular corriente.

**Pendiente:** mediciones del puente rectificador (3.x.x).
