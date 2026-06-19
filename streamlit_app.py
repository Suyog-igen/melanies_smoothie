import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("Customize your smoothie 🥤")
st.write("Choose your own fruits")

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    'Choose up to five:',
    my_dataframe
)

if ingredients_list:
    ingredients_string = ''
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '

    name_on_order = st.text_input('Customer Name:')
    st.write('The name for your order is:', name_on_order)

    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                        VALUES ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""

    if st.button('Submit Order'):
        if name_on_order:
            session.sql(my_insert_stmt).collect()
            st.success('Your smoothie has been ordered!')
        else:
            st.warning('Please enter your name before submitting!')
