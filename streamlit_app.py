import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests  

st.title("Customize your smoothie 🥤")
st.write("Choose your own fruits")

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to five:',
    pd_df['FRUIT_NAME'].tolist()
)

if ingredients_list:
    ingredients_string = ''
    
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '
        
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_chosen, ' is ', search_on, '.')
        
        st.subheader(fruits_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = smoothiefroot_response.json()
        st.dataframe(data=sf_df, use_container_width=True)

    name_on_order = st.text_input('Customer Name:').strip()
    st.write('The name for your order is:', name_on_order)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                        VALUES ('""" + ingredients_string.strip() + """', '""" + name_on_order.strip() + """')"""

    if st.button('Submit Order'):
        if name_on_order:
            session.sql(my_insert_stmt).collect()
            st.success('Your smoothie has been ordered!')
        else:
            st.warning('Please enter your name before submitting!')
