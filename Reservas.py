import pandas as pd
import numpy as np
import easygui   ## ¿¿ conda install -c conda-forge easygui  ??
import string
import os


###
filename='Verano_2020.xlsx'

#### Entrar info
msg = "Información"
title = "Reserva"
fieldNames = ["Nombre y apellidos","DNI", "Número de habitaciones", 
"Tipo de habitación", "Entrada", "Salida", "Terraza", "Ruido", "Observaciones"]
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
nombre, DNI, n_hab, tipo_hab, entrada, salida, obs_t, obs_r, observ = fieldValues

df=pd.read_excel(filename)

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
df_tipo_dias = df.loc[df['clase']==int(tipo_hab)].iloc[:, idx_entrada:idx_salida]

## en el df del tipo y días ver cuantas hay disponibles (todo 0 en la fila)
libres=[]
for hab_ in range(len(df_tipo_dias)):
    if sum(df_tipo_dias.iloc[hab_, :]==0) == len(df_tipo_dias.iloc[hab_, :]):
        libres.append(df_tipo_dias.index[hab_]) ## guardas los indexs de las hab libres 


if len(libres)<int(n_hab):
    print('No hay tantas habitaciones LIBRES de este tipo')
    print('De este tipo hay: ' + str(len(libres)) + ' disponibles')
    exit()



#### Observaciones

#### Observación terraza (solamente)
if obs_t == '1':
    ##añades la condición de tarraza
    df_t = df.loc[ (df['clase']==int(tipo_hab)) & (df['terraza']==1)].iloc[:, idx_entrada:idx_salida]
    libres_t=[]
    for hab_ in range(len(df_t)):
        if sum(df_t.iloc[hab_, :]==0) == len(df_t.iloc[hab_, :]):
            libres_t.append(df_t.index[hab_]) 
    ##
    if len(libres_t)<int(n_hab):
        print('Con terrza hay: ' + str(len(libres_t)) + ' disponibles')
        #print('No hay tantas habitaciones con terraza, ¿desea reservar sin terraza?')
        image = "terraza_.gif"
        msg = 'No hay tantas habitaciones con terraza, ¿desea completar la reservar con habitaciones sin terraza?'
        choices = ["Sí","No"]
        reply_t = easygui.buttonbox(msg, image=image, choices=choices)
        if reply_t == 'No':
            exit()
        elif reply_t=='Sí': #si dice que si, completar que ya tengan terraza, con sin terraza
            diferencias_ = np.setdiff1d(libres, libres_t) 
            for n_completar in range(0, int(n_hab)-len(libres_t)):
                libres_t.append(diferencias_[n_completar]) ## completas la lista con terraza con algunas sin terraza
                #
            libres=libres_t
    else:
        df_tipo_dias = df_t
        libres=libres_t
        
#####

#### Observación de ruido (solamente)
if obs_r == '1':
    ##añades la condición de tarraza
    df_r = df.loc[ (df['clase']==int(tipo_hab)) & (df['tranquila']==1)].iloc[:, idx_entrada:idx_salida]
    libres_r=[]
    for hab_ in range(len(df_r)):
        if sum(df_r.iloc[hab_, :]==0) == len(df_r.iloc[hab_, :]):
            libres_r.append(df_r.index[hab_]) 
    ##
    if len(libres_r)<int(n_hab):
        print('Tranquilas hay: ' + str(len(libres_r)) + ' disponibles')
        #print('No hay tantas habitaciones con terraza, ¿desea reservar sin terraza?')
        image = "ruido_.gif"
        msg = 'No hay tantas habitaciones tranquilas, ¿desea completar la reservar con habitaciones no tan tranquilas?'
        choices = ["Sí","No"]
        reply_r = easygui.buttonbox(msg, image=image, choices=choices)
        if reply_r == 'No':
            exit()
        elif reply_r=='Sí': #si dice que si, completar que ya tengan terraza, con sin terraza
            diferencias_ = np.setdiff1d(libres, libres_r) 
            for n_completar in range(0, int(n_hab)-len(libres_r)):
                libres_r.append(diferencias_[n_completar]) ## completas la lista con terraza con algunas sin terraza
                #
            libres=libres_r
    else:
        df_tipo_dias = df_r
        libres=libres_r
        
