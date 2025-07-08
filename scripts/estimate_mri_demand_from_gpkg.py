import geopandas as gpd
import pandas as pd

def estimate_mri_demand_from_gpkg():
    """
    Compute total estimated MRI demand per LSOA using age-segmented population
    and national MRI demand rates by age band.

    Returns:
    - DataFrame with LSOA code and estimated MRI total
    """

    # --- File Paths (absolute) ---
    gpkg_path = "/Users/rosstaylor/Downloads/Research Project/Code Folder/diagnostic-modality-demand/diagnostic-modality-demand/data/raw/LSOA_5-year_segment_master.gpkg"
    counts_path = "/Users/rosstaylor/Downloads/Research Project/Code Folder/diagnostic-modality-demand/diagnostic-modality-demand/data/raw/modality_procedure_counts_by_age_band_2024.csv"

    # --- Step 1: Load age-based MRI counts and population ---
    modality_df = pd.read_csv(counts_path)

    # Define population for 2024 projection (same used for rate calc)
    pop_df = pd.DataFrame({
        "age_band": [
            "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
            "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74",
            "75-79", "80-84", "85+"
        ],
        "population_2024": [
            283792, 322018, 331416, 324765, 342425, 342688, 367510, 355513,
            341210, 362553, 413048, 423510, 376552, 337298, 357074,
            266939, 181501, 183436
        ]
    })

    # Merge counts with population to compute rate per 1k
    df = modality_df[["age_band", "MRI_Total"]].merge(pop_df, on="age_band")
    df["mri_demand_per_1k"] = (df["MRI_Total"] / df["population_2024"]) * 1000

    # --- Step 2: Map to LSOA columns from GPKG ---
    ageband_to_column = {
        "0-4": "age_0_4",
        "5-9": "age_5_9",
        "10-14": "age_10_14",
        "15-19": "age_15_19",
        "20-24": "age_20_24",
        "25-29": "age_25_29",
        "30-34": "age_30_34",
        "35-39": "age_35_39",
        "40-44": "age_40_44",
        "45-49": "age_45_49",
        "50-54": "age_50_54",
        "55-59": "age_55_59",
        "60-64": "age_60_64",
        "65-69": "age_65_69",
        "70-74": "age_70_74",
        "75-79": "age_75_79",
        "80-84": "age_80_84",
        "85+": "age_85_plus"
    }

    # Create dict: LSOA column → per-1k MRI rate
    mri_rate_dict = {
        ageband_to_column[ab]: rate
        for ab, rate in zip(df["age_band"], df["mri_demand_per_1k"])
    }

    # --- Step 3: Load GPKG and compute MRI demand per LSOA ---
    gdf = gpd.read_file(gpkg_path)

    for col, rate in mri_rate_dict.items():
        gdf[f"mri_{col}"] = (gdf[col] * rate) / 1000

    mri_cols = [f"mri_{col}" for col in mri_rate_dict.keys()]
    gdf["mri_total_demand"] = gdf[mri_cols].sum(axis=1)

    return gdf[["lsoa21cd", "mri_total_demand"] + mri_cols]
