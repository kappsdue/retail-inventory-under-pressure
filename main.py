from src.extract import get_all_raw_metrics
from src.transform import (get_clean_flow_metrics,get_clean_inventory,
                           merge_raw_metrics,save_processed_data,
                           merge_with_gscpi)
from src.validate import run_validation
from src.load import create_database_if_not_exists,create_table_if_not_exists,load_data

raw_metrics=get_all_raw_metrics()
clean_revenue=get_clean_flow_metrics(raw_metrics,'revenue_tag','revenue')
clean_cogs=get_clean_flow_metrics(raw_metrics,'cogs_tag','costofrevenue')
clean_inventory=get_clean_inventory(raw_metrics)


merged=merge_raw_metrics(clean_revenue,clean_cogs,clean_inventory)


result=run_validation(merged)
print(result)

save_processed_data(merged)

show=merge_with_gscpi(merged)
print(show)

save_processed_data(show,'financials_merged_w_gscpi.csv')

create_database_if_not_exists()
create_table_if_not_exists()
load_data(show)

#20-aug-2026 final build