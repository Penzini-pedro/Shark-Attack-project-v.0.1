from turtle import left
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import re
import datetime
pd.set_option("display.max_rows", None)
df_sucio = pd.read_csv(r'C:\Users\penzi\projectos\Shark-Attack-project-v.0.1\DATASET-CSV\attacks.csv', sep= ',', encoding='latin1')

df_limpiando= df_sucio.copy()#creo una dataframe sin los rows nulos para poder limpiar y despues unirlo con los row que no necesito 

df_limpiando= df_limpiando.dropna(axis=0, how='all')#drop fillas nulas que despue svamos a join
df_limpiando= df_limpiando.drop(df_limpiando.index[6302:]) #mas facil era agarrar el range i drop que buscar los indice aunque lo pudiera hacer asi


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

cell_Date('^Rep[o]?rt[e]?d\s','' )
cell_Date('Reported?', '')
cell_Date('^\s*', '')
cell_Date('$\w*', '')
cell_Date('^(Circa|Ca|Before|Early|Late|Fall|[Ss]ummer)[\s]?', '')
cell_Date('Between','-')
cell_Date('$Reported','')
cell_Date('.', '-')
cell_Date('^-\s', '')
cell_Date('World War II', '1935-1945')
cell_Date('--','-')
cell_Date('190Feb-2010', '19-Feb-2010')
cell_Date('No date,\s','')
cell_Date('^\s*', '')
cell_Date('$-*','')
cell_Date('?','')

pd.to_datetime(df_limpiando['Date'],errors='ignore', format= "%d/%m/%Y")

#Limpiar year column convertir float to int y si quieres aplicar un date 
# cambio filla nan o 0.0 por un numero que pueda leer como int luego cambio a numericos y al final formateo para formato año
df_limpiando['Year'] = df_limpiando['Year'].fillna(0.0)
df_limpiando['Year'] = df_limpiando['Year'].replace(0.0, 1)
df_limpiando['Year'] = pd.to_numeric(df_limpiando['Year'], errors='ignore')
df_limpiando['Year'] = df_limpiando['Year'].apply(np.int64)
df_limpiando.loc[(df_limpiando.Year == 1),'Year']=df_limpiando['Date']#ojo que con esto puedes rellenar la info de una columna con otra
df_limpiando['Year']= pd.to_datetime(df_limpiando['Year'],errors='ignore', format= "/%Y")



#limpiando type
#vamos los valores que contiene
#print(df_limpiando['Type'].value_counts())
#creamos una funcion para corregir los valores en la serie
df_limpiando['Type']= df_limpiando['Type'].fillna('Invalid')
def cell_Type(a,b):
    df_limpiando.Type=df_limpiando.Type.str.replace(a ,b)
cell_Type('Questionable', 'Invalid') 
cell_Type('Sea Disaster', 'Unprovoked')
cell_Type('Boating', 'Provoked' )
cell_Type('Boatomg', 'Provoked')
cell_Type('Boat', 'Provoked')




# Limpiamos Country

df_limpiando['Country']= df_limpiando['Country'].fillna('x')
#df_limpiando['Country']= df_limpiando.loc[(df_limpiando.Country == 'x'),'Country']=df_limpiando['Area']
df_limpiando['Country']= df_limpiando['Country'].str.upper()
def cell_Country(a,b):
    df_limpiando.Country= df_limpiando.Country.str.replace(a ,b)
df_limpiando['Country']= df_limpiando['Country'].str.strip()
cell_Country('\?*','')

#print(df_limpiando['Country'].value_counts())

#Limpiamos area
df_limpiando['Area']= df_limpiando['Area'].fillna('X')
#df_limpiando['Area']= df_limpiando.loc[(df_limpiando.Country == 'x'),'Area']=df_limpiando['Country']

#Limpiamos Location

df_limpiando['Location']= df_limpiando['Location'].str.strip()
def cell_Location(a,b):
    df_limpiando.Location= df_limpiando.Location.str.replace(a ,b)
cell_Location("[^a-zA-Z0-9\s]", "",)


