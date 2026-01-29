# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Example Streamlit App :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruites you want in your smoothie
  """
)

import streamlit as st
cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name of Smoothie: ")
st.write("The name of smoothie will be:", name_on_order)




my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=False)


ingredient_list = st.multiselect(
    "Choose up to five ingredients:"
    ,my_dataframe
    ,max_selections=5
)


if ingredient_list:
    ingredients_string =''
    
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen + 'Nutrition info')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

st.write(my_insert_stmt)


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()

    st.success(f"Your Smoothie {name_on_order} is ordered!", icon="✅")
