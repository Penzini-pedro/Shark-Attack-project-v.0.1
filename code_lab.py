import pandas as pd
import numpy as np
import re
import datetime

df_sucio = pd.read_csv(r'C:\Users\penzi\projectos\Shark-Attack-project-v.0.1\DATASET-CSV\attacks.csv', sep= ',', encoding='latin1')

df_limpiando= df_sucio.copy()#creo una dataframe sin los rows nulos para poder limpiar y despues unirlo con los row que no necesito 

df_limpiando= df_limpiando.dropna(axis=0, how='all')#drop fillas nulas que despue svamos a join
df_limpiando= df_limpiando.drop(df_limpiando.index[6302: -1]) #mas facil era agarrar el range i drop que buscar los indice aunque lo pudiera hacer asi


#aca ya empiezas a limpiar la data 
df_limpiando.rename(columns={'Species ': 'Species'}, inplace=True)#renombrar columnas
df_limpiando['Species']= df_limpiando['Species'].fillna('shark')#change null in colum for shark
#asi vemos que contiene la columna para editar para Species /ODIO REGEX VIVA HARDCODING
df_limpiando.replace(['shark involvement prior to death was not confirmed', 'Said to involve a grey nurse shark that leapt out of the water and  seized the boy but Species identification is questionable', 'Shark involvement prior to death unconfirmed'], ['Shark involvement not confirmed', 'Shark involvement not confirmed', 'Shark involvement not confirmed'], inplace=True)
#ME DIO FASTIDIO VAMOS A APRENDER REGEX
#Limpiar columna case number
df_limpiando.rename(columns={'Case Number': 'Case_Number'}, inplace=True)
df_limpiando.rename(columns={'Case Number.1': 'Case_Number_1'}, inplace=True)
df_limpiando.rename(columns={'Case Number.2': 'Case_Number_2'}, inplace=True) #cambio columna name para hacer la limpieza mas rapid solo quita la fecha

df_limpiando.Case_Number=df_limpiando.Case_Number_1




#Limpiamos date
#print(type(df_limpiando.Date[1]))#primero veo que tipo de data es la fecha que es un str ahora iteramos y ponemos los strings en date format
def cell_Date(a,b):
    df_limpiando.Date=df_limpiando.Date.str.replace(a ,b)

cell_Date('^Report[e]?d\s','' )
cell_Date('Reported[*]?', '')
cell_Date('^\s*', '')
cell_Date('$\w*', '')
cell_Date('^[Circa|Ca.]', '')
cell_Date('$Reported','')
cell_Date('^Before\s', '')





def cell_Species(a,b):
    df_limpiando.Species=df_limpiando.Species.str.replace(a ,b)
cell_Species('shark   probably a blacktip or spinner shark', 'spinner shark') 
cell_Species('\d+', '') #quitamos numeros /s quita espacios
cell_Species("\W", '') #quitamos no alphanumericos
cell_Species('[m]', '')
cell_Species('$m', '') #quitamos solo la primera si aparece en este caso m
cell_Species("Invalid", "Shark involvement not confirmed")
cell_Species("to   shark", 'Shark')
cell_Species("whiteshark", "White shark")
cell_Species("Shark involvement prior to death was not confirmed", "Shark involvement not confirmed")
cell_Species('$tofeet', '')
cell_Species('^to', '')
cell_Species('$to', '')
cell_Species('^Possiblya', '')
cell_Species('Sharkinvolvementnotconfirmed', 'Shark involvement not confirmed')
cell_Species('Whitesharkm', 'Whiteshark' )
cell_Species('Sharkinvolvementpriortodeathwasnotconfirmed', 'Shark involvement not confirmed')
cell_Species('Questionable', 'Shark involvement not confirmed')
#print(df_limpiando['Species'].value_counts())#esto me ayuda a ver como van la row de la columna si quiere limpiar quita #


df_limpiando.to_csv(r"C:\Users\penzi\projectos\Shark-Attack-project-v.0.1\DATASET-CSV\CLeaned_df.csv")