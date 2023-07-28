import pandas as pd
import numpy as np

def set_null_values(data_frame):
    return data_frame.replace('-', np.nan)

def replace_comma_to_dot(float_number_with_comma):
    return float_number_with_comma.str.replace(',','.')

def replace_comma_to_dot_in_columns(data_frame, columns):
    for column in columns:
        is_not_null_mask = ~data_frame[column].isnull()
        data_frame.loc[is_not_null_mask, [column]] = \
            data_frame.loc[is_not_null_mask, [column]].apply(lambda float_number_with_comma: replace_comma_to_dot(float_number_with_comma))
        
def clean_data_frame(data_frame):

    numeric_columns = data_frame.columns.to_list()[1:]

    data_frame = data_frame.rename(columns = {'Mês':'Mês Ano'})

    data_frame= set_null_values(data_frame)

    replace_comma_to_dot_in_columns(data_frame, numeric_columns)

    data_frame[numeric_columns] = data_frame[numeric_columns].astype(np.float16)

    data_frame['Ano'] = data_frame['Mês Ano'].apply(lambda mes_ano: mes_ano.split()[1])

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

    data_frame['Mês'] = data_frame['Mês Ano'].apply(lambda data: data.split()[0]).replace(meses_dict)

    data_frame['Data'] = pd.to_datetime(data_frame['Ano'] + '-' + data_frame['Mês'], format = '%Y-%m')

    data_frame = data_frame.drop(['Mês', 'Mês Ano', 'Ano'], axis = 1)

    return data_frame