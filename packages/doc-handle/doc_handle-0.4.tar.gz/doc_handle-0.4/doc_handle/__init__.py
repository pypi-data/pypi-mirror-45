from pyexcel_ods import get_data
import pyexcel as pe
import csv
import numpy as np
import os


def import_ods(filedir, sheetname='pyexcel sheet'):
    dict_array = get_data(filedir)
    array = dict_array[sheetname]
    return array


def save_ods(file, name):
    try:
        sheet = pe.Sheet(file)
        file_name = name
        sheet.save_as(file_name)
        # print("Data saved as \"" + file_name + "\"")
    except:
        if isinstance(file[0], str):
            for i in range(len(file)):
                file[i] = [file[i]]
            sheet = pe.Sheet(file)
            file_name = name
            sheet.save_as(file_name)
            # print("Data saved as \"" + file_name + "\"")
        else:
            new = []
            for i in range(len(file)):
                row = []
                for j in range(len(file[i])):
                    row.append(str(file[i][j]))
                new.append(row)
            sheet = pe.Sheet(new)
            file_name = name
            sheet.save_as(file_name)
            # print("Data saved as \"" + file_name + "\"")

    return


def save_csv(variable, name, separator='|'):
    if isinstance(variable, np.ndarray):
        variable1 = list(map(lambda a: list(a), variable))
    else:
        variable1 = variable
    with open(name, mode='w', encoding='utf-8') as x:
        y = csv.writer(x, delimiter=separator)
        y.writerow(list(map(lambda a: a, variable1)))
    # print('Data save as "' + str(name) + '"')
    return


def import_csv(filedir, separator='|'):
    with open(filedir, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=separator)
        readed = list(map(lambda a: eval(a), csv_reader.fieldnames))
        # raw_string = list(map(lambda a: '|'.join(a), csv_reader))

    return readed


def save_txt(file, name):
    f = open(name, 'w')
    for i in range(len(file)):
        f.write(file[i])
    # print('Data save as "' + str(name) + '"')
    return


def import_txt(file):
    with open(file, mode='r') as txt:
        listed = txt.readlines()
    return listed


def write_ods(output_file, row):
    """
    :param output_file: must be the name of the .ods file where you want to write.
    :param row: list
    :return: None
    """
    if not os.path.isfile(output_file):
        save_ods([], output_file)
    # row = list(map(lambda a: str(a), row[]))
    sheet = pe.get_sheet(file_name=output_file)
    for r in range(len(row)):
        t_to_s = str(row[r][2])
        corr_row = [row[r][0], row[r][1], t_to_s]
        sheet.row += corr_row
        sheet.save_as(output_file)
    return
