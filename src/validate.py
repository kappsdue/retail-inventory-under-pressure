
def check_no_duplicate_years(df):
    return not df.duplicated(subset=['company','fiscal_year']).any()

def check_no_negative_values(df,columns):
    return (df[columns] >= 0).all().all()

def check_no_missing_values(df,columns):
    return df[columns].notna().all().all()

def check_margin_within_bounds(df,upper=.5,lower= 0):
    return df['gross_margin_pct'].between(lower,upper).any()

def run_validation(df):
    if not check_no_duplicate_years(df):
        raise ValueError("Duplicate (company, fiscal_year) rows found")

    if not check_no_negative_values(df, ['revenue', 'costofrevenue', 'inventory']):
        raise ValueError("Negative values found in revenue/costofrevenue/inventory")

    if not check_no_missing_values(df, ['revenue', 'costofrevenue', 'inventory', 'gross_margin_pct']):
        raise ValueError("Missing (NaN) values found in required columns")

    if not check_margin_within_bounds(df):
        raise ValueError("Gross margin outside plausible bounds (0-50%)")

    return True