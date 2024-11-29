import re
start_date = "2024 year 8/30"
start_list = re.split(r'\D+', start_date)
start_year = int(start_list[0])
start_month = int(start_list[1])
start_day = int(start_list[2])
start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}"
print("start_date:", start_date)