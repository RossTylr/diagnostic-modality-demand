# Geospatial Analysis to Optimise NHS Diagnostic Capacity

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14-green)

This repository contains code for the study **“Geospatial Analysis to Optimise Diagnostic Capacity Across the NHS South West Region.”** It uses population health data and geospatial methods to model accessibility and demand for **CT**, **MRI**, and **Endoscopy** services, informing strategic expansion of **Community Diagnostic Centres (CDCs)**.

## Table of Contents
1. [Introduction](#introduction)
2. [Methodology](#methodology)
3. [Key Results](#key-results)
4. [Relevance and Impact](#relevance-and-impact)
5. [Technical Stack](#technical-stack)

---

## Introduction

In line with the **NHS Long Term Plan** and the **Richards Review (2020)**, CDCs are being rolled out to expand diagnostic capacity and separate elective from acute patient flows. This project addresses a central planning question: **where to place new facilities to maximise equitable access**.

Using a competition-aware geospatial framework, it quantifies current accessibility, identifies underserved populations, and simulates the impact of targeted capacity uplift across the NHS South West region.

---

## Methodology

It follows a three-stage pipeline: (1) build the geospatial and demographic foundation, (2) model modality-specific demand, and (3) run spatial access models and scenario tests.

### Data Sources
- **Geospatial spine:** ONS 2021 Census for 3451 LSOAs in NHS SW.
- **Diagnostic activity:** NHS Diagnostic Imaging Dataset (DIDS) 2024 (3 989 188 anonymised tests across 142 providers aggregated in demand/1000 5 year age-band).
- **Health infrastructure:** Site locations and capabilities from SHAPE Place Atlas and NHS asset registers.

### Demand & Access Modelling
1. **Age-based demand (CT/MRI):** For each LSOA, expected demand is calculated by applying 5-year age-band usage rates (derived from DIDS) to local population structure.
2. **CT & MRI accessibility (E3SFCA):** We compute an accessibility score \(F_i\) per LSOA using the Enhanced 3-Step Floating Catchment Area method:
   - 60-minute car catchments,
   - capacity competition,
   - stepwise travel-time decay weighting nearer facilities more highly.
3. **Endoscopy accessibility:** Access measured as **competition-adjusted rooms per 100 000 population (aged 50–74)**, aligning with screening cohorts. LSOAs are classified as:
   - `Adequate` (≥ 4.0),
   - `Marginal` (3.5–< 4.0),
   - `Low` (< 3.5),
   - `No Access` (0).
4. **Scenario testing:** Candidate new sites are placed in clusters with **bottom tertile access + above median demand**. We re-run models with capacity uplifts of **+5%**, **+10%**, and **+20%** to quantify improvement.

---

## Key Results

- **CT:** A **+10%** capacity uplift produced a strong system-wide response, improving access for **90.2%** of LSOAs. The **median** accessibility score increased by **+6.34%**.
- **MRI:** A larger **+20%** uplift was needed for a systemic response; **61.8%** of LSOAs improved, with a **median** gain of **+10.11%**.
- **Endoscopy:** Modest, targeted investments yielded significant gains. Adding **7 rooms** (≈ **+7.8%**) increased `Adequate` LSOAs from **1,386 → 1,767** and **halved** `No Access` (**32 → 16**).

---

## Relevance and Impact

This framework supports NHS planners to:
- **Operationalise policy:** Link capacity planning to population need and spatial equity as set out by the Richards Review.
- **Tailor strategy by modality:** Protect CT at acute sites for emergency resilience; prioritise broader community rollout for MRI and Endoscopy.
- **Run “what-if” analyses:** Test proposed CDC sites so investment reduces access deserts and benefits the most underserved communities.

---

## Technical Stack

Developed in **Python 3.11** with:
- `pandas` — data manipulation
- `geopandas` — spatial processing
- `scikit-learn` — KMeans clustering
- `matplotlib` — visualisation
- `pyproj` — CRS transformations
