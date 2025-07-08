import os
import geopandas as gpd
import pandas as pd

def estimate_mri_elective_demand_from_gpkg():
    """
    Estimate Elective MRI demand per LSOA using national age-specific elective MRI rates
    and 2024 LSOA population estimates.
    """

    # --- File Paths ---
    base_path = "/Users/rosstaylor/Downloads/Research Project/Code Folder/diagnostic-modality-demand/diagnostic-modality-demand/data/raw"
    gpkg_path = os.path.join(base_path, "LSOA_5-year_segment_master.gpkg")
    mri_master_path = os.path.join(base_path, "mri_master.csv")
    population_path = os.path.join(base_path, "south_west_population_2024.csv")

    # --- Step 1: Load MRI data and classify sources ---
    mri_df = pd.read_csv(mri_master_path)
    elective_sources = [
        "Outpatient (this Health Care Provider)",
        "GP Direct Access",
        "Admitted Patient Care - Day case (this Health Care Provider)"
    ]

    mri_df["source_group"] = mri_df["patient_source"].apply(
        lambda x: "Elective" if x in elective_sources else "Other"
    )
    mri_df["exam_count"] = 1

    # --- Step 2: Bin into age bands ---
    age_bins = list(range(0, 90, 5)) + [200]
    age_labels = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
        "75-79", "80-84", "85+"
    ]

    mri_df["age_band"] = pd.cut(mri_df["age"], bins=age_bins, labels=age_labels, right=False)

    # --- Step 3: Aggregate elective MRI per age band ---
    elective_demand = (
        mri_df[mri_df["source_group"] == "Elective"]
        .groupby("age_band")["exam_count"]
        .sum()
        .reset_index()
        .rename(columns={"exam_count": "MRI_Elective"})
    )

    # --- Step 4: Load population and map age bands ---
    population_df = pd.read_csv(population_path)
    population_df["age_band"] = pd.cut(population_df["age"], bins=age_bins, labels=age_labels, right=False)
    age_band_pop = (
        population_df.groupby("age_band", observed=False)["population"]
        .sum()
        .reset_index()
        .rename(columns={"population": "population_2024"})
    )

    # --- Step 5: Compute elective MRI rate per 1,000 ---
    df = elective_demand.merge(age_band_pop, on="age_band", how="left")
    df["mri_elective_per_1k"] = (df["MRI_Elective"] / df["population_2024"]) * 1000

    # --- Step 6: Map to LSOA columns ---
    ageband_to_column = {
        "0-4": "age_0_4", "5-9": "age_5_9", "10-14": "age_10_14", "15-19": "age_15_19",
        "20-24": "age_20_24", "25-29": "age_25_29", "30-34": "age_30_34", "35-39": "age_35_39",
        "40-44": "age_40_44", "45-49": "age_45_49", "50-54": "age_50_54", "55-59": "age_55_59",
        "60-64": "age_60_64", "65-69": "age_65_69", "70-74": "age_70_74", "75-79": "age_75_79",
        "80-84": "age_80_84", "85+": "age_85_plus"
    }

    mri_rate_dict = {
        ageband_to_column[str(ab)]: rate
        for ab, rate in zip(df["age_band"], df["mri_elective_per_1k"])
    }

    # --- Step 7: Apply to GPKG ---
    gdf = gpd.read_file(gpkg_path)
    for col, rate in mri_rate_dict.items():
        gdf[f"mri_elective_{col}"] = (gdf[col] * rate) / 1000

    mri_cols = [f"mri_elective_{col}" for col in mri_rate_dict]
    gdf["mri_elective_total_demand"] = gdf[mri_cols].sum(axis=1)

    return gdf[["lsoa21cd", "mri_elective_total_demand"] + mri_cols]
