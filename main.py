from faker import Faker
from faker.providers import DynamicProvider
from random import randint
import random
import threading
import concurrent.futures
import json
import time
import os
from multiprocessing import Pool
import csv
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import math

fake = Faker('pl_PL')

OFFICE_NUMBER = 20
REAL_ESTATE_NUMBER = 500
EMPLOYEES_NUMBER = 100
T1_start_date = date(2020, 1, 1)
T1_end_date = date(2022, 12, 31)
T2_start_date = date(2023, 1, 1)
T2_end_date = date(2023, 12, 31)
ORDER_NUMBER = 1000
ADDRESSES_NUMBER = 200
DEVELOPERS_NUMBER = 100

start_time = time.time()
lock = threading.Lock()




def fakeOffice(n):
    data = []
    print(os.getpid())
    for i in range(0, n):
        temp = {}
        temp['FK_address'] = fake.random_int(min=1, max=ADDRESSES_NUMBER)
        data.append(temp)
    return data


# data provider for generating fake positions for employees
employee_positions_provider = DynamicProvider(
    provider_name="employee_position",
    elements=["customer service", "finance", "head office manager", "operations manager", "marketing manage", "trainee"],
)
fake.add_provider(employee_positions_provider)


def generatePesel():
    year = fake.random_int(min=0, max=99)
    month = fake.random_int(min=1, max=12)
    day = fake.random_int(min=1, max=28)
    birth_date_str = f"{year:02}{month:02}{day:02}"
    unique_id = fake.random_int(min=10000, max=99999)

    pesel_str = f"{birth_date_str}{unique_id}"

    random_control_digit = fake.random_int(min=0, max=9)



    return pesel_str


def fakeEmployee(n):
    data = []
    employee_composite_pk = []
    for i in range(0, n):
        temp = {}
        temp['fk_office'] = randint(1, OFFICE_NUMBER)
        temp['firstName'] = fake.first_name()
        temp['lastName'] = fake.last_name()
        temp['position'] = fake.employee_position()
        temp['employmentDate'] = fake.date_between(start_date=T1_start_date, end_date=T1_end_date)
        if temp['position'] == 'trainee':
            temp['endDate'] = fake.date_between(start_date=temp['employmentDate'], end_date=T2_end_date)
        else:
            temp['endDate'] = None
        temp['is_current'] = 0
        temp['pesel'] = generatePesel()
        employee_composite_pk.append((i,temp['employmentDate']))
        data.append(temp)

    return data, employee_composite_pk

def fakeEmployeePromoted(n, employee_promoted_data):
    data = []
    employee_composite_pk = []
    for i in range(0, n):
        temp = employee_promoted_data[i].copy()
        if temp['position'] == 'trainee':
            temp['position'] = 'customer service'
            temp['employmentDate'] = employee_promoted_data[i]['endDate']
            temp['is_current'] = 1
            temp['endDate'] = None
            employee_composite_pk.append((i, temp['employmentDate']))
            data.append(temp)

    return data


# data provider for generating types of real estate
real_estate_type_provider = DynamicProvider(
    provider_name="real_estate_type",
    elements=["house", "apartment", "commercial office"],
)
fake.add_provider(real_estate_type_provider)


def fakeRealEstate(n):
    data = []
    for i in range(0, n):
        temp = {}
        temp['FK_address'] = fake.random_int(min=1, max=ADDRESSES_NUMBER)
        temp['type'] = fake.real_estate_type()
        temp['number_of_rooms'] = randint(1, 5)
        temp['area'] = randint(20, 80)
        temp['price'] = randint(1000, 5000)
        temp['owner'] = fake.name()
        data.append(temp)
    return data


def generateMultithreaded(func, thread_count, objects_count, *args):
    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as executor:
        print(int(math.ceil(objects_count / thread_count)))
        results = [executor.submit(func, int(math.ceil(objects_count / thread_count)), *args) for _ in
                   range(thread_count)]

        all_data = []
        all_composite_pks = []
        for r in results:
            result = r.result()
            if func == fakeEmployee:
                all_data.extend(result[0])
                all_composite_pks.extend(result[1])
            else:
                all_data.extend(result)
    return (all_data, all_composite_pks) if func == fakeEmployee else all_data


def fakeAddress(n):
    data = []
    print(os.getpid())
    for i in range(0, n):
        temp = {}
        temp['city'] = fake.city()
        temp['neighbourhood'] = fake.city_suffix()
        temp['street '] = fake.street_name()
        temp['house_number '] = fake.random_int(min=1, max=50)
        temp['apartment_number '] = fake.random_int(min=1, max=50)
        temp['postal_code'] = fake.postcode()
        data.append(temp)
    return data


# data provider for order status
real_estate_status_provider = DynamicProvider(
    provider_name="real_estate_status",
    elements=["done", "in progress", "cancelled"],
)
fake.add_provider(real_estate_status_provider)


def fakeOrder(n):
    data = []
    orders = []
    invoices = []
    print(os.getpid())
    for i in range(0, n):
        temp = {}
        temp['real_estate'] = fake.random_int(min=1, max=REAL_ESTATE_NUMBER - 1)
        temp['date_of_order'] = fake.date_between(start_date=T1_start_date, end_date=T1_end_date)
        temp['margin'] = fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=5, max_value=50)
        temp['status'] = fake.real_estate_status()
        temp['rent'] = fake.random_int(min=1, max=36)
        temp['rent_start_date'] = fake.date_between(start_date=T1_start_date, end_date=T1_end_date)
        temp['rent_end_date'] = temp['rent_start_date'] + relativedelta(months=int(temp['rent']))
        order_date = temp['date_of_order']
        orders.append(temp)
        temp = {}
        temp['FK_order'] = fake.random_int(min=1, max=ORDER_NUMBER - 1)
        temp['issue_date'] = fake.date_between(start_date=order_date, end_date=order_date + relativedelta(days=14))
        temp['price'] = fake.random_int(min=1000, max=5000)
        temp['payment_date'] = fake.date_between(start_date=temp['issue_date'],
                                                 end_date=temp['issue_date'] + relativedelta(days=14))
        temp['payment_form'] = fake.payment_type()
        invoices.append(temp)
    data.append(orders)
    data.append(invoices)
    return data


