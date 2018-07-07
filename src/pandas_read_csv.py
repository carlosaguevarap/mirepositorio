from pandas import pandas as pd
import numpy as np
#import datetime as dt


#Deprecated(Metodo solo de prueba)
def read_file0():
    print("*Leer Archivo*")

    #Leer el archivo y unir la fecha(Date) y hora(Time) en un solo campo(Date_time)
    df = pd.read_csv('../data/Data_Planta.csv',parse_dates=[['Date', 'Time']])


    #Definir el Index
    df.index = df["Date_Time"]

    #df['Timestamp'] = df.Date_Time.values.astype(np.int64)
    #df.set_index('Timestamp')

    return df;

def read_file(filepath,columns_names):
    print("*Leer Archivo*")

    df=pd.DataFrame()

    #Leer el archivo y unir la fecha(Date) y hora(Time) en un solo campo(Date_time)
    if(columns_names is None):
        df = pd.read_csv(filepath,parse_dates=[['Date', 'Time']])
    else:
        df = pd.read_csv(filepath,parse_dates=[['Date', 'Time']],usecols=columns_names)

    #Definir el Index
    df.index = df["Date_Time"]

    #df['Timestamp'] = df.Date_Time.values.astype(np.int64)
    #df.set_index('Timestamp')

    return df;

def group_by_mean(dataframe,interval):
    print("*Agrupar*")

    #Agrupar Datos
    dfg = dataframe.resample(interval).mean()
    return dfg

def replace_nan_column(dataframe,column_name,value):
    print("*Cambiar NaN*")

    # change NaN (empty data) to 'value'
    if column_name in dataframe.columns:
        #dataframe["column_name"]=dataframe[column_name].fillna(value)
        dataframe[column_name] = dataframe[column_name].replace(np.nan,value)
    return dataframe


def previous_data(df,column_name,num_previous):
    print("*Datos Anteriores*")

    #Reindexar para trabajar con numero entero en index
    df["IndexNum"]=range(0,df.index.size)

    #Reemplazar el index(Borra la columna de index actual)
    #df.set_index("IndexNum",inplace=True)

    #Agrega otra columna con el index
    df = df.reset_index().set_index("IndexNum")

    #Crear un dataframe
    prev_df=pd.DataFrame()

    #Por cada registro, buscar datos anteriores y colocarlos en un DataFrame Auxiliar
    for i in df.index:
        prev_index=i-num_previous
        if(prev_index>=0):
            prev_data=df.iloc[prev_index:prev_index+num_previous][column_name].values
            aux_df=pd.DataFrame(prev_data)
            aux_df=aux_df.T
            aux_df["IndexNum"]=i
            aux_df.set_index("IndexNum",inplace=True)

            #Agregar al Dataframe consolidado
            prev_df = pd.concat([prev_df,aux_df])

    #Renombrar las columnas del dataframe
    for c in prev_df.columns:
        new_column_name=column_name+"_"+str(num_previous-c)
        prev_df.rename(columns={c: new_column_name}, inplace=True)

    #Unir el DataFrame consolidado con el DataFrame Original
    df=pd.merge(df, prev_df,on="IndexNum", how='outer')

    #Enviar la columna al final del dataframe(Crear otra columna con los mismos datos)
    df[column_name+"_Actual"]=df[column_name]
    df = df.drop(column_name, 1)

    #Reemplazar el index(Borra la columna de index actual)
    df.set_index("Date_Time",inplace=True)

    return df

#Divide un dataframe en dos partes
def split_data_frame(data_frame,split_percent):

    if(split_percent<=0 or split_percent>100):
        split_percent=100

    if(split_percent==100):
        return [data_frame,None]

    #Reindexar para trabajar con numero entero en index
    data_frame["IndexNum"]=range(0,data_frame.index.size)

    #Agrega otra columna con el index
    data_frame = data_frame.reset_index().set_index("IndexNum")

    split_index=int((split_percent*data_frame.index.size)/100)

    df1=data_frame.iloc[0:split_index]
    df2=data_frame.iloc[split_index:data_frame.index.size]

    #Reemplazar el index(Borra la columna de index actual)
    df1.set_index("Date_Time",inplace=True)
    df2.set_index("Date_Time",inplace=True)

    return[df1,df2]


