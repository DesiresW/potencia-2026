# Electrónica de Potencia 2026 — Universidad Nacional de Colombia

Material de laboratorio: simulaciones, mediciones e informes.

## Práctica 1 — Caracterización de diodos
- `practica 1/Datos.txt`: base de datos del informe 1.
- `practica 1/SIM1N4004.asc`: simulación LTspice del 1N4004.

## Práctica 2 — Rectificadores de potencia con diodos
| Carpeta / archivo | Contenido |
|---|---|
| `LAB2_DE_POTENCIA/` | Proyecto LaTeX del informe 2 (`main.tex`, compila con `latexmk -pdf main.tex`). |
| `LAB2_DE_POTENCIA/sub_files/circuitos/` | Esquemáticos en CircuiTikZ (generalizados, bloques modulares y adaptados). |
| `Simulaciones_Lab2/` | Simulaciones LTspice definitivas (media onda, tab central y puente, con y sin filtro RC). |
| `Simulaciones/` | Versión anterior de las simulaciones. |
| `Mediciones/` | Capturas del osciloscopio en CSV (`Time(s), CH1V, CH2V`). |
| `latex_informe2/` | Borrador de prueba de las figuras de metodología. |

### Nomenclatura de las mediciones
El archivo `XYZ0.csv` corresponde a la medición **X.Y.Z** (el `0` final se ignora):

- **X**: circuito — 1 media onda (SW1, SW2), 2 onda completa con tab central (SW3–SW5), 3 puente rectificador (SW6–SW9).
- **Y**: carga — 1 resistiva ($R_L$), 2 $R_L \parallel C_1$ (selector a la izquierda), 3 $R_L \parallel C_2$ (selector a la derecha).
- **Z**: punto medido — 1 sobre $R_L$; 2 en adelante sobre cada R dummy de 1 Ω.

Estados de los switches: C cerrado, A abierto, I izquierda, D derecha. El detalle está en las tablas de mediciones del informe.
