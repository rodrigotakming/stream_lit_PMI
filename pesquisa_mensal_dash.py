import pandas as pd
import streamlit as st
import numpy as np
import datetime

def set_null_values(data_frame):
    return data_frame.replace('-', np.nan)

def replace_comma_with_dot(string):
    return string.str.replace(',','.')

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

def streamlit_sidebar(data_frame):
    option = create_cnae_multiselect(data_frame)

    filter_date_start = create_start_date_input()

    filter_date_end = create_end_date_input()
    
    return option, filter_date_start, filter_date_end

def render_dash():

    pmi_data_frame = pd.read_csv('PMI.csv', 
                                            sep = ';', 
                                            header = 4)\
                                            .dropna()
                                
    numeric_columns = pmi_data_frame.columns.to_list()[1:]

    pmi_data_frame= set_null_values(pmi_data_frame)

    for column in numeric_columns:

        is_not_null_mask = ~pmi_data_frame[column].isnull()
        
        pmi_data_frame.loc[is_not_null_mask, [column]] = \
            pmi_data_frame.loc[is_not_null_mask, [column]].apply(lambda string: replace_comma_with_dot(string))
        
    pmi_data_frame[numeric_columns] = pmi_data_frame[numeric_columns].astype(np.float16)

    pmi_data_frame['Ano'] = pmi_data_frame['Mês'].apply(lambda data: data.split()[1])

    meses_dict = {
        'janeiro': '01',
        'fevereiro': '02',
        'março': '03',
        'abril': '04',
        'maio': '05',
        'junho': '06',
        'julho': '07',
        'agosto': '08',
        'setembro': '09',
        'outubro': '10',
        'novembro':'11',
        'dezembro': '12'
    }

    pmi_data_frame['Mês'] = pmi_data_frame['Mês'].apply(lambda data: data.split()[0]).replace(meses_dict)
    pmi_data_frame['Data'] = pd.to_datetime(pmi_data_frame['Ano'] + '-' + pmi_data_frame['Mês'], format = '%Y-%m')

    pmi_data_frame = pmi_data_frame.drop(['Mês', 'Ano'], axis = 1)

    option, filter_date_start, filter_date_end = streamlit_sidebar(pmi_data_frame)

    st.subheader('Comparativo de volume de vendas entre  CNAEs:')

    if option == []:
        return st.warning("Selecione um CNAE.")

    st.line_chart(data = pmi_data_frame.query("Data >= @filter_date_start and Data <= @filter_date_end")[['Data']+ option], 
                x = 'Data',  
                height = 500, 
                use_container_width = True)
    
render_dash()
