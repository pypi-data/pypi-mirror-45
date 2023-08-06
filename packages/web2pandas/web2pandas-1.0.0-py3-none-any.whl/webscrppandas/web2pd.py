import requests
import pandas as pd

def WebScrap2df(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)
    return df_list