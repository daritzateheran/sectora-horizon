## Descripción General
Cada actualización del ranking empresarial del país no es solo una lista: es una oportunidad para entender cómo se mueve nuestra economía. **Sectora Horyzon** es una plataforma analítica diseñada para ayudarnos en esa tarea, utilizando fuentes de datos abiertos empresariales y transformandolos en información predictiva útil para el análisis económico y la toma de decisiones.

A partir de los rankings anuales de las principales empresas del país, la solución permite anticipar tendencias sectoriales, identificar sesgos y comprender cómo factores como la región o el tamaño empresarial influyen en el desempeño futuro.

El proyecto aborda un problema recurrente: las soluciones disponibles ofrecen una visión detallada del pasado, pero no estiman con claridad lo que puede ocurrir en los próximos años. Nuestra solución responde a esta necesidad mediante un modelo que integra información histórica, clasificación económica y variables territoriales para generar proyecciones anuales por sector económico.

La plataforma cuenta con una arquitectura automatizada y escalable, conectada end-to-end con fuentes de datos abiertos, lo que permite actualizar la información con un solo proceso y mantener vigentes las predicciones sin reprocesos manuales. Sobre esta base se construye un dashboard interactivo que facilita consultar el comportamiento empresarial, analizar tendencias y explorar escenarios futuros.

**Sectora Horyzon** convierte la información pública en un recurso estratégico, promoviendo transparencia, mejorando la supervisión y fortaleciendo la capacidad de análisis de instituciones, empresas y ciudadanía. Su aporte principal es ofrecer una visión integral del comportamiento empresarial colombiano, combinando datos históricos con estimaciones que ayudan a comprender la dinámica económica del país y a anticipar oportunidades y riesgos.


## Challenge General Notes

- Mejorar la **estimación del crecimiento**  de empresas del país por **sector económico**.
- Trabajos anteriores muestran el *“qué pasó”*, pero no el *“qué pasará”* (p. ej., crecimiento sectorial y su dispersión entre empresas)
- Mejorar la comprensión de las dinámicas económicas empresariales en Colombia.


### Objetivo General

- **Modelo predictivo** que estime **ganancias** proyectadas de las empresas integrado en un dashboard con analitica predictiva y descriptiva (Por sector, región, tamaño empresarial).


### Objetivos especificos


- [x] OE1. Limpiar, procesar y analizar el set de datos de las 10.000 empresas más grandes del país. 
- [ ] OE2. Explorar técnicas de machine learning para generar un modelo predictivo de ganancias o crecimiento. &rarr; **En progreso**
- [ ] OE3. Validar el modelo con métricas de desempeño. &rarr; **En progreso**
- [ ] OE4. Desarrollar un dashboard interactivo que permita:
    - [ ] Consultar resultados y predicciones por sector, ubicación o tamaño empresarial.
    - [ ] Responder preguntas estratégicas de decisión (por ejemplo: 
        - “¿qué sectores tienen mayor potencial de rentabilidad?”, 
        - “¿cómo se proyectan las ganancias según el patrimonio?”).
- [ ] OE5. Generar una herramienta de apoyo para la toma de decisiones basadas en datos.



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
