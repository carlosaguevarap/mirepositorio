from pandas import pandas as pd
import numpy as np

def read_file(filepath,columns_names):
    df=pd.DataFrame()
    if(columns_names is None):
        df = pd.read_csv(filepath,parse_dates=[['Date', 'Time']])
    else:
        df = pd.read_csv(filepath,parse_dates=[['Date', 'Time']],usecols=columns_names)
    df.index = df["Date_Time"]

    return df;

def main():
    print("Correlacion Humidity - TemperatureC - LDR")
    df=read_file('../data/Data_Planta.csv',None)
    df=df.corr('pearson')
    print(df)
main()
