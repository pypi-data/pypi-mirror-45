def main():

    import pandas as pd
    import glob
    from sqlalchemy import create_engine

    #Запрос на путь к папке с файлами
    myway = input('Введите путь к папке с файлами .csv для обработки в формате /my/path/to/CSV_DIR/  ')
    myway_for_read = myway+"*.csv"
    myway_for_write = myway+"result.csv"


    #Создаем список f csv-файлов с путями  
    f = glob.glob(myway_for_read)

    #Создаем пустой датафрейм для последующей конкатенации
    df1 = pd.DataFrame({})

    #Парсим список f по колонке 'Дата Сдачи'с приведением даты с произвольного в форматированный вид,
    #пулучeнные датафреймы конкатенируем в df1
    for i in f:
        df = pd.read_csv(i, 
                    parse_dates = ['Дата Сдачи'],  dayfirst = True, 
                    index_col = 0)
        df1 = pd.concat([df1,df], join = 'outer', verify_integrity = True)

    #Сортируем колонку "Дата сдачи"
    df1 = df1.sort_values(by = ['Дата Сдачи'])

    #DataFrame to CSV-file
    x = df1.to_csv()

    #Запись в файл отсортированного датафрейма    
    fil = open(myway_for_write, 'w')
    fil.write(x)
    fil.close()
    print(df1)
    print(x)
    #Создание базы данных sqlite и слив в нее готового датафрейма
    eng = create_engine('sqlite:///data-baza.db', echo = False)
    conn = eng . connect ()
    df1.to_sql('mytab', eng, if_exists = 'append')

    print('****************************************************************************************************')
    print('Результат под именем "result.csv" смотрите в вашей папке: '+ myway_for_write) 
    print('!При повторном старте программы Этот файл нужно удалить!')
    print('****************************************************************************************************')
    #!!!При повторном запуске скрипта удалить полученный файл "result.csv" из папки!!!

if __name__ == "__main__":
    main()