#limpiamos Activity
df_limpiando['Activity']= df_limpiando['Activity'].fillna('x')
df_limpiando['Activity']= df_limpiando['Activity'].str.strip()
def cell_Activity(a,b):
    df_limpiando.Activity= df_limpiando.Activity.str.replace(a ,b)
cell_Activity("[^a-zA-Z0-9\s]", "",)
df_limpiando['Activity']= df_limpiando['Activity'].fillna('Unkown')
df_limpiando['Activity']= df_limpiando['Activity'].astype(str)

df_limpiando['Activity']= df_limpiando['Activity'].str.upper()

#limpiamos sex primero porque nombre contiene info importante
df_limpiando.rename(columns = {'Sex ':'Sex'}, inplace = True)
df_limpiando.where(df_limpiando['Name']== '[male*]', df_limpiando['Sex']== 'M', axis=0) 
df_limpiando.where(df_limpiando['Name']== '[female*]', df_limpiando['Sex']== 'M', axis=0) 
df_limpiando['Sex']= df_limpiando['Sex'].fillna('U')


#limpiamos Name
df_limpiando['Name']= df_limpiando['Name'].fillna('Unkown')
df_limpiando['Name']= df_limpiando['Name'].str.strip()
def cell_Name(a,b):
    df_limpiando['Name']= df_limpiando['Name'].str.replace(a ,b)
cell_Name("[^a-zA-Z0-9\s]", "",)
cell_Name('$male|$female', '')
cell_Name('(male|female)', 'Unkown')
df_limpiando['Country']= df_limpiando['Country'].str.upper()

#Limpiamos Age
def cell_Age(a,b):
    df_limpiando['Age']= df_limpiando['Age'].str.replace(a ,b)
cell_Age('[^0-9]', '')
df_limpiando['Age']= df_limpiando['Age'].fillna('Unkown')

#Limpiamos Injury 
df_limpiando['Injury']= df_limpiando['Injury'].fillna('UNKNOWN')

#Limpiamos Fatal (Y/N)
df_limpiando.rename(columns = {'Fatal (Y/N)':'Fatal'}, inplace = True)
df_limpiando['Fatal']= df_limpiando['Fatal'].str.strip()
df_limpiando['Fatal']= df_limpiando['Fatal'].astype(str)

df_limpiando.where(df_limpiando['Injury']== '[Fatal]', df_limpiando['Fatal']== 'Y', axis=0) 
df_limpiando.where(df_limpiando['Injury']== '[Fatal]', df_limpiando['Fatal']== 'N', axis=0) 
df_limpiando['Fatal']= df_limpiando['Fatal'].str.upper()
df_limpiando['Fatal']= df_limpiando['Fatal'].replace('M', 'UNKNOWN')
df_limpiando['Fatal']= df_limpiando['Fatal'].replace('2017', 'UNKNOWN')
df_limpiando['Fatal']= df_limpiando['Fatal'].fillna('UNKNOWN')
df_limpiando['Fatal']= df_limpiando['Fatal'].replace('NAN', 'U')
df_limpiando['Fatal']= df_limpiando['Fatal'].replace('UNKNOWN', 'U')







#Limpiamos Time
df_limpiando['Time']= df_limpiando['Time'].str.strip()
df_limpiando['Time']= df_limpiando['Time'].fillna('Unkown')
df_limpiando['Time']= df_limpiando['Time'].replace('nan', 'Unkown')
df_limpiando['Time']= pd.to_timedelta(df_limpiando['Time'], errors='ignore')
#df_limpiando['Time']= df_limpiando['Time'].replace('(DUSK|NOON|LATE AFTERNOON|MORNING|MIDDAY|NIGHT)', '')
#df_limpiando['Time']= df_limpiando['Time'].replace('DUSK', '')

#Limpiamos Species
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






df_limpiando['original order']= df_limpiando['original order'].astype(int)




df_sucio.columns= df_limpiando.columns
df_limpiando= df_limpiando.concat(df_sucio, how= 'left')

df_limpiando.to_csv(r"C:\Users\penzi\projectos\Shark-Attack-project-v.0.1\DATASET-CSV\CLeaned_df.csv")
