import pandas as pd
import numpy as np
import easygui   ## ¿¿ conda install -c conda-forge easygui  ??



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


print(fieldValues)



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