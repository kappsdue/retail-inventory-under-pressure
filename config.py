# --- Companies ---
COMPANIES = {
    "TGT": {
        "name": "Target",
        "cik": "0000027419",
        "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
        "cogs_tag": "CostOfGoodsAndServicesSold",
        "inventory_tag": "InventoryNet",
    },
    "WMT": {
        "name": "Walmart",
        "cik": "0000104169",
        "revenue_tag": "RevenueFromContractWithCustomerExcludingAssessedTax",
        "cogs_tag": "CostOfRevenue",
        "inventory_tag": "InventoryNet",
    },
}


# --- Paths ---
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

# --- SEC API ---
SEC_USER_AGENT = "Kaustubh kaustubhbhai27@gmail.com>"

# --- Database ---
# NOTE: If you're cloning this repo, update DB_USER/DB_PASSWORD below with your own local MySQL credentials.
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "supply_chain_case_study"