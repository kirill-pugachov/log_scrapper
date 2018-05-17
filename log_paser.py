# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 17:49:43 2018

@author: Kirill
"""

FILE_PATH = 'C:\\Users\\Кирилл\\CashDataLogScrap\\Data\\'
FILE_NAME = '9849-20180322-045740-212635-TOP.log'
#FILE_NAME = '9062-20180317-004517-234149-TOP.ENC[1].txt'
MARK_0 = 'TRANSACTION START'
MARK_1 = 'TRANSACTION END'
MARK_2 = 'CASH TAKEN'
MARK_3 = '----------'


def temp_trans(temp_tank):
    from copy import deepcopy
    temp = deepcopy(temp_tank)
    return temp
    
    
def separate_transaction(FILE_PATH, FILE_NAME, MARK_0, MARK_1):
    temp_tank = list()
    result_list = list()
    data_file = FILE_PATH + FILE_NAME
    with open(data_file, 'r', encoding='utf-8-sig') as file_to_read:
        for line in file_to_read:
            if MARK_0 in line:
                temp_tank.append(line)
            elif MARK_1 in line:
                temp_tank.append(line)
#                print(len(temp_tank))
                result_list.append(temp_trans(temp_tank))
                temp_tank.clear()
            else:
                temp_tank.append(line)                
    return result_list


def search_for_taken(transaction, MARK_2):
    temp = None
    for raws in transaction:
        if MARK_2 in raws:
            temp = transaction
        else:
            continue
    return temp


def legend_getting(list2):
    result = list()
    n = -1
    raw = list2[n]
    while raw.strip(' \t\n\r') != MARK_3:
        result.append(raw.strip(' \t\n\r'))
        n -= 1
        raw = list2[n]
#        print(n, result)
    return list(reversed(result))


def get_atm_id_date(raw):
    id_tr =  raw.split()[0]
    date = raw.split()[1]
    atm = raw.split()[3]
    return atm, id_tr, date


def get_total_curr(raw):
    total = raw.split()[3]
    curr = raw.split()[4]
    time = raw.split()[0]
    return total, curr, time


def get_code(raw):
    code = raw.split()[2]
    return code


def prepare_legend(legend_list):
    result = {'SEQ Number':'',
              'Tran date':'',
              'Tran time':'',
              'ATM':'',
              'Amount':'',
              'Currency':'',
              'Card':'',
              'Auth code':'',
              'Result': MARK_2}
    for raw in legend_list:
        if 'ATM:' in raw:
            result['ATM'], result['SEQ Number'], result['Tran date'] = get_atm_id_date(raw)
        elif 'CASH WITHDRAWAL' in raw:
            result['Amount'], result['Currency'], result['Tran time'] = get_total_curr(raw)
            result['Card'] = legend_list[legend_list.index(raw) + 2].split()[0]#идем на 2 строки ниже за номерром карты
        elif 'AUTH. CODE:' in raw:
            result['Auth code'] = get_code(raw)
    return result
    

def write_to_file(list1, list2, list3, file_number):
    data_to_write = [list1, list2, list3]
    with open(str(file_number) + '_' + 'file' + '.txt', 'a') as output:
        for key in prepare_legend(legend_getting(list2)).keys():
            output.write(key + ': ' + prepare_legend(legend_getting(list2))[key] + '\n')
        output.write('\n')
        for data in data_to_write:
            for raw in data:
                output.write(raw)
            output.write('****'*45 + '\n')
            output.write('\n')
       

def build_files_with_taken(transaction_list):
    for transaction in transaction_list:
        if search_for_taken(transaction, MARK_2):
            if transaction_list.index(transaction) == 0:
                print('Первая транзакция в логе')
                print('Индекс TAKEN', transaction_list.index(transaction))
                print('Индекс следующей за TAKEN транзакции', transaction_list.index(transaction) + 1)
                print('\n')
                list1 = ['Первая транзакция в логе', '\n']
                list2 = transaction_list[transaction_list.index(transaction)]
                list3 = transaction_list[transaction_list.index(transaction) + 1]
                file_number = transaction_list.index(transaction)
                write_to_file(list1, list2, list3, file_number)
            elif transaction_list.index(transaction) == (len(transaction_list) - 1):
                print('Индекс преведущей до TAKEN транзакции', transaction_list.index(transaction) - 1)
                print('Индекс TAKEN', transaction_list.index(transaction))
                print('Последняя транзакция в логе')
                print('\n')
                list1 = transaction_list[transaction_list.index(transaction) - 1]
                list2 = transaction_list[transaction_list.index(transaction)]
                list3 = ['Последняя транзакция в логе', '\n']
                file_number = transaction_list.index(transaction)
                write_to_file(list1, list2, list3, file_number)
            else:
                print('Индекс преведущей до TAKEN транзакции', transaction_list.index(transaction) - 1)
                print('Индекс TAKEN', transaction_list.index(transaction))
                print('Индекс следующей за TAKEN транзакции', transaction_list.index(transaction) + 1)
                print('\n')
                list1 = transaction_list[transaction_list.index(transaction) - 1]
                list2 = transaction_list[transaction_list.index(transaction)]
                list3 = transaction_list[transaction_list.index(transaction) + 1]
                file_number = transaction_list.index(transaction)
                write_to_file(list1, list2, list3, file_number)

                
if __name__ == "__main__":
    transaction_list = separate_transaction(FILE_PATH, FILE_NAME, MARK_0, MARK_1)
    build_files_with_taken(transaction_list)