def create_scenario(filepath_csv,columns_names_array,interval,num_previuos_data,split_percent):
    print("*Creando Escenario*")

    df=read_file(filepath_csv,["Date","Time"]+columns_names_array)
    dfg=group_by_mean(df,interval)

    #dfg=replace_nan_column(dfg,'Humidity',-1)
    #dfg=replace_nan_column(dfg,'TemperatureC',-1)
    #dfg=replace_nan_column(dfg,'LDR',-1)

    #Nombres de las columnas para colocar en el nombre del archivo a generar
    colnames=""

    #Buscar datos anteriores en cada columna
    for column in columns_names_array:
        dfg=previous_data(dfg,column,num_previuos_data)
        colnames=colnames+"_"+column

    #Eliminar registros con NaN
    dfg=dfg.dropna()

    #Dividir los datos en dos bloques(Escenario y pruebas)
    df_split=split_data_frame(dfg,split_percent)

    #Ruta de los achivos a generar
    filename_export="../data_generated/Escenario"+colnames+"_"+interval+"_"+str(num_previuos_data)

    #Exportar el archivo de datos
    df_split[0].to_csv(filename_export+"_data.csv")

    #Exportar el archivo de pruebas
    if(df_split[1] is not None):
        df_split[1].to_csv(filename_export+"_test.csv")

    print("*Escenario creado: "+filename_export+" *")

def manager_scenarios(filepath_csv,interval,num_previuos_data,split_percent):
    print("*Generar Escenarios*")

    H="Humidity"
    T="TemperatureC"
    L="LDR"

    colnam_h=[H]
    colnam_t=[T]
    colnam_l=[L]

    colnam_th=[T,H]
    colnam_lh=[L,H]
    colnam_ht=[H,T]
    colnam_lt=[L,T]
    colnam_hl=[H,L]
    colnam_tl=[T,L]

    colnam_tlh=[T,L,H]
    colnam_lth=[L,T,H]
    colnam_hlt=[H,L,T]
    colnam_lht=[L,H,T]
    colnam_htl=[H,T,L]
    colnam_thl=[T,H,L]

    create_scenario(filepath_csv,colnam_h,interval,num_previuos_data,split_percent)#1
    create_scenario(filepath_csv,colnam_t,interval,num_previuos_data,split_percent)#2
    create_scenario(filepath_csv,colnam_l,interval,num_previuos_data,split_percent)#3

    create_scenario(filepath_csv,colnam_th,interval,num_previuos_data,split_percent)#4
    create_scenario(filepath_csv,colnam_lh,interval,num_previuos_data,split_percent)#5
    create_scenario(filepath_csv,colnam_ht,interval,num_previuos_data,split_percent)#6
    create_scenario(filepath_csv,colnam_lt,interval,num_previuos_data,split_percent)#7
    create_scenario(filepath_csv,colnam_hl,interval,num_previuos_data,split_percent)#8
    create_scenario(filepath_csv,colnam_tl,interval,num_previuos_data,split_percent)#9

    create_scenario(filepath_csv,colnam_tlh,interval,num_previuos_data,split_percent)#10
    create_scenario(filepath_csv,colnam_lth,interval,num_previuos_data,split_percent)#11
    create_scenario(filepath_csv,colnam_hlt,interval,num_previuos_data,split_percent)#12
    create_scenario(filepath_csv,colnam_lht,interval,num_previuos_data,split_percent)#13
    create_scenario(filepath_csv,colnam_htl,interval,num_previuos_data,split_percent)#14
    create_scenario(filepath_csv,colnam_thl,interval,num_previuos_data,split_percent)#15





def main():
    print("*********************Start*********************")

    manager_scenarios('../data/Data_Planta.csv',"h",3,70)

    print("*********************End*********************")


main()

