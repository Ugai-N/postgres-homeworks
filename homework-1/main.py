"""Скрипт для заполнения данными таблиц в БД Postgres."""
import os

import psycopg2
import pathlib
import csv

FILE_PATH = pathlib.Path(__file__).resolve().parent / 'north_data'
database = 'north'
password = os.getenv('POSTGRES_PASSWORD')


def instantiate_from_csv(file_name) -> list:
    """Парсит данные из csv-файла, возвращает список строк, каждая строка - список"""
    file = FILE_PATH / file_name
    if os.path.exists(file):
        with open(file, newline='', encoding='UTF-8') as f:
            lst = []
            reader = csv.reader(f)
            for col in reader:
                lst.append(col)
        return lst[1:]
    else:
        raise FileNotFoundError('Отсутствует файл item.csv')


def set_customers_list() -> list:
    customers_list = []
    customers_list_raw = instantiate_from_csv('customers_data.csv')
    for customer in customers_list_raw:
        customer = tuple(customer)
        customers_list.append(customer)
    return customers_list


def set_employees_list() -> list:
    employees_list = []
    employees_list_raw = instantiate_from_csv('employees_data.csv')
    for employee in employees_list_raw:
        employee[0] = int(employee[0])
        employee = tuple(employee)
        employees_list.append(employee)
    return employees_list


def set_orders_list() -> list:
    orders_list = []
    orders_list_raw = instantiate_from_csv('orders_data.csv')
    for line in orders_list_raw:
        line[0] = int(line[0])
        line[2] = int(line[2])
        line = tuple(line)
        orders_list.append(line)
    return orders_list


connection = psycopg2.connect(host='localhost', database=database, user='postgres', password=password)
try:
    with connection:
        '''контекстный менеджер для установки соединения (при закрытии авто коммит)'''
        with connection.cursor() as cursor:
            '''контекстный менеджер для установки курсора по автозаполнению customers_list (авто закрытие)'''
            cursor.executemany('INSERT into customers_data VALUES (%s, %s, %s)', set_customers_list())
            cursor.execute('SELECT * from customers_data')
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        with connection.cursor() as cursor:
            '''контекстный менеджер для установки курсора по автозаполнению employees_list (авто закрытие)'''
            cursor.executemany('INSERT into employees_data VALUES (%s, %s, %s, %s, %s, %s)', set_employees_list())
            cursor.execute('SELECT * from employees_data')
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        with connection.cursor() as cursor:
            '''контекстный менеджер для установки курсора по автозаполнению orders_list (авто закрытие)'''
            cursor.executemany('INSERT into orders_data VALUES (%s, %s, %s, %s, %s)', set_orders_list())
            cursor.execute('SELECT * from orders_data')
            rows = cursor.fetchall()
            for row in rows:
                print(row)
finally:
    connection.close()
