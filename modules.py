import pandas as pd
import requests
import matplotlib.pyplot as plt
from stqdm import stqdm
import streamlit as st


def get_html(url):
    res=requests.get(url)
    return res

def details(item):
    return {
        "name": item.find(class_='link_search_title').get('title'),
        "price": int(item.find('p', class_='item-box__item-price').text.replace("¥","").replace(",",""))
    } 

def df_maker(items_list):
    li = []
    
    for item in stqdm(items_list):
        try:
            li.append(details(item))
        
        except:
            del item
    
    df = pd.DataFrame(li)
    return df

def histgram_creater(df):
    x = df.price

    quantile_1 = x.quantile(0.25)
    quantile_3 = x.quantile(0.75)
    dif = quantile_3-quantile_1
    limit_up = quantile_3+1.5*(dif)
    limit_down = quantile_1-1.5*(dif)
    
    fig = plt.figure()
    ax = fig.add_subplot(xlim=(limit_down,limit_up))

    ax.hist(x,bins=30)
    
    st.header('価格の分布')
    st.pyplot(fig)