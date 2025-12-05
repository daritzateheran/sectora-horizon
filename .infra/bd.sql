CREATE TABLE public."Company" (
    company_id      uuid PRIMARY KEY,
    nit             varchar(20) UNIQUE NOT NULL,
    raz_n_social    text
);

CREATE TABLE public."Ciiu" (
    ciiu_code       char(4) PRIMARY KEY,
    "div/grp"       text,
    division_desc   text,
    macrosector_calc text
);

CREATE TABLE public."Location" (
    dept_code       char(2) PRIMARY KEY,
    dept_name       text,
    region_raw      text,
    region_natural  text
);

CREATE TABLE public."ReportYear" (
    company_id        uuid NOT NULL,
    year              text NOT NULL,
    ciiu_code         char(4),
    macrosector_calc  text,
    dept_code         char(2),
    ingresos          double precision,
    ganancias         double precision,
    activos           double precision,
    pasivos           double precision,
    patrimonio        double precision,
    supervisor        text,

    CONSTRAINT reportyear_company_fk
        FOREIGN KEY (company_id)
        REFERENCES public."Company"(company_id)
        ON DELETE CASCADE,

    CONSTRAINT reportyear_ciiu_fk
        FOREIGN KEY (ciiu_code)
        REFERENCES public."Ciiu"(ciiu_code),

    CONSTRAINT reportyear_location_fk
        FOREIGN KEY (dept_code)
        REFERENCES public."Location"(dept_code)
);

CREATE TABLE public."MacroEconomy" (
    year               integer PRIMARY KEY,
    gdp_nominal        double precision,
    gdp_nominal_pct    double precision,
    gdp_real           double precision,
    gdp_real_pct       double precision,
    gdp_nominal_growth double precision,
    gdp_real_growth    double precision,
    cpi                double precision,
    population         double precision
);

CREATE TABLE public."ReportYearPrediction" (
    prediction_id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id              uuid NOT NULL,
    year                    text NOT NULL,          -- 2021–2025
    ciiu_code               char(4),
    macrosector_calc        text,
    dept_code               char(2),

    -- reales (2021–2024)
    ingresos                double precision,       -- usado para proyectar 2025
    ganancias               double precision,       -- real (2021–2024) y proyectada en 2025

    -- predicción
    prediccion_margen       double precision,       -- NULL para 2021–2024
    ganancia_proyectada     double precision,       -- NULL 2021–2024, valor para 2025
    fuente                  text NOT NULL,          -- REAL / PREDICCION

    CONSTRAINT ryp_company_fk
        FOREIGN KEY (company_id)
        REFERENCES public."Company"(company_id)
        ON DELETE CASCADE,

    CONSTRAINT ryp_ciiu_fk
        FOREIGN KEY (ciiu_code)
        REFERENCES public."Ciiu"(ciiu_code),

    CONSTRAINT ryp_location_fk
        FOREIGN KEY (dept_code)
        REFERENCES public."Location"(dept_code)
);

