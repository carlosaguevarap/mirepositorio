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


def previous_data(df,num_previous,column_name):
    print("*Datos Anteriores*")

    #Reindexar para trabajar con numero entero en index
    df["IndexNum"]=range(0,df.index.size)
    df.set_index("IndexNum",inplace=True)

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



def main():
    print("**Start**")

    df=read_file()
    #print(df)

    # group data using interval for T= hour, M= month, S= second
    df=group_by_mean(df,"h")


    df=replace_nan_column(df,'Humidity',-1)
    df=replace_nan_column(df,'TemperatureC',-1)
    df=replace_nan_column(df,'LDR',-1)

    #Agregar Datos Anteriores
    df=previous_data(df,2,"Humidity")

    print(df)








    # export to csv
    df.to_csv('../data/DataTemp.csv')





    print("**End**")
main()

