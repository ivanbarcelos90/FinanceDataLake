from airflow.models import Variable

# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
INTERVAL=Variable.get('interval')

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
PERIOD=Variable.get('period')

# buckets variables names
BRONZE_ZONE=Variable.get('bronze_zone')
SILVER_ZONE=Variable.get('silver_zone')
GOLD_ZONE=Variable.get('gold_zone')

PERFORMANCE_FOLDER = Variable.get("performance_folder")