# data provider for order status
payment_type_provider = DynamicProvider(
    provider_name="payment_type",
    elements=["Mastercard", "Visa", "cash", "transfer"],
)
fake.add_provider(payment_type_provider)


def fakeInvoice(n, orders):
    data = []
    print(os.getpid())
    for i in range(0, n):
        temp = {}
        temp['FK_order'] = fake.random_int(min=0, max=ORDER_NUMBER - 1)
        order_date = orders[int(temp['FK_order'])]['date_of_order']
        temp['issue_date'] = fake.date_between(start_date=order_date, end_date=order_date + relativedelta(days=14))
        temp['price'] = fake.random_int(min=1000, max=5000)
        temp['payment_date'] = fake.date_between(start_date=temp['issue_date'],
                                                 end_date=temp['issue_date'] + relativedelta(days=14))
        temp['payment_form'] = fake.payment_type()
        data.append(temp)
    return data


'''
generating data for excell
'''


def fakeDeveloper(n):
    data = []
    for i in range(0, n):
        temp = {}
        temp['company_name'] = fake.company()
        temp['nip'] = fake.numerify(text='###-###-##-##')
        temp['start_date'] = fake.date_between(start_date='-5y', end_date='today')
        temp['developer_start_date'] = fake.date_between(start_date='-10y', end_date='today')
        temp['credit_rating'] = random.choice(['Bardzo dobra', 'Dobra', 'Średnia', 'Zła'])
        temp['project_count'] = random.randint(1, 50)
        data.append(temp)
    return data


def fakeOffers(n, developers):
    data = []
    for i in range(0, n):
        temp = {}
        temp['developer_nip'] = developers[randint(0, len(developers) - 1)]['nip']
        temp['rent_price'] = round(random.uniform(500.00, 5000.00), 2)
        temp['apartment_size'] = round(random.uniform(30.00, 150.00), 2)
        temp['address'] = fake.address().replace("\n", ", ")
        temp['planned_end_date'] = fake.date_between(start_date='today', end_date='+1y')
        temp['actual_end_date'] = fake.date_between(start_date=temp['planned_end_date'],
                                                    end_date=temp['planned_end_date'] + relativedelta(days=30))
        temp['status'] = random.choice(['gotowe', 'oczekuje'])
        data.append(temp)
    return data


def writeToFile(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nr'] + list(data[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for index, row in enumerate(data, start=1):
            data[index-1]['Nr'] = index
            row_with_index = {'Nr': index, **row}
            writer.writerow(row_with_index)
    return data

def writeEmployee2ToFile(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        data = [{'Nr': d['Nr'], **{k: v for k,v in d.items() if k!='Nr'}} for d in data]
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        for index, row in enumerate(data, start=1):
            row_with_index = { **row}
            writer.writerow(row_with_index)
    return data

def writeOrdersToFile(filename, data, employee_composite_pk):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Nr', 'EmployeeID', 'EmploymentDate'] + list(data[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for index, row in enumerate(data, start=1):
            employee_id, employment_date = random.choice(employee_composite_pk)
            row_with_index = {'Nr': index,
                              'EmployeeID': employee_id,
                              'EmploymentDate': employment_date,
                              **row}
            writer.writerow(row_with_index)

def main():
    PROCESSES = 4
    results = generateMultithreaded(fakeOffice, PROCESSES, OFFICE_NUMBER)
    writeToFile('offices.csv', results)

    results, employee_info = generateMultithreaded(fakeEmployee, PROCESSES, EMPLOYEES_NUMBER)
    employee_promoted_results = results
    employee_promoted_results = writeToFile('employess.csv', results)
    print(employee_promoted_results)
    #results = generateMultithreaded(fakeEmployeePromoted, PROCESSES, EMPLOYEES_NUMBER, employee_promoted_results)
    results = fakeEmployeePromoted(EMPLOYEES_NUMBER, employee_promoted_results)
    writeEmployee2ToFile('employess_t2.csv', results)

    results = generateMultithreaded(fakeRealEstate, PROCESSES, REAL_ESTATE_NUMBER)
    writeToFile('real_estates.csv', results)

    r = generateMultithreaded(fakeOrder, PROCESSES, ORDER_NUMBER)
    results = r[0]
    invoices = r[1]
    orders = results
    writeOrdersToFile('orders.csv', results, employee_info)
    writeToFile('invoices.csv', invoices)

    results = generateMultithreaded(fakeAddress, PROCESSES, ADDRESSES_NUMBER)
    writeToFile('addresses.csv', results)

    results = generateMultithreaded(fakeDeveloper, PROCESSES, ADDRESSES_NUMBER)
    writeToFile('developers.csv', results)

    developers = results
    results = generateMultithreaded(fakeOffers, PROCESSES, ADDRESSES_NUMBER, developers)
    writeToFile('offers.csv', results)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"time: {elapsed_time}")


if __name__ == "__main__":
    main()