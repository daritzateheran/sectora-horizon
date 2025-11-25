
## Challenge General Notes

- Mejorar la **estimación del crecimiento**  de empresas del país por **sector económico**.
- Trabajos anteriores muestran el *“qué pasó”*, pero no el *“qué pasará”* (p. ej., crecimiento sectorial y su dispersión entre empresas)
- Mejorar la comprensión de las dinámicas económicas empresariales en Colombia.


### Objetivo General

- **Modelo predictivo** que estime **ganancias** proyectadas de las empresas integrado en un dashboard con analitica predictiva y descriptiva (Por sector, región, tamaño empresarial).


### Objetivos especificos


- [  ] OE1. Limpiar, procesar y analizar el set de datos de las 10.000 empresas más grandes del país. &rarr; **En progreso**
- [ ] OE2. Explorar técnicas de machine learning para generar un modelo predictivo de ganancias o crecimiento.
- [ ] OE3. Validar el modelo con métricas de desempeño.
- [ ] OE4. Desarrollar un dashboard interactivo que permita:
    - [ ] Consultar resultados y predicciones por sector, ubicación o tamaño empresarial.
    - [ ] Responder preguntas estratégicas de decisión (por ejemplo: 
        - “¿qué sectores tienen mayor potencial de rentabilidad?”, 
        - “¿cómo se proyectan las ganancias según el patrimonio?”).
- [ ] OE5. Generar una herramienta de apoyo para la toma de decisiones basadas en datos.

## Definición

### Dominio del problema

Se intenta responder tres preguntas (Qué pasó?):

- ¿Qué empresa es?
- ¿Qué actividad económica realiza y dónde opera?
- ¿Cómo se comporta financieramente en el tiempo/sector/región?

Y debe permitir construir (Qué pasará?):

- Proyecciones de ganancia
- Análisis por sector
- Comparaciones interanuales
- Relación con macroeconomía

---
### Posibles Features:

- Empresas_10k:
    - ingresos
    - ganancia
    - margen
    - crecimiento interanual
    - leverage
    - solvencia
    - tamaño relativo en su sector
    - dispersión sectorial (media / std del sector por año)
- CIIU:
    - agrupación sectorial fina
    - efectos sectoriales en rendimiento
- DIVIPOLA:
    - análisis regional
    - clusters territoriales (opcional)
- macroeconomía:
    - PIB real/nominal
    - inflación
    - crecimiento económico nacional
    - señales macro (útil para forecast 1–2 años)

### Plan de experimentos 
