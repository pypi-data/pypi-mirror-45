def func():

    import pandas as pd
    import sqlite3
    import csv
    import glob
    from sqlalchemy import create_engine

    myway = input('Введите путь к папке с файлами .csv для обработки в формате /my/path/to/CSV_DIR/  ')
    myway_for_read = myway+"*.csv"
    myway_for_write = myway+"result.csv"
    print(myway)

    #Перебор csv-файлов с путями в список f
    #f = glob.glob("/home/mik/workfrankomik/csv_files/*.csv")
    f = glob.glob(myway_for_read)
    print(f)


    df1 = pd.DataFrame({})
    for i in f:
        df = pd.read_csv(i,  # Это то, куда вы скачали файл
                        parse_dates = ['Дата Сдачи'],  dayfirst = True, 
                        index_col = 0)
        

        df1 = pd.concat([df1,df], join = 'outer', verify_integrity = True)

    df1 = df1.sort_values(by = ['Дата Сдачи'])
    print(df1)

    #DataFrame to CSV-file
    y = df1.to_csv()
    
    fil = open(myway_for_write, 'w')
    fil.write(y)
    fil.close()
    print(y)

    eng = create_engine('sqlite:///data-baza.db', echo = False)
    conn = eng . connect ()
    df1.to_sql('mytab', eng, if_exists = 'append')

    print('****************************************************************************************************')
    print('Результат под именем "result.csv" смотрите в вашей папке: ' + " " + myway_for_write)
    print('****************************************************************************************************')
if __name__ == "__main__":
    func()