from pandas import pandas
import os

def main():
    print('Carga de datos')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../Data/Data_planta.csv')
    df = pandas.read_csv(filename,sep=', ')
    print(df)

if __name__ == '__main__':
    main()

