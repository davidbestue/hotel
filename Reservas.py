import pandas as pd
import numpy as np
import easygui   ## ¿¿ conda install -c conda-forge easygui  ??
import sys 


#### Entrar info
msg = "Información"
title = "Reserva"
fieldNames = ["Nombre y apellidos","DNI", "número de habitaciones","tipo de habitación", "entrada", "salida", "observaciones"]
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

nombre, DNI, n_hab, tipo_hab, entrada, salida, obs = fieldValues


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

## en el df del tipo y días ver cuantas hay disponibles (todo 0 en la fila)
libres=[]
for hab_ in range(len(df_tipo_dias)):
    if sum(df_tipo_dias.iloc[hab_, :]==0) == len(df_tipo_dias.iloc[hab_, :]):
        libres.append(hab_) 


if len(libres)<int(n_hab):
    print('No hay tantas habitaciones LIBRES de este tipo')
    print('De este tipo hay: ' + str(len(libres)) + ' disponibles')
    exit()


#### Precio total (numero de noche y habitaciones del mismo tipo)
n_total_noches = np.shape(df_tipo_dias)[1] - 1 
n_habitaciones= int(n_hab)
if tipo_hab=='1':
    precio_noche=20
elif tipo_hab=='2':
    precio_noche=40
elif tipo_hab=='3':
    precio_noche=50

TotalAmount = n_habitaciones*precio_noche*n_total_noches

###Confirmar reserva

image = "book_.gif"
msg = '¿Confirmar la reserva de '+ n_hab + ' habitaciones, de '  + entrada + ' a ' + salida + '?'
choices = ["Sí","No"]
reply = easygui.buttonbox(msg, image=image, choices=choices)


if reply == 'Sí':
    for hab_ in range(int(n_hab)):
        df_tipo_dias.iloc[hab_, :]=1 ### marcar como 1 la hab reservada
        #### Generar archivo de registro de la reserva
        g = df_tipo_dias.index[hab_]
        detalles_habitacion_reservada = df.loc[g][['clase', 'habitaciones', 'terraza']]  
        habitación_res = str(detalles_habitacion_reservada.habitaciones) 
        #### Generar archivo de registro de la reserva
        name_ = entrada+'_'+salida+'_'+nombre+'_'+ str(habitación_res)+'.txt'
        name_ = nombre+'_'+ str(habitación_res)+'.txt'
        text_file = open(name_, "w")
        text_file.write("Habitación: %s" % habitación_res)
        text_file.write("\n")
        text_file.write("Nombre: %s" % nombre)
        text_file.write("\n")
        text_file.write("DNI: %s" % DNI)
        text_file.write("\n")
        text_file.write("entrada: %s" % entrada)
        text_file.write("\n")
        text_file.write("salida: %s" % salida)
        text_file.write("\n")
        text_file.write("clase habitación: %s" % detalles_habitacion_reservada.clase)
        text_file.write("\n")
        text_file.write("terraza habitación: %s" % detalles_habitacion_reservada.terraza)
        text_file.write("\n")
        text_file.write("Total (€): %s" % TotalAmount)
        text_file.close()
        



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