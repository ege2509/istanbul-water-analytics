import pandas as pd
import numpy as np
from collections import Counter

def validate_dataset(file_name):
    """
    Comprehensive data quality check for CSV/Excel files
    """
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT: {file_name}")
    print(f"{'='*60}\n")
    

    df = pd.read_excel(file_name)
    
    print(f"   Basic Info:")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {len(df.columns)}")
    
    
    print(f" Missing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    has_missing = False
    for col in df.columns:
        if missing[col] > 0:
            has_missing = True
            print(f"   {col}: {missing[col]} ({missing_pct[col]}%)")
    
    if not has_missing:
        print("No missing values found!")
    print()
    
    
    print(f"Duplicate Rows:")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Found {duplicates} duplicate rows ({duplicates/len(df)*100:.2f}%)")

        dup_rows = df[df.duplicated(keep=False)].head(3)
        print(f"   Example duplicates:\n{dup_rows}\n")
    else:
        print("No duplicates found!\n")
    
    print(f"Data Types:")
    for col in df.columns:
        dtype = df[col].dtype
        unique_count = df[col].nunique()
        print(f"   {col}: {dtype} ({unique_count} unique values)")
    print()
    
    print(f"Data Type Issues:")
    issues_found = False
    for col in df.columns:
        if df[col].dtype == 'object':
            sample_types = df[col].dropna().apply(type).value_counts()
            if len(sample_types) > 1:
                issues_found = True
                print(f"   {col}: Mixed types detected - {sample_types.items}")
    
    if not issues_found:
        print("No data type inconsistencies!\n")
    else:
        print()
    

    print(f"Whitespace Issues:")
    whitespace_issues = False
    for col in df.columns:
        if df[col].dtype == 'object':
            with_whitespace = df[col].dropna().astype(str).str.strip() != df[col].dropna().astype(str)
            if with_whitespace.any():
                whitespace_issues = True
                count = with_whitespace.sum()
                print(f"   {col}: {count} values with leading/trailing spaces")
    
    if not whitespace_issues:
        print("No whitespace issues!\n")
    else:
        print()
    
    
    print(f"\n Common Placeholder Values:")
    placeholders = ['N/A', 'NA', 'n/a', 'NULL', 'null', 'None', 'none', '', '-', '?']
    found_placeholders = False
    for col in df.columns:
        if df[col].dtype == 'object':
            for placeholder in placeholders:
                count = (df[col].astype(str) == placeholder).sum()
                if count > 0:
                    found_placeholders = True
                    print(f"   {col}: '{placeholder}' appears {count} times")
    
    if not found_placeholders:
        print("No common placeholders found!\n")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    total_cells = len(df) * len(df.columns)
    null_cells = df.isnull().sum().sum()
    completeness = ((total_cells - null_cells) / total_cells * 100)
    print(f"Data Completeness: {completeness:.2f}%")
    print(f"Total Missing Cells: {null_cells} out of {total_cells}")
    print(f"Duplicate Rows: {duplicates}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("Data Validation")
    print("="*60)
    
    validate_dataset('istanbul-dams-daily-occupancy-rates.xlsx')
    validate_dataset('istanbul-barajlarnda-ya-ve-gunluk-tuketim-verileri.xlsx')
    validate_dataset('istanbula-verilen-temiz-su-miktarlar-tr-en.xlsx')

    validate_dataset('consumption_cleaned.xlsx')
    validate_dataset('occupancy_cleaned.xlsx')
    