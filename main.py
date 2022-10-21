from time import sleep
from stqdm import stqdm
import time
import streamlit as st

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
import io
import matplotlib.pyplot as plt
import base64

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



def main():
    st.title('ラクマスクレイピングアプリ')
    
    with st.form('text_form'):
        search_text = st.text_input('商品名を入力')
        button = st.form_submit_button('送信')
    
    url="https://fril.jp/s?query="+search_text+"&transaction=selling"

    items_list=[]
    res=get_html(url)
    soup=bs(res.content,"html.parser")

    max_page = int(soup.find_all(class_="col-xs-4 pager-text")[0].text.replace("\n ","").replace( " ","").replace( "ページ","").replace( " ","").split("/")[1])

    for i in stqdm(range(max_page)):
        res=get_html(url)
        soup=bs(res.content,"html.parser")
        items=soup.find_all(class_="view view_grid")
        items=items[0].findAll(class_="item")
        items_list+=[item for item in items]
        url = "https://fril.jp/s?order=desc&"+"page="+str(i+2)+"&query="+"ps5本体"+"&sort=created_at&transaction=selling"

    
    df = df_maker(items_list)

    df_describe = df.describe()
    
    st.header('価格の記述統計量')
    st.write(df_describe)

    histgram_creater(df)


if __name__ == '__main__':
    main()

