# Dominio del problema

Se intenta responder tres preguntas **(Qué pasó?)**:

- ¿Qué empresa es?
- ¿Qué actividad económica realiza y dónde opera? (Historico)
- ¿Cómo se comporta financieramente en el tiempo/sector/región?

Y debe permitir construir **(Qué pasará?)**:

- Proyecciones de ganancia
- Análisis por sector
- Comparaciones interanuales
- Relación con macroeconomía

Utilizando tres **capas conceptuales**
1. Identidad empresarial (estática, no anual)
2. Reportes anuales por empresa (dinámicos)
3. Contexto sectorial/macroeconómico (externo)

## Entidades base
### 1. Company

Representa una empresa única en la base principal ```empresas_10k```. Para ello se asegura NIT y razón social limpias, relación 1:1.

| Campo       | Tipo         | Descripción               |
|-------------|--------------|---------------------------|
| company_id  | UUID (PK)    | Identificador             |
| nit         | TEXT         | Identificador             |
| name        | TEXT         | Razón social normalizada  |

---
#### **Reglas ETL**

- Cada ```nit``` único en ```empresas_10k``` produce exactamente una fila en **Company**.
- Por cada```raz_n_social``` normalizada de ```empresas_10k```, debe existir solo un registro por combinación ```(nit, raz_n_social)```. 
- Si un ```nit``` tiene multiples ```raz_n_social```, se elige el ultimo reportado cronológicamente por ```a_o_de_corte```.
- No se incluyen supervisor, región, CIIU ni nada variable ya que se encontro que estos datos pueden cambiar por cada año y deben estar en otra tabla.
- Esta tabla es inmutable por año.
---
### 2. CIIU 

Catálogo estatico limpio con código CIIU, sector y su descripción, derivados de la base ```ciuu_4ac```.

| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| ciiu_code            | TEXT (PK)   | Código único (ej: 1031)   |
| division / grupo / clase | TEXT      | Jerarquías                |
| description          | TEXT         | Descripción oficial       |
| macrosector | TEXT         | Macrosector derivado |

#### **Reglas ETL**

- Cada ```ciiu_code``` único en ```ciuu_4ac``` produce exactamente una fila en CIIU.
- ```macrosector``` se infiere usando heuristicas por los sectores encontrados en ```ciuu_4ac```.
- Evita confiar en el macrosector reportado por Supersociedades.
---
### 3. Location

Catálogo estatico por departamento, con regiones en dos versiones (reportada y natural) usando la base ```divipola```.

| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| dept_code            | TEXT (PK)    | Código DANE               |
| dept_name            | TEXT         | Nombre oficial            |
| region_raw           | TEXT         | Región que venía en el dataset, corregida por departamento |
| region_natural       | TEXT         | Región natural            |

#### **Reglas ETL**

- Cada ```dept_code``` único en ```divipola``` produce exactamente una fila en Location
- No se usa municipio ni ciudad; solo departamento, se espera usar el pk para cruzar con geomapas.
- Las dos regiones se definen por heurísticas basadas en el nombre del departamento.
---
### 4. ReportYear (Entidad anual central)

Representa el “reporte anual” de una empresa extraido de ```empresas_10k```, con toda la información financiera y categórica que puede cambiar por año:
- Información financiera, CIIU, ubicación y sector de ese año.
- Se basa principalmente en ```empresas_10k``` y se cruza con CIIU y Location.
- PK → **(company_id, year)**

| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| company_id                  | FK → Company | Empresa                   |
| year                 | INT          | Año del corte             |
| ciiu_code            | FK → CIIU    | Actividad económica reportada en ese año |
| macrosector          | TEXT         | Macrosector inferido por ciiu |
| dept_code            | FK → Location | Departamento reportado en ese año |
| ingresos             | FLOAT       | ingresos_operacionales    |
| ganancia             | FLOAT       | ganancia_p_rdida         |
| activos              | FLOAT       | total_activos            |
| pasivos              | FLOAT       | total_pasivos            |
| patrimonio           | FLOAT       | total_patrimonio         |
| supervisor           | TEXT         | Por año (sí puede variar)|

#### **Reglas ETL**

- Cada ```departamento_domicilio``` en ```empresas_10k``` debe existir en ```dpto``` de ```divipola```.
- Se cruza ```empresas_10k``` con ```divipola```, en los campos ```dpto``` vs ```departamento_domicilio``` para obtener ```dept_code```.
- Cada ```ciiu``` en ```empresas_10k``` debe existir en ```clase``` de ```ciiu_4k```;
- Se cruza ```empresas_10k``` con ```ciuu_4ac```, en los campos ```ciiu``` vs ```clase``` para obtener ```ciiu_code```.
- Validar que el ```ciiu``` en ```empresas_10k``` pertenezca al mismo macrosector que en ```ciuu_4ac```. ***--opcional***
- Campos financieros se estandarizan

Aquí se resuelve el problema:
- CIIU que cambian
- Departamento que cambia
- Supervisor que cambia

---
### 5. FinancialDerived (Índices derivados por año)

Separa lo calculado de lo reportado. Esto mejora trazabilidad y se convierte en el estándar para ML pipelines / Analítica avanzada
- PK → **(company_id, year)**

| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| company_id           | FK → Company | Empresa                   |
| year                 | INT          | Año del corte             |
| margen_operacional    | FLOAT       | ganancia / ingresos       |
| leverage             | FLOAT       | pasivos / activos         |
| solvencia            | FLOAT       | patrimonio / activos      |
| crecimiento_ingresos | FLOAT       | ingreso_t − ingreso_(t−1) |
| crecimiento_ganancia  | FLOAT       | ?                         |
| expansion_activos     | FLOAT       | ?                         |

#### **Reglas ETL**

- Se genera después de poblar ReportYear. Usa ventanas por ```nit``` y ```year```.
- Puede hacerse directamente usando los adaptadores de pg, leyendo desde ReportYear.

---
### 6. MacroEconomicYear ***--opcional pero recomendado***

Indicadores macroeconómicos generales: PIB, inflación, población, COLCAP, etc. Se utiliza la base ```banco_republica```, la cual contiene series de tiempo de diferentes variables macroeconómicas.

| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| year                 | INT PK      | Año                       |
| pib_nominal          | FLOAT       | PIB nominal               |
| pib_real             | FLOAT       | PIB real                  |
| inflacion            | FLOAT       | Inflación                 |
| poblacion            | FLOAT       | Población                 |
| other_vars           | JSONB      | por si agregas más       |

---
### 7. FinancialSectorYear ***--opcional pero recomendado***

Contexto sectorial anual: Variables económicas por macrosector. Se utilizan diferentes fuentes, incluyendo ```banco_republica```, ```pib_municipios```...

- PK → **(macrosector, year)**


| Campo                | Tipo         | Descripción               |
|----------------------|--------------|---------------------------|
| year                 | INT PK      | Año                       |
| macrosector          | TEXT        | Macrosector               |
| pib_sector           | FLOAT       | PIB del sector            |
| ipp                  | FLOAT       | Indice de productor       |

### Consideraciones adicionales
El EDA sobre ```empresas_10k``` mostró que  la información financiera esta sesgada hacia empresas grandes, se hace necesario tratar de diferenciarlas:
- Grande, Mediana, Pequeña. -> es esto invariante en el tiempo? podria ir en financial derived?
- Privada vs Pública -> se puede inferir de supervisor? es esto invariante en el tiempo?