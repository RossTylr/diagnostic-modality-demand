import os
import geopandas as gpd
import pandas as pd

def estimate_ct_emergency_demand_from_gpkg():
    """
    Estimate Emergency CT demand per LSOA using national age-specific emergency CT rates
    and 2024 LSOA population estimates.

    Returns:
        GeoDataFrame with LSOA code and total Emergency CT demand per 1,000 population.
    """

    # --- File Paths ---
    base_path = "/Users/rosstaylor/Downloads/Research Project/Code Folder/diagnostic-modality-demand/diagnostic-modality-demand/data/raw"
    gpkg_path = os.path.join(base_path, "LSOA_5-year_segment_master.gpkg")
    ct_master_path = os.path.join(base_path, "ct_master.csv")
    population_path = os.path.join(base_path, "south_west_population_2024.csv")

    # --- Step 1: Load CT data and classify emergency sources ---
    ct_master_df = pd.read_csv(ct_master_path)
    emergency_sources = [
        "Accident and Emergency Department (this Health Care Provider)",
        "Admitted Patient Care - Inpatient (this Health Care Provider)"
    ]

    ct_master_df["source_group"] = ct_master_df["patient_source"].apply(
        lambda x: "Emergency" if x in emergency_sources else "Other"
    )
    ct_master_df["exam_count"] = 1  # default count

    # --- Step 2: Bin into age bands ---
    age_bins = list(range(0, 90, 5)) + [200]
    age_labels = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
        "75-79", "80-84", "85+"
    ]

    ct_master_df["age_band"] = pd.cut(
        ct_master_df["age"], bins=age_bins, labels=age_labels,
        right=False, include_lowest=True
    )

    # --- Step 3: Aggregate emergency demand by age band ---
    emergency_demand = (
        ct_master_df[ct_master_df["source_group"] == "Emergency"]
        .groupby("age_band")["exam_count"]
        .sum()
        .reset_index()
        .rename(columns={"exam_count": "CT_Emergency"})
    )

    # --- Step 4: Load national population and bin by age band ---
    population_df = pd.read_csv(population_path)
    population_df["age_band"] = pd.cut(
        population_df["age"], bins=age_bins, labels=age_labels,
        right=False, include_lowest=True
    )
    age_band_pop = (
        population_df.groupby("age_band", observed=False)["population"]
        .sum()
        .reset_index()
        .rename(columns={"population": "population_2024"})
    )

    # --- Step 5: Compute emergency CT rate per 1,000 ---
    df = emergency_demand.merge(age_band_pop, on="age_band", how="left")
    df["ct_emergency_per_1k"] = (df["CT_Emergency"] / df["population_2024"]) * 1000

    # --- Step 6: Map age bands to LSOA GPKG columns ---
    ageband_to_column = {
        "0-4": "age_0_4", "5-9": "age_5_9", "10-14": "age_10_14", "15-19": "age_15_19",
        "20-24": "age_20_24", "25-29": "age_25_29", "30-34": "age_30_34", "35-39": "age_35_39",
        "40-44": "age_40_44", "45-49": "age_45_49", "50-54": "age_50_54", "55-59": "age_55_59",
        "60-64": "age_60_64", "65-69": "age_65_69", "70-74": "age_70_74", "75-79": "age_75_79",
        "80-84": "age_80_84", "85+": "age_85_plus"
    }

    ct_rate_dict = {
        ageband_to_column[str(ab)]: rate
        for ab, rate in zip(df["age_band"], df["ct_emergency_per_1k"])
    }

    # --- Step 7: Load LSOA GPKG and compute demand per LSOA ---
    gdf = gpd.read_file(gpkg_path)
    for col, rate in ct_rate_dict.items():
        gdf[f"ct_emergency_{col}"] = (gdf[col] * rate) / 1000

    ct_cols = [f"ct_emergency_{col}" for col in ct_rate_dict]
    gdf["ct_emergency_total_demand"] = gdf[ct_cols].sum(axis=1)

    return gdf[["lsoa21cd", "ct_emergency_total_demand"] + ct_cols]
