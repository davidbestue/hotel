import pandas as pd
import numpy as np
import easygui   ## ¿¿ conda install -c conda-forge easygui  ??
import sys 


#### Entrar info
msg = "Información"
title = "Reserva"
fieldNames = ["Nombre y apellidos","número de habitaciones","tipo de habitación", "entrada", "salida", "observaciones"]
fieldValues = []  # we start with blanks for the values
fieldValues = easygui.multenterbox(msg,title, fieldNames)

# make sure that none of the fields was left blank
while 1:
    if fieldValues == None: break
    errmsg = ""
    for i in range(len(fieldNames)):
      if fieldValues[i].strip() == "":
        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
    if errmsg == "": break # no problems found
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)


#print(fieldValues)

nombre, n_hab, tipo_hab, entrada, salida, obs = fieldValues


df=pd.read_excel('Verano_2020.xlsx')

### Algoritmo para ver si hay disponible
### 1: coger en el df las filas que corresponden al tipo de habitacion y las columnas que corresponden a los días
df_tipo = df.loc[df['clase']==int(tipo_hab)] 
### 2: ver si, de entrada, hay tantas habitaciones de ese tipo disponibles
if len(df_tipo)<int(n_hab):
    print('No hay tantas habitaciones de este tipo')
    exit()


## 3: ver si hay ese número de habitaciones disponibles todos los días que se piden
idx_entrada = np.where(df.columns==entrada)[0][0]  
idx_salida = np.where(df.columns==salida)[0][0]  
df_tipo_dias = df_tipo.iloc[:, idx_entrada:idx_salida] #df de el tipo seleccionado, los días seleccionados

print('lalala')

# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
# df.to_excel(writer, sheet_name='Sheet1')

# # Get the xlsxwriter workbook and worksheet objects.
# workbook  = writer.book
# worksheet = writer.sheets['Sheet1']

# # Apply a conditional format to the cell range.
# #worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})
# format_ocupada = workbook.add_format({'bg_color':   '#FFC7CE',
#                                'font_color': '#000000'})

# worksheet.conditional_format('B2:B8', {'type':     'cell',
#                                     'criteria': 'equal to',
#                                     'value':     30,
#                                     'format':    format_ocupada})

# worksheet.conditional_format('B2:B8', {'type':     'cell',
#                                     'criteria': 'equal to',
#                                     'value':     15,
#                                     'format':    format_ocupada})

# # Close the Pandas Excel writer and output the Excel file.
# writer.save()