#####







#### Precio total (numero de noche y habitaciones del mismo tipo)
n_total_noches = np.shape(df_tipo_dias)[1] - 1 
n_habitaciones= int(n_hab)
if tipo_hab=='1':
    precio_noche=50
elif tipo_hab=='2':
    precio_noche=40
elif tipo_hab=='3':
    precio_noche=20

TotalAmount = n_habitaciones*precio_noche*n_total_noches
Total_IVA = TotalAmount + TotalAmount*0.1

###Confirmar reserva
image = "book_.gif"
msg = '¿Confirmar la reserva de '+ n_hab + ' habitaciones, de '  + entrada + ' a ' + salida + '?'
choices = ["Sí","No"]
reply = easygui.buttonbox(msg, image=image, choices=choices)

### Grabar un .txt con los datos
rows_=[]  

if reply == 'Sí':
    for hab_ in range(int(n_hab)):
        #df_tipo_dias.iloc[hab_, :]=1 ### marcar como 1 la hab reservada
        #### Generar archivo de registro de la reserva
        #row = df_tipo_dias.index[hab_]
        row = libres[hab_]
        rows_.append(row)
        #df.iloc[row, idx_entrada:idx_salida] =1
        df.loc[row].iloc[idx_entrada:idx_salida] =1
        ##
        detalles_habitacion_reservada = df.loc[row][['clase', 'habitaciones', 'terraza']]  
        habitación_res = str(detalles_habitacion_reservada.habitaciones) 
        print('Reservada la habitación '+ habitación_res    )
        #### Generar archivo de registro de la reserva
        #name_ = entrada+'_'+salida+'_'+nombre+'_'+ str(habitación_res)+'.txt'
        name_ = nombre+'_'+ str(habitación_res)+'.txt'
        reservas_path = os.path.join(os.getcwd() , 'reservas', name_)
        text_file = open(reservas_path, "w")
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
        text_file.write("Observaciones: %s" % observ)
        text_file.write("\n")
        text_file.write("Total (€): %s" % TotalAmount)
        text_file.write("\n")
        text_file.write("Total + IVA (€): %s" % Total_IVA )
        text_file.close()
        



### Poner en rojo las reservas
### Acutalizar con ROJO de reserva el excel
writer = pd.ExcelWriter(filename, engine='xlsxwriter')

df.to_excel(writer, sheet_name='Sheet1') #sobreescribirás el ya generado
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

format_reserva = workbook.add_format({'bg_color':   '#FFC7CE',
                                'font_color': '#000000'})

## F2 es la primera celda (up left) de reservas y CS11 la ultima (bottom right)
worksheet.conditional_format('F2:CS11', {'type':     'cell',
                                'criteria': 'equal to',
                                'value':     1,
                                'format':    format_reserva})


writer.save()


# ### columnas de el excel
# alph = list(string.ascii_uppercase) 
# alphA= [alph[0]+ alph[i] for i in range(len(alph))] 
# alphB= [alph[1]+ alph[i] for i in range(len(alph))] 
# alphC= [alph[2]+ alph[i] for i in range(len(alph))] 
# alphD= [alph[3]+ alph[i] for i in range(len(alph))] 
# #
# excel_columns=alph+alphA+alphB+alphC+alphD   
# excel_columns=excel_columns[1:] ##empieza por la B

# for r in range(len(rows_)):
#     ### filas de las reservas --> pasar a formato de Excel
#     row_xls = str(rows_[r]+2) ##las filas, hay que sumar 2 para que coincida
#     ### columnas
#     entrada_xls = excel_columns[idx_entrada]  
#     salida_xls = excel_columns[idx_salida-1]  ##hay que restar 1
#     ###
#     indexes_excel = entrada_xls + row_xls +':' + salida_xls+row_xls 
#     ###
#     worksheet.conditional_format('F2:CS11', {'type':     'cell',
#                                     'criteria': 'equal to',
#                                     'value':     1,
#                                     'format':    format_reserva})



# writer.save()



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