from pandas import pandas as pd
import numpy as np
#import datetime as dt



def read_file():
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

    return df

def create_scenario(filepath_csv,columns_names_array,column_name_previous_data,interval,num_previuos_data,test_percent):
    print("*Creando Escenario*")

    df=read_file(filepath_csv,["Date","Time"]+columns_names_array)
    dfg=group_by_mean(df,interval)

    #dfg=replace_nan_column(dfg,'Humidity',-1)
    #dfg=replace_nan_column(dfg,'TemperatureC',-1)
    #dfg=replace_nan_column(dfg,'LDR',-1)

    dfgp=previous_data(dfg,column_name_previous_data,num_previuos_data)

    #Enviar la columna al final del dataframe(Crear otra columna con los mismos datos)
    dfgp[column_name_previous_data+"_Actual"]=dfgp[column_name_previous_data]
    dfgp = dfgp.drop(column_name_previous_data, 1)

    filename_export="../data/Escenario_"+column_name_previous_data+"_"+interval+"_"+str(num_previuos_data)+".csv"
    print(filename_export)
    print(dfgp)
    dfgp.to_csv(filename_export)

def manager_scenarios(filepath_csv,interval,num_previuos_data,test_percent):
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
    colnam_tlh=[T,L,H]

    create_scenario(filepath_csv,colnam_h,H,interval,num_previuos_data,test_percent)
    create_scenario(filepath_csv,colnam_t,T,interval,num_previuos_data,test_percent)
    create_scenario(filepath_csv,colnam_l,L,interval,num_previuos_data,test_percent)




def main():
    print("*********************Start*********************")

    #df=read_file()
    #print(df)

    # group data using interval for T= hour, M= month, S= second
    #df=group_by_mean(df,"h")


    #df=replace_nan_column(df,'Humidity',-1)
    #df=replace_nan_column(df,'TemperatureC',-1)
    #df=replace_nan_column(df,'LDR',-1)

    #Agregar Datos Anteriores
    #df=previous_data(df,2,"Humidity")

    #print(df)

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
    colnam_tlh=[T,L,H]

    colnam_dt=["Date","Time"]

    print(colnam_tlh+colnam_dt)



    #df=read_file('../data/Data_Planta.csv',None);
    #print(df)

    #create_scenario('../data/Data_Planta.csv',colnam_h,H,"h",3,0)

    manager_scenarios('../data/Data_Planta.csv',"h",3,0)












    # export to csv
    #df.to_csv('../data/DataTemp.csv')





    print("*********************End*********************")
main()

