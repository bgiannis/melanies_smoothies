# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
# Need space after first occurrence of ":cup_with_straw: " otherwise you get a syntax error

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

# For connection go SniS (Streamlit app)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients;'
    , my_dataframe
    , max_selections=5
)

# Removes array braces if no selections made (to look cleaner)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
   
    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    # insert the order into snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# adding the json function displayes the record to screen
# st.text(fruityvice_response.json())  

# putting JSON into a Dataframe
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)





