import pandas as pd
import streamlit as st
import numpy as np
import datetime
from streamlit_sidebar import streamlit_sidebar
from clean_data_frame import clean_data_frame 

def render_dash():

    pmi_data_frame = pd.read_csv('PMI.csv', 
                                sep = ';', 
                                header = 4)\
                                .dropna()

    pmi_data_frame = clean_data_frame(pmi_data_frame)

    cnae_selection, filter_date_start, filter_date_end = streamlit_sidebar(pmi_data_frame)

    st.subheader('Comparativo de volume de vendas entre  CNAEs:')

    if cnae_selection == []:
        return st.warning("Selecione um CNAE.")

    st.line_chart(data = pmi_data_frame.query("Data >= @filter_date_start and Data <= @filter_date_end")[['Data']+ cnae_selection], 
                x = 'Data',  
                height = 500, 
                use_container_width = True)
    
render_dash()
