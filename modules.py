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

    quantile_1 = x.quantile(0.05)
    quantile_3 = x.quantile(0.95)
    
    fig = plt.figure()
    ax = fig.add_subplot(xlim=(quantile_1,quantile_3))

    ax.hist(x,bins=30)
    
    st.header('価格の分布')
    st.pyplot(fig)