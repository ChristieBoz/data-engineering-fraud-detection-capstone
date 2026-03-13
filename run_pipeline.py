#import the functions from the scripts
from scripts.load_raw_data import load_raw_data
from scripts.cleaning_data import cleaning_data
from scripts.feature_engineering import feature_engineering
from scripts.baseline_modeling import baseline_modeling
from scripts.curated_modeling import curated_modeling
from scripts.comparison import comparison
from scripts.data_visuals import class_distribution, amount_distribution

def run_pipeline():

    print("STEP 1: Load Raw Data")
    load_raw_data()

    print("STEP 2: Clean Data")
    cleaning_data()

    print("STEP 3: Feature Engineering")
    feature_engineering()

    print("STEP 4: Baseline Modeling")
    baseline_modeling()

    print("STEP 5: Curated Modeling")
    curated_modeling()

    print("STEP 6: Model Comparison")
    comparison()

    print("STEP 7: Data Visualizations")
    class_distribution()
    amount_distribution()

    print("PIPELINE COMPLETE!!")

if __name__ == "__main__":
    run_pipeline()