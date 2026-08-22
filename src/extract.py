import json
import os
import requests
import pandas as pd
from config.config import COMPANIES,RAW_DATA_DIR,SEC_USER_AGENT

def get_data_from_sec(cik):
    """to get data from sec api"""
    url= f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    headers = {'USER-AGENT':  SEC_USER_AGENT }
    response = requests.get(url,headers=headers)
    response.raise_for_status()
    return response.json()

def save_data_as_json(data, filename):
    """to save data into JSON file locally"""
    os.makedirs (RAW_DATA_DIR, exist_ok= True)
    filepath= os.path.join(RAW_DATA_DIR, filename)
    with open(filepath,'w') as f:
        json.dump(data, f)
    return filepath

def load_data(filename):
    """to load data from JSON file locally"""
    filepath= os.path.join(RAW_DATA_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)

def get_company_facts(ticker,force_refresh=False):
    """
        Main entry point: returns company facts JSON for a ticker,
        using local cache unless force_refresh=True or no cache exists.
    """

    company=COMPANIES[ticker]
    filename=f"{ticker.lower()}_companyfacts.json"
    filepath= os.path.join(RAW_DATA_DIR, filename)

    if not force_refresh and os.path.exists(filepath):
        return load_data(filename)

    data= get_data_from_sec(company['cik'])
    save_data_as_json(data, filename)
    return data




def get_raw_metrics(data, tag_name):
    try:
        metric= data['facts']['us-gaap'][tag_name]['units']['USD']
        return pd.DataFrame(metric)

    except KeyError:
        raise KeyError(f"{tag_name} not found in sec company facts")


def get_all_raw_metrics():
   raw_metrics= {}

   for ticker in COMPANIES:
       company = COMPANIES[ticker]
       data= get_company_facts(ticker)

       raw_metrics[ticker]= {}
       for tag_key in ["revenue_tag","cogs_tag","inventory_tag"]:
           tag_name = company[tag_key]
           raw_metrics[ticker][tag_key]= get_raw_metrics(data, tag_name)
   return raw_metrics
