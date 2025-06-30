# Diagnostic Modality Demand – NHS Geospatial Analysis

This repository develops a spatial analysis pipeline to estimate and forecast diagnostic imaging demand (CT, MRI, Endoscopy) across the NHS South West region. It integrates population and deprivation data, diagnostic procedure rates, hospital site locations, travel times, and projected growth scenarios to support regional planning and Community Diagnostic Centre (CDC) optimisation.

---

## 1. Project Objectives

1.1 Map NHS diagnostic infrastructure including acute hospitals, community sites, and CDCs  
1.2 Link Output Areas (OAs) to LSOAs, MSOAs, and Local Authorities using official ONS geographies  
1.3 Apply age-specific diagnostic modality demand to LSOAs using national rates  
1.4 Integrate LSOA-to-LSOA travel time matrices for car and public transport  
1.5 Build synthetic demand scenarios by geography, age, and year (2026, 2031, 2036)  
1.6 Develop an interactive Streamlit app for stakeholder use

---

## 2. Repository Structure and Notebooks

This project is structured as a series of modular Jupyter notebooks and scripts. Key components are:

### Notebooks

1. `01_file_audit_and_overview.ipynb`  
   Review and validate the contents, formats, and completeness of all input data files

2. `02_map_lsoa_msoa_la_lookup.ipynb`  
   Build a hierarchical mapping from OA to LSOA, MSOA, and Local Authority codes

3. `03_map_hospital_and_cdc_sites.ipynb`  
   Visualise the location of CDCs, acute hospitals, and community diagnostic centres

4. `04_lsoa_to_lsoa_travel_times.ipynb`  
   Load and process pairwise travel time matrices by car and public transport between LSOAs

5. `05_layer_ct_mri_endoscopy_demand.ipynb`  
   Apply age-band specific diagnostic procedure rates to LSOAs using population projections

6. `06_synthetic_demand_model_by_age_location.ipynb`  
   Generate synthetic demand using PDFs or sampling techniques at the LSOA level

7. `07_scenario_forecasting_and_growth.ipynb`  
   Incorporate projected population growth and scenario-based demand stress testing

8. `08_final_model_inputs_export.ipynb`  
   Export LSOA-level demand, travel, and site datasets for modelling and Streamlit use

### Streamlit Application

9. `streamlit_app/app.py`  
   Web-based interface for exploring demand, accessibility, and CDC placement options

10. `streamlit_app/utils.py`  
    Functions for filtering, map rendering, and dynamic controls

11. `streamlit_app/config.yaml`  
    ICB-level configuration, default colours, toggles, and region options

---

## 3. Environment Setup

To install the required environment using Conda:

```bash
conda env create -f environment.yml
conda activate diag-demand
