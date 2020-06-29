import pandas as pd
import numpy as np

# Crear Dataframe con los datos de las habitaciones del hotel
habitaciones=[1,2,3,4,5,6,7,8,9,10]
clase=[3,3,3,2,2,2,2,2,1,1]
terraza=[0,0,1,1,1,0,0,1,1,1]
ruidosa=[1,1,1,1,0,0,0,0,0,0] 

df_rooms=pd.DataFrame({'habitaciones':habitaciones, 
    'clase':clase, 'terraza':terraza, 'ruidosa':ruidosa})


# Crear df con los datos de la temporada (empieza 1 de junio y acaba 31 de agosto (p.ej))
dias_mes=[30,31,31] #dias los meses de junio, julio y agosto
meses_temporada=['6', '7', '8'] #número del mes: junio, julio y agosto

meses=[]
for idx_mes, mes in enumerate(meses_temporada):
    df_mes = pd.DataFrame(np.zeros((len(df_rooms) , dias_mes[idx_mes])) ) 
    df_mes.columns= [str(np.arange(1, dias_mes[idx_mes]+1)[i]) + '/' + meses_temporada[idx_mes] for i in range(dias_mes[idx_mes])]
    meses.append(df_mes)


df_temporada=pd.concat(meses, axis=1)
# Poner juntos el de habitaciones y meses
df=pd.concat([df_rooms, df_temporada], axis=1)


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Verano_2020.xlsx', engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
