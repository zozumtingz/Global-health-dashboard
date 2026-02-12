import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import logging

# Configuration & Logging Setup 
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class HealthDataAnalyzer:
    """
    A professional class for analyzing global health indicators.
    Features: Automated data cleaning, multi-metric analysis, and professional reporting.
    """
    
    def __init__(self):
        self.smoke_df = None
        self.health_df = None
        self.merged_data = None
        # ISO-3 Standard Mapping for accurate integration
        self.country_map = {
            "USA": "USA", "UK": "GBR", "Thailand": "THA", 
            "Japan": "JPN", "Germany": "DEU", "Australia": "AUS", 
            "India": "IND", "Brazil": "BRA"
        }

    def load_datasets(self, tobacco_file, health_file):
        """High-integrity data ingestion with error management."""
        try:
            # Ingest Tobacco Prevalence (Expected format: Excel/CSV)
            if tobacco_file.endswith('.xlsx'):
                self.smoke_df = pd.read_excel(tobacco_file)
            else:
                self.smoke_df = pd.read_csv(tobacco_file, on_bad_lines='skip')
                
            self.smoke_df.columns = self.smoke_df.columns.str.strip()
            
            # Ingest Health Data (Expected format: CSV)
            self.health_df = pd.read_csv(health_file, on_bad_lines='skip', skip_blank_lines=True)
            self.health_df.columns = self.health_df.columns.str.strip()
            
            logging.info("Datasets successfully synchronized.")
            return True
        except Exception as e:
            logging.error(f"Failed to ingest source files: {e}")
            return False

    def preprocess_data(self):
        """Data cleaning and multi-source integration."""
        try:
            # Extract Global Smoking Average
            self.smoke_df['FactValueNumeric'] = pd.to_numeric(self.smoke_df['FactValueNumeric'], errors='coerce')
            smoking_avg = self.smoke_df.groupby("SpatialDimValueCode")["FactValueNumeric"].mean().reset_index()
            smoking_avg.columns = ["CountryCode", "SmokingRate"]

            # Standardize Country Codes in Health Dataset
            self.health_df["CountryCode"] = self.health_df["Country"].map(self.country_map)
            
            # Perform Inner Join on ISO Country Codes
            self.merged_data = pd.merge(smoking_avg, self.health_df, on="CountryCode", how="inner")
            
            logging.info(f"Preprocessing completed. {len(self.merged_data)} observations validated.")
        except Exception as e:
            logging.error(f"Preprocessing Failure: {e}")

    def generate_visualization(self, target_metric):
        """Renders a high-resolution scatter plot with regression analysis."""
        if self.merged_data is None or target_metric not in self.merged_data.columns:
            logging.warning(f"Target metric '{target_metric}' not found in data.")
            return

        # Professional visual configuration
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = self.merged_data["SmokingRate"]
        y = self.merged_data[target_metric]
        
        # Core Visualization
        scatter = ax.scatter(x, y, s=160, c=y, cmap='coolwarm', alpha=0.9, edgecolors='white', linewidth=1.5)
        
        # Labeling Data Points
        for i, country in enumerate(self.merged_data["Country"]):
            ax.annotate(country, (x.iloc[i], y.iloc[i]), xytext=(7, 7), textcoords='offset points', fontsize=9)

        # Statistical Trend Analysis
        correlation = x.corr(y)
        m, b = np.polyfit(x, y, 1)
        ax.plot(x, m*x + b, color='#c0392b', linestyle='--', linewidth=2, label=f"Correlation (r={correlation:.2f})")

        # Layout Refinement
        ax.set_title(f"Impact Analysis: Smoking vs {target_metric.replace('_', ' ')}", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("Smoking Prevalence (%)", fontsize=11)
        ax.set_ylabel(target_metric.replace('_', ' '), fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True)
        
        # Output result
        save_path = f"Report_Smoking_vs_{target_metric}.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logging.info(f"Analysis report generated: {save_path}")
        plt.show()

# Execution Block 
if __name__ == "__main__":
    analyzer = HealthDataAnalyzer()
    
    # Define file paths
    files = [f for f in os.listdir() if not f.startswith('~$')]
    tobacco_file = next((f for f in files if "tobacco" in f.lower()), None)
    health_file = "health_data.csv"

    if analyzer.load_datasets(tobacco_file, health_file):
        analyzer.preprocess_data()
        
        # Identify available metrics for statistical comparison
        # (Exclude non-numeric and index columns)
        exclude_cols = ['Country', 'CountryCode', 'Smoking_Rate']
        available_metrics = [c for c in analyzer.health_df.columns if c not in exclude_cols]

        print("\n--- ANALYTICS DASHBOARD: SELECT TARGET METRIC ---")
        for i, metric in enumerate(available_metrics, 1):
            print(f"[{i}] {metric.replace('_', ' ')}")

        try:
            # User input handling with professional validation
            user_input = input(f"\nEnter metric index (1-{len(available_metrics)}) [Default: 1]: ").strip()
            selected_idx = int(user_input) - 1 if user_input else 0
            
            if 0 <= selected_idx < len(available_metrics):
                analyzer.generate_visualization(available_metrics[selected_idx])
            else:
                raise IndexError
        except (ValueError, IndexError):
            logging.warning("Input unrecognized. Reverting to default metric.")
            analyzer.generate_visualization(available_metrics[0])
