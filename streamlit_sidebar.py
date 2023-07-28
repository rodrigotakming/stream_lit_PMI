import pandas as pd
import streamlit as st
import datetime

def create_cnae_multiselect(data_frame):
    return st.sidebar.multiselect('Selecione o CNAE:',
                                  data_frame.columns.to_list()[1:])

def create_start_date_input():
    return st.sidebar.date_input(
        "Selecione Data Início:",
        datetime.datetime(2002, 1, 1),
        max_value = datetime.datetime(2030, 1, 1))

def create_end_date_input():
    return st.sidebar.date_input(
        "Selecione Data Fim:",
        datetime.datetime(2030, 1, 1),
        max_value = datetime.datetime(2030, 1, 1), min_value = datetime.datetime(2002, 1, 1))

def streamlit_sidebar(data_frame: pd.DataFrame):
    cnae_selection = create_cnae_multiselect(data_frame)

    filter_date_start = create_start_date_input()

    filter_date_end = create_end_date_input()
    
    return cnae_selection, filter_date_start, filter_date_end
