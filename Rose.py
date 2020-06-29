import pandas as pd
import numpy as np

# Crear Dataframe con los datos de las habitaciones del hotel
habitaciones=[1,2,3,4,5,6,7,8,9,10]
clase=[3,3,3,2,2,2,2,2,1,1]
terraza=[0,0,1,1,1,0,0,1,1,1]
ruidosa=[1,1,1,1,0,0,0,0,0,0] 

df_rooms=pd.DataFrame({'habitaciones':habitaciones, 
    'clase':clase, 'terraza':terraza, 'ruidosa':ruidosa})


# Crear df con los datos del mes
dias_mes=30
df_mes = pd.DataFrame(np.zeros((len(df_rooms) , dias_mes)) ) 
df_mes.columns=np.arange(1, dias_mes+1)

# Poner juntos el de habitaciones y meses
df_all=pd.concat([df_rooms, df_mes], axis=1)



# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Apply a conditional format to the cell range.
#worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
format_ocupada = workbook.add_format({'bg_color':   '#FFC7CE',
                               'font_color': '#000000'})

worksheet.conditional_format('B2:B8', {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':     30,
                                    'format':    format_ocupada})

worksheet.conditional_format('B2:B8', {'type':     'cell',
                                    'criteria': 'equal to',
                                    'value':     15,
                                    'format':    format_ocupada})

# Close the Pandas Excel writer and output the Excel file.
writer.save()