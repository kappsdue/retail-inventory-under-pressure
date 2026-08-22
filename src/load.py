import mysql.connector as connection
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import pandas as pd

def create_database_if_not_exists():

    conn=connection.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor= conn.cursor()
    cursor.execute (f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()

def get_connection():
    return connection.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

def create_table_if_not_exists():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  company_financials(
    company VARCHAR(20),
    fiscal_year INT,
    fiscal_year_end Date,
    revenue BIGINT,
    costofrevenue BIGINT,
    inventory BIGINT,
    gross_profit BIGINT,
    gross_margin_pct DECIMAL(6,4),
    GSCPI DECIMAL(8,7),
    UNIQUE KEY unique_company_year(company,fiscal_year)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def load_data(final_df):

    conn=get_connection()
    cursor=conn.cursor()
    final_df=final_df.copy()
    final_df['end'] = pd.to_datetime(final_df['end']).dt.date

    rows= list(final_df[[
        'company','fiscal_year','end','revenue','costofrevenue','inventory','gross_profit','gross_margin_pct','GSCPI'
    ]].itertuples(index=False, name=None))

    insert_query= """
        INSERT INTO company_financials
            (company, fiscal_year, fiscal_year_end, revenue, costofrevenue,inventory,gross_profit,gross_margin_pct,GSCPI)
            VALUES ( %s,%s,%s,%s, %s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE 
                fiscal_year_end = VALUES (fiscal_year_end),
                revenue = VALUES (revenue),
                costofrevenue = VALUES (costofrevenue),
                inventory = VALUES (inventory),
                gross_profit= VALUES (gross_profit),
                gross_margin_pct= VALUES (gross_margin_pct),
                GSCPI = VALUES (GSCPI)
"""
    cursor.executemany(insert_query, rows)
    conn.commit()

    print(f'{cursor.rowcount} rows are affected')
    cursor.close()
    conn.close()










