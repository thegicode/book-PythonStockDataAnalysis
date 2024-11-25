
import pandas as pd
import requests


url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
file_path = "./data/companies.xls"

response = requests.get(url)

with open(file_path, "wb") as f:
    f.write(response.content)

df = pd.read_html(file_path)[0]
df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by='종목코드')

print(df)