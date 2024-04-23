from stqdm import stqdm
import streamlit as st
from bs4 import BeautifulSoup as bs
import modules

def main():
    st.title('rakuma_price_survey')
    
    with st.form('text_form'):
        search_text = st.text_input('商品名を入力')
        button = st.form_submit_button('送信')

    
    if button:
    
        url="https://fril.jp/s?query="+search_text+"&transaction=selling"

        items_list=[]
        res=modules.get_html(url)
        soup=bs(res.content,"html.parser")

        max_page = int(soup.find_all(class_="col-xs-4 pager-text")[0].text.replace("\n ","").replace( " ","").replace( "ページ","").replace( " ","").split("/")[1])

        for i in stqdm(range(max_page)):
            res=modules.get_html(url)
            soup=bs(res.content,"html.parser")
            items=soup.find_all(class_="view view_grid")
            items=items[0].findAll(class_="item")
            items_list+=[item for item in items]
            url = f"https://fril.jp/s?order=desc&page={str(i+2)}&query={search_text}&sort=created_at&transaction=selling"

        
        df = modules.df_maker(items_list)

        df_describe = df.describe()
        
        st.header('価格の記述統計量')
        st.write(df_describe)

        modules.histgram_creater(df)


if __name__ == '__main__':
    main()

