import pandas as pd
import os
from config.config import PROCESSED_DATA_DIR

def clean_snapshot_metric(df):
    df['end'] = pd.to_datetime(df['end'])
    snap = (
        df[df['form'] == '10-K']
        .sort_values('filed')
        .drop_duplicates(subset=['end'], keep='first')
    )

    clean = (
        snap[snap['end'] >= '2019-01-01']
        .rename(columns={'val': 'inventory'})[['end', 'inventory']]
    )

    inventory = clean[clean['end'] <= '2025-02-01']
    return inventory



def get_clean_inventory(raw_metrics):
    clean = {}
    for ticker in raw_metrics:
        inventory_df = raw_metrics[ticker]['inventory_tag']
        clean[ticker] = clean_snapshot_metric(inventory_df)
    return clean



def clean_flow_metric(df):
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    df['duration'] = df['end'] - df['start']

    full_year = (
        df
        [df['duration'] > pd.Timedelta(days=360)]
                 .sort_values('filed')
                 )
    no_duplicates = full_year.drop_duplicates(subset=['start', 'end'], keep='first')

    clean = no_duplicates[(no_duplicates['end'] >= '2019-01-01') & (no_duplicates['end'] <= '2025-12-31')]
    return clean[['end', 'val']]



def get_clean_flow_metrics(raw_metrics, tag_key, new_col_name):
    clean = {}
    for ticker in raw_metrics:
        df = raw_metrics[ticker][tag_key]
        cleaned = clean_flow_metric(df).rename(columns={'val': new_col_name})
        clean[ticker] = cleaned
    return clean

def merge_raw_metrics(clean_rev,clean_cogs,clean_inv):


    merged ={}
    for ticker_name in clean_rev:
        do_merge=clean_rev[ticker_name].merge(clean_cogs[ticker_name], on='end').merge(clean_inv[ticker_name], on='end')
        do_merge['gross_profit']=do_merge['revenue']-do_merge['costofrevenue']
        do_merge['gross_margin_pct']=do_merge['gross_profit']/do_merge['revenue']
        do_merge['company'] = ticker_name
        do_merge['fiscal_year']= do_merge['end'].dt.year
        merged[ticker_name]=do_merge

    final_df= pd.concat(merged.values(), ignore_index=True).sort_values(['company', 'end']).reset_index(drop=True)

    return final_df

def save_processed_data(df,filename='merged_financial.csv'):
    """
    saves processed data to csv
    """
    os.makedirs(PROCESSED_DATA_DIR,exist_ok=True)
    filepath=os.path.join(PROCESSED_DATA_DIR,filename)
    df.to_csv(filepath, index=False)
    return filepath

def merge_with_gscpi(company_df):
    gscpi_df = pd.read_csv(
        os.path.join(PROCESSED_DATA_DIR,'gscpi_yearly.csv')
                )

    gscpi_df=gscpi_df[['Year','GSCPI']]

    do_merg=(pd.merge
             (company_df,gscpi_df,left_on='fiscal_year',
    right_on='Year', how= 'left')
             )
    do_merg.drop(columns='Year',inplace=True)

    return do_merg